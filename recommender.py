"""Generates activity recommendations, safe time windows and safety advice."""

from dataclasses import dataclass

from datetime import date, datetime, time, timedelta

from typing import List, Optional

from analyzer import ActivityRiskAnalyzer, HourAssessment, Rating

from exceptions import InvalidInputError, WeatherDataError

from models import Forecast, Location

@dataclass

class TimeWindow:

    """Represents a continuous period for an outdoor activity."""

    assessments: List[HourAssessment]

    score: float

    @property

    def start(self) -> datetime:

        return self.assessments[0].hour.time

    @property

    def end(self) -> datetime:

        return self.assessments[-1].hour.time + timedelta(hours=1)

    @property

    def rating(self) -> Rating:

        return Rating.from_score(self.score)

    @property

    def label(self) -> str:

        return f"{self.start:%H:%M}-{self.end:%H:%M}"

@dataclass

class ActivityPlan:

    """Stores the complete recommendation for an outdoor activity."""

    location: Location

    activity_name: str

    day: date

    duration: int

    window: TimeWindow

    reasons: List[str]

    advice: List[str]

    checklist: List[str]

    hourly: List[HourAssessment]

    day_average: float

    user_chose_time: bool = False

    @property

    def rating(self) -> Rating:

        return self.window.rating

    def hourly_table(self) -> str:

        """Creates a readable table of hourly weather assessments."""

        rows = [

            f"{'Time':<7}{'Temp':>7}{'Feels':>7}"

            f"{'Rain%':>7}{'Wind':>7}{'UV':>5}  Rating"

        ]

        for assessment in self.hourly:

            hour = assessment.hour

            def display(value, suffix=""):

                if value is None:

                    return "N/A"

                return f"{value:.0f}{suffix}"

            rows.append(

                f"{hour.time:%H:%M:<7}"

                f"{display(hour.temperature, '°'):>7}"

                f"{display(hour.apparent_temp, '°'):>7}"

                f"{display(hour.rain_probability, '%'):>7}"

                f"{display(hour.wind_speed):>7}"

                f"{display(hour.uv_index):>5}  "

                f"{assessment.rating.value}"

            )

        return "\n".join(rows)

    def to_text(self) -> str:

        """Converts the activity plan into readable text."""

        label = (

            "Your chosen time"

            if self.user_chose_time

            else "Best time"

        )

        lines = [

            f"ACTIVITY PLAN - {self.activity_name} "

            f"in {self.location.label}",

            f"Date: {self.day:%A, %d %B %Y}",

            f"Verdict: {self.rating.value.upper()}",

            f"{label}: {self.window.label}, {self.duration}h",

            "",

            "Why:",

            *[f"  - {reason}" for reason in self.reasons],

            "",

            "Safety advice:",

            *[f"  - {item}" for item in self.advice],

            "",

            "Packing checklist:",

            *[f"  [ ] {item}" for item in self.checklist],

        ]

        return "\n".join(lines)

