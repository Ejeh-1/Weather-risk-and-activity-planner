from dataclasses import dataclass
from enum import Enum
from typing import List

@dataclass
class ActivityProfile:
    name: str
    active_hours: tuple
    max_temp: float
    min_temp: float
    max_rain: float
    max_wind: float
    max_humidity: float
    tips: List[str]
    base_items: List[str]

ACTIVITY_PROFILES = {
    "football": ActivityProfile(
    "Football",
    (6, 19),
    32,
    10,
    40,
    30,
    85,
    [
    "Warm up properly before playing."
    "Take regular water breaks."
    ],
    [
    "Football boots",
    "Sportswear",
    "Towel"
    ]
    ),

    "jogging": ActivityProfile(
        "Jogging",
        (5, 19),
        30,
        5,
        50,
        35,
        80,
        [
            "Start with a gentle warm-up.",
            "Avoid overexertion."
        ],
        [
            "Running shoes",
            "Comfortable sportswear"
        ]
    ),
    "farming": ActivityProfile(
        "Farming",
        (6, 18),
        35,
        10,
        60,
        40,
        90,
        [
            "Wear protective clothing.",
            "Take regular shade breaks."
        ],
        [
            "Farm tools",
            "Protective gloves",
            "Boots"
        ]
    ),
    "picnic": ActivityProfile(
        "Picnic",
        (7, 19),
        33,
        15,
        20,
        25,
        85,
        [
            "Choose a shaded location.",
            "Keep food properly covered."
        ],
        [
            "Picnic mat",
            "Food",
            "Insect repellent"
        ]
    ),
    "travelling": ActivityProfile(
        "Travelling",
        (5, 21),
        38,
        0,
        60,
        50,
        95,
        [
            "Check your route before departure.",
            "Carry emergency supplies."
        ],
        [
            "Travel documents",
            "Power bank",
            "Travel bag"
        ]
    ),
    "outdoor events": ActivityProfile(
        "Outdoor Events",
        (7, 21),
        34,
        12,
        30,
        30,
        85,
        [
            "Provide shade for attendees.",
            "Keep drinking water available."
        ],
        [
            "Event supplies",
            "First-aid kit"
        ]
    )

    }

class Rating(Enum):
    SAFE = "Safe"
    MANAGEABLE = "Manageable"
    RISKY = "Risky"
    AVOID = "Avoid"

    @classmethod
    def from_score(cls, score):
          if score <= 1:
              return cls.SAFE
         elif score <= 3:
            return cls.MANAGEABLE
         elif score <= 5:
              return cls.RISKY
         else:
             return cls.AVOID

    @dataclass
    class HourAssessment:
         hour: object
         score: float
         reasons: List[str]

          @property
          def rating(self):
              return Rating.from_score(self.score)
class ActivityRiskAnalyzer:

    def __init__(self, activity="football"):

        if isinstance(activity, ActivityProfile):

            self.activity = activity

        else:

            activity_key = str(activity).strip().lower()

            if activity_key not in ACTIVITY_PROFILES:

                raise ValueError(

                    f"Unsupported activity: {activity}. "

                    f"Available activities: "

                    f"{', '.join(ACTIVITY_PROFILES)}"

                )

            self.activity = ACTIVITY_PROFILES[activity_key]

    def assess_hour(self, hour):

        score = 0

        reasons = []

        limits = self.activity

        if hour.temperature is None or hour.apparent_temp is None:

            raise ValueError("Temperature data is missing.")

        if hour.apparent_temp > limits.max_temp:

            score += 2

            reasons.append("Temperature is too high for this activity.")

        if hour.apparent_temp < limits.min_temp:

            score += 2

            reasons.append("Temperature is too low for this activity.")

        if hour.rain_probability is None:

            raise ValueError("Rain probability data is missing.")

        if hour.rain_probability > limits.max_rain:

            score += 2

            reasons.append("High probability of rainfall.")

        if hour.wind_speed is None or hour.wind_gusts is None:

            raise ValueError("Wind data is missing.")

        if hour.wind_speed > limits.max_wind:

            score += 2

            reasons.append("Wind speed is too high.")

        if hour.wind_gusts >= 60:

            score += 2

            reasons.append("Dangerous wind gusts expected.")

        if hour.humidity is not None:

            if hour.humidity > limits.max_humidity:

                score += 1

                reasons.append("Humidity is too high.")

        if hour.uv_index is not None:

            if hour.uv_index >= 8:

                score += 1

                reasons.append("Very high UV exposure expected.")

        if hour.is_thunderstorm:

            score += 5

            reasons.append("Thunderstorm conditions expected.")

        return HourAssessment(

            hour=hour,

            score=score,

            reasons=reasons

        )

    def assess_hours(self, hours):

        return [

            self.assess_hour(hour)

            for hour in hours

        ]

    @staticmethod

    def summarize(assessments):

        if not assessments:

            return {"average": 0.0}

        average = sum(

            assessment.score

            for assessment in assessments

        ) / len(assessments)

        return {

            "average": round(average, 1)

        }
    
