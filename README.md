# Agentic Azure App Service app with LangGraph and Foundry Agent Service

This repository demonstrates how to build a modern FastAPI web application that integrates with both Foundry Agent Service and LangGraph agents. It provides a simple CRUD task list and two interactive chat agents.

## Getting Started

See [Tutorial: Build an agentic web app in Azure App Service with LangGraph or Azure AI Foundry Agent Service (Python)](https://learn.microsoft.com/azure/app-service/tutorial-ai-agent-web-app-langgraph-foundry-python).

## Features

- **Task List**: Simple CRUD web app application.
- **LangGraph Agent**: Chat with an agent powered by LangGraph.
- **Foundry Agent Service**: Chat with an agent powered by Foundry Agent Service.
- **OpenAPI Schema**: Enables integration with Foundry Agent Service.

## Project Structure

```
.devcontainer/
└── devcontainer.json            # Dev container configuration for VS Code
infra/
├── main.bicep                   # Bicep IaC template
├── main.parameters.json         # Parameters for Bicep deployment
public/
└── index.html                   # React frontend
src/
├── __init__.py
├── app.py                       # Main FastAPI application
├── azure.yaml                   # Azure Developer CLI config
├── agents/                      # AI agent implementations
│   ├── __init__.py
│   ├── foundry_task_agent.py    # Foundry agent
│   └── langgraph_task_agent.py  # LangGraph agent
├── models/                      # Pydantic models for data validation
│   └── __init__.py
├── routes/                      # API route definitions
│   ├── __init__.py
│   └── api.py                   # Task and chat endpoints
└── services/                    # Business logic services
    ├── __init__.py
    └── task_service.py          # Task CRUD operations with SQLite
tasks.db                         # SQLite database file
requirements.txt                 # Python dependencies
README.md                        # Project documentation
```

### Quick runtime checks

- Create a `.env` from the supplied template and populate Azure OpenAI values:
```
cp .env.example .env
# Edit .env to set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT_NAME
```

- `.env.example` contains:
```
AZURE_OPENAI_ENDPOINT=https://<your-openai-resource>.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=<your-deployment-name>
# Optional (service principal):
# AZURE_CLIENT_ID=
# AZURE_CLIENT_SECRET=
# AZURE_TENANT_ID=
PORT=3000
```

- Start server (uses virtual env `./venv` if you created it):
```
./venv/bin/uvicorn src.app:app --host 0.0.0.0 --port 3000
```

- Check initialization logs for LangGraph messages (look for `LangGraph Task Agent initialized successfully` or `Azure OpenAI configuration missing for LangGraph agent`):
```
tail -n 100 server.log
```

- Health check endpoint (added):
```
curl -sS http://localhost:3000/health | jq .
```

- Run integration tests locally (uses a mocked LangGraph agent):
```
pytest -q
```

- GitHub Actions CI (added): `.github/workflows/ci.yml` — installs dependencies and runs tests on push/pull-request to `main`.

- Test the LangGraph chat endpoint:
```
curl -sS -X POST http://localhost:3000/api/chat/langgraph \
  -H "Content-Type: application/json" \
  -d '{"message":"Create a task named Test Task","sessionId":"session-1"}' | jq .
```

- If agents are configured, you can also use the OpenAPI UI at `/docs` to call `/api/chat/langgraph` or `/api/chat/foundry`.