class RecommendationEngine:

    """Finds suitable activity times and generates recommendations."""

    def __init__(self, analyzer: ActivityRiskAnalyzer):

        self.analyzer = analyzer

        self.activity = analyzer.activity

    # ---------------- WINDOW SELECTION ----------------

    def candidate_hours(self, forecast: Forecast, day: date):

        """Gets available hourly forecasts within activity hours."""

        start_hour, end_hour = self.activity.active_hours

        hours = forecast.daytime_hours(

            day,

            start_hour,

            end_hour

        )

        # Excludes past hours when planning for today

        if forecast.local_now and day == forecast.local_now.date():

            cutoff = forecast.local_now.replace(

                minute=0,

                second=0,

                microsecond=0

            )

            hours = [

                hour for hour in hours

                if hour.time >= cutoff

            ]

        if not hours:

            raise WeatherDataError(

                f"No usable forecast hours for "

                f"{self.activity.name} on {day}."

            )

        return hours

    @staticmethod

    def _validate_duration(duration):

        """Ensures the requested duration is a positive integer."""

        if (

            isinstance(duration, bool)

            or not isinstance(duration, int)

            or duration < 1

        ):

            raise InvalidInputError(

                "Duration must be a positive whole number."

            )

    @staticmethod

    def _window_score(chunk: List[HourAssessment]) -> float:

        """Scores a window while considering its worst hour."""

        scores = [assessment.score for assessment in chunk]

        average = sum(scores) / len(scores)

        worst = max(scores)

        return round(0.7 * average + 0.3 * worst, 1)

    @staticmethod

    def _is_continuous(chunk):

        """Checks that all forecast hours are consecutive."""

        for index in range(len(chunk) - 1):

            current = chunk[index].hour.time

            following = chunk[index + 1].hour.time

            if following - current != timedelta(hours=1):

                return False

        return True

    def find_best_window(

        self,

        assessments: List[HourAssessment],

        duration: int

    ) -> TimeWindow:

        """Finds the lowest-risk continuous window."""

        self._validate_duration(duration)

        if duration > len(assessments):

            raise WeatherDataError(

                "Not enough forecast hours for the requested duration."

            )

        best = None

        for index in range(len(assessments) - duration + 1):

            chunk = assessments[index:index + duration]

            if not self._is_continuous(chunk):

                continue

            window = TimeWindow(

                chunk,

                self._window_score(chunk)

            )

            if best is None or window.score < best.score:

                best = window

        if best is None:

            raise WeatherDataError(

                "No continuous forecast window is available."

            )

        return best

    def window_at(

        self,

        assessments: List[HourAssessment],

        start: time,

        duration: int

    ) -> TimeWindow:

        """Finds a continuous window beginning at the chosen time."""

        self._validate_duration(duration)

        if not assessments:

            raise WeatherDataError(

                "No forecast hours are available."

            )

        if not isinstance(start, time):

            raise InvalidInputError(

                "Please provide a valid start time."

            )

        for index, assessment in enumerate(assessments):

            if assessment.hour.time.time() == start:

                chunk = assessments[index:index + duration]

                if len(chunk) != duration:

                    raise InvalidInputError(

                        "The requested duration exceeds available hours."

                    )

                if not self._is_continuous(chunk):

                    raise InvalidInputError(

                        "The requested time window contains missing hours."

                    )

                return TimeWindow(

                    chunk,

                    self._window_score(chunk)

                )

        raise InvalidInputError(

            f"The selected start time {start:%H:%M} "

            "is unavailable."

        )

    # ---------------- WEATHER STATISTICS ----------------

    @staticmethod

    def _stats(window: TimeWindow) -> dict:

        """Calculates weather statistics for a selected window."""

        hours = [assessment.hour for assessment in window.assessments]

        if not hours:

            raise WeatherDataError(

                "The selected window has no weather data."

            )

        def values(attribute):

            result = [

                getattr(hour, attribute)

                for hour in hours

                if isinstance(getattr(hour, attribute), (int, float))

                and not isinstance(getattr(hour, attribute), bool)

            ]

            if not result:

                raise WeatherDataError(

                    f"Missing weather information: {attribute}"

                )

            return result

        return {

            "feels_max": max(values("apparent_temp")),

            "feels_min": min(values("apparent_temp")),

            "rain": max(values("rain_probability")),

            "wind": max(values("wind_speed")),

            "gust": max(values("wind_gusts")),

            "uv": max(values("uv_index")),

            "humidity": max(values("humidity")),

            "storm": any(hour.is_thunderstorm for hour in hours),

        }

    # ---------------- SAFETY ADVICE ----------------

    def safety_advice(self, window: TimeWindow) -> List[str]:

        """Generates safety advice based on forecast conditions."""

        stats = self._stats(window)

        advice = []

        if stats["storm"]:

            advice.append(

                "Thunderstorm expected: do not stay outdoors. "

                "Postpone the activity."

            )

        if stats["feels_max"] >= 35:

            advice.append(

                "Extreme heat: take frequent shade breaks and "

                "stop if you feel dizzy or nauseous."

            )

        elif stats["feels_max"] >= 30:

            advice.append(

                "Hot conditions: drink water regularly and "

                "avoid the midday sun."

            )

        if stats["feels_min"] <= 5:

            advice.append(

                "Cold conditions: dress in layers."

            )

        if stats["rain"] >= 60:

            advice.append(

                "Rain is likely: surfaces may be slippery."

            )

        elif stats["rain"] >= 40:

            advice.append(

                "Rain is possible: prepare a place to take cover."

            )

        if stats["wind"] >= 40 or stats["gust"] >= 60:

            advice.append(

                "Strong wind expected: stay away from trees "

                "and unsecured structures."

            )

        if stats["uv"] >= 8:

            advice.append(

                "Very high UV exposure: use sunscreen and protective clothing."

            )

        elif stats["uv"] >= 6:

            advice.append(

                "High UV exposure: use sunscreen and sunglasses."

            )

        if stats["humidity"] >= 80 and stats["feels_max"] >= 28:

            advice.append(

                "High humidity: reduce your activity intensity "

                "and rest regularly."

            )

        if window.rating is Rating.AVOID:

            advice.append(

                "This activity is not recommended during this period."

            )

        advice.extend(self.activity.tips)

        if not advice:

            advice.append(

                "Conditions look comfortable. Stay hydrated "

                "and check the forecast before leaving."

            )

        return advice

    # ---------------- PACKING CHECKLIST ----------------

    def packing_checklist(self, window: TimeWindow) -> List[str]:

        """Creates a packing checklist based on weather conditions."""

        stats = self._stats(window)

        items = [

            "Water bottle",

            "Fully charged phone",

            "Basic first-aid kit"

        ]

        items.extend(self.activity.base_items)

        if stats["rain"] >= 40:

            items.extend([

                "Umbrella or rain jacket",

                "Waterproof bag"

            ])

        if stats["uv"] >= 6:

            items.extend([

                "Sunscreen (SPF 30+)",

                "Hat or cap",

                "Sunglasses"

            ])

        if stats["feels_max"] >= 30:

            items.extend([

                "Extra drinking water",

                "Electrolyte solution",

                "Cooling towel"

            ])

        if stats["feels_min"] <= 10:

            items.extend([

                "Warm clothing",

                "Gloves"

            ])

        if stats["wind"] >= 30:

            items.extend([

                "Windbreaker",

                "Items to secure lightweight equipment"

            ])

        if stats["humidity"] >= 80:

            items.extend([

                "Quick-dry clothing",

                "Spare clothes"

            ])

        if window.start.hour < 7 or window.end.hour >= 19:

            items.extend([

                "Torch or headlamp",

                "Reflective clothing"

            ])

        # Removes duplicate items while preserving their order

        return list(dict.fromkeys(items))

    # ---------------- MAIN ENTRY POINT ----------------

    def build_plan(

        self,

        forecast: Forecast,

        day: date,

        duration: int = 2,

        start: Optional[time] = None

    ) -> ActivityPlan:

        """Builds a complete outdoor activity recommendation."""

        self._validate_duration(duration)

        if not isinstance(day, date) or isinstance(day, datetime):

            raise InvalidInputError(

                "Please provide a valid activity date."

            )

        if not isinstance(forecast.location, Location):

            raise InvalidInputError(

                "A valid Location object is required."

            )

        # Retrieves available weather forecasts

        available_hours = self.candidate_hours(forecast, day)

        # Evaluates the weather risk for each available hour

        assessments = self.analyzer.assess_hours(

            available_hours

        )

        if not assessments:

            raise WeatherDataError(

                "No weather assessments are available."

            )

        # Selects the requested time or finds the safest window

        if start is not None:

            window = self.window_at(

                assessments,

                start,

                duration

            )

        else:

            window = self.find_best_window(

                assessments,

                duration

            )

        # Collects unique reasons from the selected hours

        reasons = list(dict.fromkeys(

            reason

            for assessment in window.assessments

            for reason in assessment.reasons

        ))

        if not reasons:

            reasons = [

                "No significant weather concerns were detected."

            ]

        # Creates the final activity plan

        return ActivityPlan(

            location=forecast.location,

            activity_name=self.activity.name,

            day=day,

            duration=duration,

            window=window,

            reasons=reasons,

            advice=self.safety_advice(window),

            checklist=self.packing_checklist(window),

            hourly=assessments,

            day_average=self.analyzer.summarize(

                assessments

            )["average"],

            user_chose_time=start is not None

        )
        
