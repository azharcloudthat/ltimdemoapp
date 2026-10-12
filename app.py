import os

import requests
from flask import Flask, jsonify, render_template, request

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 8

WMO_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime fog",
    51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    56: "Freezing drizzle", 57: "Freezing drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain",
    66: "Freezing rain", 67: "Freezing rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow", 77: "Snow grains",
    80: "Rain showers", 81: "Rain showers", 82: "Violent rain showers",
    85: "Snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with hail",
}

app = Flask(__name__)


def error(message, status):
    return jsonify({"error": message}), status


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/weather")
def weather():
    city = request.args.get("city", "").strip()
    if not 2 <= len(city) <= 100:
        return error("City name must be 2-100 characters.", 400)

    try:
        geo = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=TIMEOUT,
        )
        geo.raise_for_status()
        places = geo.json().get("results")
        if not places:
            return error(f"City '{city}' not found.", 404)
        place = places[0]

        forecast = requests.get(
            FORECAST_URL,
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m,apparent_temperature,"
                "relative_humidity_2m,wind_speed_10m,weather_code",
            },
            timeout=TIMEOUT,
        )
        forecast.raise_for_status()
        current = forecast.json()["current"]
    except (requests.RequestException, ValueError, KeyError):
        app.logger.exception("Open-Meteo request failed")
        return error("Weather service unavailable. Please try again.", 502)

    return jsonify({
        "city": place["name"],
        "country": place.get("country"),
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "description": WMO_CODES.get(current["weather_code"], "Unknown"),
    })


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")

