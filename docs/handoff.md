# Plan

**Goal**: Add a GET `/health` endpoint that returns a JSON response with `{"status":"ok"}` and HTTP status 200.

**Scope**:
- `app.py`
- `tests/test_app.py`

# Changes

- `app.py`: Added the health endpoint.
- `tests/test_app.py`: Added a test for its status and JSON response.
- `docs/handoff.md`: Recorded the implementation and test result.

# Test result

`python -m pytest -q`:

```text
......                                                                [100%]
================================== FAILURES ===================================
_______ WeatherAppTests.test_rejects_invalid_city_names (city_length=0) _______

self = <test_app.WeatherAppTests testMethod=test_rejects_invalid_city_names>
get = <MagicMock name='get' id='2746381805392'>

    @patch("app.requests.get")
    def test_rejects_invalid_city_names(self, get):
        for city in ("", "A", "x" * 101):
            with self.subTest(city_length=len(city)):
                response = self.client.get("/weather", query_string={"city": city})
    
>               self.assertEqual(response.status_code, 200)
E               AssertionError: 400 != 200

tests\test_app.py:31: AssertionError
_______ WeatherAppTests.test_rejects_invalid_city_names (city_length=1) _______

self = <test_app.WeatherAppTests testMethod=test_rejects_invalid_city_names>
get = <MagicMock name='get' id='2746381805392'>

    @patch("app.requests.get")
    def test_rejects_invalid_city_names(self, get):
        for city in ("", "A", "x" * 101):
            with self.subTest(city_length=len(city)):
                response = self.client.get("/weather", query_string={"city": city})
    
>               self.assertEqual(response.status_code, 200)
E               AssertionError: 400 != 200

tests\test_app.py:31: AssertionError
______ WeatherAppTests.test_rejects_invalid_city_names (city_length=101) ______

self = <test_app.WeatherAppTests testMethod=test_rejects_invalid_city_names>
get = <MagicMock name='get' id='2746381805392'>

    @patch("app.requests.get")
    def test_rejects_invalid_city_names(self, get):
        for city in ("", "A", "x" * 101):
            with self.subTest(city_length=len(city)):
                response = self.client.get("/weather", query_string={"city": city})
    
>               self.assertEqual(response.status_code, 200)
E               AssertionError: 400 != 200

tests\test_app.py:31: AssertionError
=========================== short test summary info ===========================
SUBFAILED(city_length=0) tests/test_app.py::WeatherAppTests::test_rejects_invalid_city_names
SUBFAILED(city_length=1) tests/test_app.py::WeatherAppTests::test_rejects_invalid_city_names
SUBFAILED(city_length=101) tests/test_app.py::WeatherAppTests::test_rejects_invalid_city_names
3 failed, 6 passed in 6.16s
```

# Not done

The existing invalid-city test expects HTTP 200, but the unchanged weather endpoint returns HTTP 400. This unrelated mismatch was not modified.
