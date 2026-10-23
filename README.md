# Inventory AI Agent

A Django web application for managing warehouse inventory through a conversational AI assistant. The assistant uses Google Gemini to interpret requests and calls inventory tools to read and update records stored in SQLite.

## Features

- List inventory items and check stock quantities and unit prices.
- Add new items and restock existing items.
- Remove units from stock or delete an item entirely.
- Set unit prices or adjust them by a percentage.
- Keep conversation history within a browser session.
- Reset the conversation using **Start over**.

## Technologies

- Python 3.14
- Django
- Google Gen AI SDK
- SQLite
- Docker

Dependency versions are listed in `requirements.txt`.

## Getting Started

Clone the repository and open the project directory:

```powershell
git clone https://github.com/Ritajaf/Lab5-EECE430-RitaAbouFares.git
cd Lab5-EECE430-RitaAbouFares
```

Create a local environment file:

```powershell
Copy-Item .env.example .env
```

Set your Gemini API key in `.env`:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
```

The key must have access to the model configured in `chat/agent.py`. Keep `.env` local; it is excluded from Git and the Docker image.

## Run with Docker

Start Docker Desktop with Linux containers enabled, then build and run the application:

```powershell
docker build -t inventory-agent .
docker run -d --name inventory-agent -p 8000:8000 --env-file .env inventory-agent
```

Open [http://localhost:8000](http://localhost:8000).

The container applies the database migrations automatically before starting the Django development server. It starts with an empty inventory database, separate from any database used outside Docker. Data remains in that container when it is stopped and restarted; removing the container removes its database.

View logs, stop the container, or restart it:

```powershell
docker logs inventory-agent
docker stop inventory-agent
docker start inventory-agent
```

## Run Locally

Install Python 3.14, then run these commands in PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000). The local database is created as `db.sqlite3`.

## Example Requests

- "Add 20 hammers to the inventory."
- "How many hammers are in stock?"
- "Set the price of a hammer to 15.00."
- "Increase the price of hammers by 10%."
- "Remove 3 hammers from stock."
- "List all inventory items."

Use the same item name when referring to an existing record. Item lookups are case-insensitive.

## Project Structure

```text
chat/
  agent.py              Gemini interaction and tool execution
  tools.py              Inventory operations and tool declarations
  models.py             Inventory item model
  views.py              Chat requests and session history
  templates/chat.html   Chat interface
  migrations/           Database schema migrations
  tests.py              Inventory tests
config/                 Django settings and URL configuration
manage.py               Django management commands
Dockerfile              Container build and startup configuration
requirements.txt        Python dependencies
.env.example            Environment configuration template
```

## Tests

With the Python dependencies installed and `.env` configured:

```powershell
.\venv\Scripts\python.exe manage.py test
```
