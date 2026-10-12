import unittest
from unittest.mock import MagicMock, patch

import requests

from app import app


class WeatherAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_renders_dashboard(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"LTIMindtree Weather Dashboard", response.data)

    @patch("app.requests.get")
    def test_rejects_invalid_city_names(self, get):
        for city in ("", "A", "x" * 101):
            with self.subTest(city_length=len(city)):
                response = self.client.get("/weather", query_string={"city": city})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    response.get_json(),
                    {"error": "City name must be 2-100 characters."},
                )

        get.assert_not_called()

    @patch("app.requests.get")
    def test_returns_not_found_when_city_has_no_geocoding_results(self, get):
        geocoding_response = MagicMock()
        geocoding_response.json.return_value = {"results": []}
        get.return_value = geocoding_response

        response = self.client.get("/weather", query_string={"city": "Atlantis"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "City 'Atlantis' not found."})
        get.assert_called_once()

    @patch("app.requests.get")
    def test_returns_current_weather_for_city(self, get):
        geocoding_response = MagicMock()
        geocoding_response.json.return_value = {
            "results": [{"name": "London", "country": "United Kingdom",
                         "latitude": 51.5, "longitude": -0.12}]
        }
        forecast_response = MagicMock()
        forecast_response.json.return_value = {
            "current": {
                "temperature_2m": 14.2,
                "apparent_temperature": 13.5,
                "relative_humidity_2m": 72,
                "wind_speed_10m": 8.1,
                "weather_code": 61,
            }
        }
        get.side_effect = [geocoding_response, forecast_response]

        response = self.client.get("/weather", query_string={"city": " London "})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {
                "city": "London",
                "country": "United Kingdom",
                "temperature": 14.2,
                "feels_like": 13.5,
                "humidity": 72,
                "wind_speed": 8.1,
                "description": "Light rain",
            },
        )
        self.assertEqual(get.call_count, 2)
        self.assertEqual(get.call_args_list[0].kwargs["params"]["name"], "London")

    @patch("app.requests.get")
    def test_returns_502_when_weather_service_fails(self, get):
        get.side_effect = requests.Timeout

        response = self.client.get("/weather", query_string={"city": "London"})

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            response.get_json(),
            {"error": "Weather service unavailable. Please try again."},
        )


if __name__ == "__main__":
    unittest.main()