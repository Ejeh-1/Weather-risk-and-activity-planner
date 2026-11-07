"""RecommendationEngine: best time window, safety advice and packing checklist."""
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import List, Optional

from analyzer import ActivityRiskAnalyzer, HourAssessment, Rating
from exceptions import InvalidInputError, WeatherDataError
from models import Forecast, Location


@dataclass
class TimeWindow:
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
        rows = [f"{'Time':<6}{'Temp':>6}{'Feels':>7}{'Rain%':>7}{'Wind':>6}{'UV':>4}  {'Rating':<11}Sky"]
        for a in self.hourly:
            h = a.hour
            rows.append(f"{h.time:%H:%M} {h.temperature:>5.0f}°{h.apparent_temp:>6.0f}°{h.rain_probability:>6.0f}%"
                        f"{h.wind_speed:>6.0f}{h.uv_index:>4.0f}  {a.rating.value:<11}{h.description}")
        return "\n".join(rows)

    def to_text(self) -> str:
        label = "Your chosen time" if self.user_chose_time else "Best time"
        lines = [
            f"ACTIVITY PLAN - {self.activity_name} in {self.location.label}",
            f"Date: {self.day:%A, %d %B %Y}",
            f"Verdict: {self.rating.value.upper()}   ({label}: {self.window.label}, {self.duration}h)",
            "", "Why:", *[f"  - {r}" for r in self.reasons],
            "", "Safety advice:", *[f"  - {a}" for a in self.advice],
            "", "Packing checklist:", *[f"  [ ] {c}" for c in self.checklist],
        ]
        return "\n".join(lines)


