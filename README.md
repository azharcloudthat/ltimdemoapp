# Kyndryl Weather Dashboard

A Flask app that looks up a city and displays its current weather. It uses the Open-Meteo geocoding and forecast APIs; no API key is required.

## Run locally with in your PC/Laptop

You need Python 3.9 or later.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

On Windows, activate the virtual environment with `.venv\Scripts\activate`. Open <http://127.0.0.1:5000> and search for a city.

The weather endpoint is also available directly at `/weather?city=London`.

## Deploy to Azure App Service

You need an Azure subscription and the [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed. Run these commands from the project directory:

```bash
az login
az group create --name rg-weather-dashboard --location eastus
az webapp up \
  --name <globally-unique-app-name> \
  --resource-group rg-weather-dashboard \
  --location eastus \
  --runtime "PYTHON:3.12" \
  --sku B1
az webapp config set \
  --resource-group rg-weather-dashboard \
  --name <globally-unique-app-name> \
  --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
```

Replace `<globally-unique-app-name>` with a unique name containing only letters, numbers, or hyphens. App Service deploys the project and installs the packages listed in `requirements.txt`. The Gunicorn startup command serves the Flask application in `app.py`.

Open `https://<globally-unique-app-name>.azurewebsites.net` to use the deployed app. To inspect application logs, run:

```bash
az webapp log tail --resource-group rg-weather-dashboard --name <globally-unique-app-name>
```
