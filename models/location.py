from dataclasses import dataclass

@dataclass

class Location:

    name: str

    country: str = ""

    latitude: float = 0.0

    longitude: float = 0.0

    timezone: str = "auto"

    @property

    def label(self):

        if self.country:

            return f"{self.name}, {self.country}"

        return self.name