class RecommendationEngine:
    def __init__(self, analyzer: ActivityRiskAnalyzer):
        self.analyzer = analyzer
        self.activity = analyzer.activity

    # ---- window selection -----------------------------------------------
    def candidate_hours(self, forecast: Forecast, day: date):
        start_h, end_h = self.activity.active_hours
        hours = forecast.daytime_hours(day, start_h, end_h)
        if forecast.local_now and day == forecast.local_now.date():
            cutoff = forecast.local_now.replace(minute=0, second=0, microsecond=0)
            hours = [h for h in hours if h.time >= cutoff]
        if not hours:
            raise WeatherDataError(
                f"No usable hours left for {self.activity.name.lower()} on {day}. Try another date.")
        return hours

    @staticmethod
    def _window_score(chunk: List[HourAssessment]) -> float:
        scores = [a.score for a in chunk]
        return round(0.7 * sum(scores) / len(scores) + 0.3 * max(scores), 1)  # one bad hour still matters

    def find_best_window(self, assessments: List[HourAssessment], duration: int) -> TimeWindow:
        d = max(1, min(duration, len(assessments)))
        best = None
        for i in range(len(assessments) - d + 1):
            chunk = assessments[i:i + d]
            w = TimeWindow(chunk, self._window_score(chunk))
            if best is None or w.score < best.score:    # strict < keeps the earlier window on ties
                best = w
        return best

    def window_at(self, assessments: List[HourAssessment], start: time, duration: int) -> TimeWindow:
        for i, a in enumerate(assessments):
            if a.hour.time.hour == start.hour:
                chunk = assessments[i:i + duration]
                return TimeWindow(chunk, self._window_score(chunk))
        first, last = assessments[0].hour.time.hour, assessments[-1].hour.time.hour
        raise InvalidInputError(f"{start:%H:%M} is outside the available hours ({first:02d}:00-{last:02d}:59).")

    # ---- advice and checklist ---------------------------------------------
    @staticmethod
    def _stats(window: TimeWindow) -> dict:
        hs = [a.hour for a in window.assessments]
        return {
            "feels_max": max(h.apparent_temp for h in hs), "feels_min": min(h.apparent_temp for h in hs),
            "rain": max(h.rain_probability for h in hs), "wind": max(h.wind_speed for h in hs),
            "gust": max(h.wind_gusts for h in hs), "uv": max(h.uv_index for h in hs),
            "humidity": max(h.humidity for h in hs), "storm": any(h.is_thunderstorm for h in hs),
        }

    def safety_advice(self, window: TimeWindow) -> List[str]:
        s, advice = self._stats(window), []
        if s["storm"]:
            advice.append("Thunderstorm expected: do NOT be outdoors. Postpone or move to another day.")
        if s["feels_max"] >= 35:
            advice.append("Extreme heat: take shade breaks every 15-20 minutes and stop if you feel dizzy, "
                          "nauseous or stop sweating (signs of heat exhaustion).")
        elif s["feels_max"] >= 30:
            advice.append("Hot conditions: drink water regularly, wear light clothing and avoid the midday sun.")
        if s["feels_min"] <= 5:
            advice.append("Cold conditions: dress in layers and keep your hands and head covered.")
        if s["rain"] >= 60:
            advice.append("Rain is likely: surfaces will be slippery, so reduce intensity and watch your footing.")
        elif s["rain"] >= 40:
            advice.append("A shower is possible: have a plan to take cover quickly.")
        if s["wind"] >= 40 or s["gust"] >= 60:
            advice.append("Strong wind: stay away from trees, poles and unsecured structures.")
        if s["uv"] >= 8:
            advice.append("Very high UV: apply sunscreen every 2 hours and cover up.")
        elif s["uv"] >= 6:
            advice.append("High UV: use sunscreen and sunglasses.")
        if s["humidity"] >= 80 and s["feels_max"] >= 28:
            advice.append("Humid air slows sweat cooling: ease the pace and rest more often.")
        if window.rating is Rating.AVOID:
            advice.append("Overall this is not recommended. Pick another day or time if you can.")
        advice.extend(self.activity.tips)
        if len(advice) == len(self.activity.tips):
            advice.insert(0, "Conditions look comfortable. Stay hydrated and recheck the forecast before leaving.")
        return advice

    def packing_checklist(self, window: TimeWindow) -> List[str]:
        s = self._stats(window)
        items = ["Water bottle", "Fully charged phone", "Basic first-aid kit"] + list(self.activity.base_items)
        if s["rain"] >= 40:
            items += ["Umbrella or rain jacket", "Waterproof bag for phone and valuables"]
        if s["uv"] >= 6:
            items += ["Sunscreen (SPF 30+)", "Hat or cap", "Sunglasses"]
        if s["feels_max"] >= 30:
            items += ["Extra drinking water", "Electrolyte / oral rehydration salts", "Cooling towel"]
        if s["feels_min"] <= 10:
            items += ["Warm layer", "Gloves"]
        if s["wind"] >= 30:
            items += ["Windbreaker", "Weights or pegs to secure light items"]
        if s["humidity"] >= 80:
            items += ["Quick-dry clothing", "Spare change of clothes"]
        if window.start.hour < 7 or window.end.hour >= 19:
            items += ["Torch or headlamp", "Reflective gear"]
        return list(dict.fromkeys(items))          # remove duplicates, keep order

    # ---- main entry point --------------------------------------------------
    def build_plan(self, forecast: Forecast, day: date, duration: int = 2,
                   start: Optional[time] = None) -> ActivityPlan:
        assessments = self.analyzer.assess_hours(self.candidate_hours(forecast, day))
        window = (self.window_at(assessments, start, duration) if start
                  else self.find_best_window(assessments, duration))
        worst = max(window.assessments, key=lambda a: a.score)
        reasons = worst.reasons or ["No significant weather concerns in this window."]
        return ActivityPlan(
            location=forecast.location, activity_name=self.activity.name, day=day,
            duration=len(window.assessments), window=window, reasons=reasons,
            advice=self.safety_advice(window), checklist=self.packing_checklist(window),
            hourly=assessments, day_average=self.analyzer.summarize(assessments)["average"],
            user_chose_time=start is not None,
        )
