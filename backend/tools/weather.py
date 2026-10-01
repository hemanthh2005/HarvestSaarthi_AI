"""
HarvestSaarthi AI - weather_risk_tool
"""

from backend.models.schemas import WeatherRiskData
from backend.data.repository import DataRepository

repo = DataRepository()


def weather_risk_tool(location: str, date_range: str = "Next 48 Hours") -> WeatherRiskData:
    """Evaluates weather risk for transit and harvest handling."""
    return repo.get_weather_risk(location)
