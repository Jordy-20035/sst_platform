#!/bin/bash

set -e

# Root structure
mkdir -p sst_platform/{backend/app/{core,db,models,schemas,crud,api/v1/endpoints,services,utils,tests},client/src/{pages,components,services,styles},data/seed,docs,scripts}

# .gitignore
cat > sst_platform/.gitignore <<EOL
__pycache__/
*.pyc
*.pyo
*.pyd
*.db
*.sqlite3
.venv/
node_modules/
.DS_Store
.env
EOL

# README
cat > sst_platform/README.md <<EOL
# SST Platform

Modern digital web platform for Smolensk Traffic Management Center.

## How to run
See docs/architecture.md for details.
EOL

# Requirements
cat > sst_platform/requirements.txt <<EOL
fastapi
uvicorn[standard]
SQLAlchemy
pydantic
python-dotenv
passlib[bcrypt]
PyJWT
alembic
requests
pytest
EOL

# docker-compose.yml
cat > sst_platform/docker-compose.yml <<EOL
version: '3.9'
services:
  backend:
    build:
      context: ./backend
      dockerfile: ../Dockerfile.backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
  frontend:
    build:
      context: ./client
      dockerfile: ../Dockerfile.frontend
    ports:
      - "3000:3000"
    volumes:
      - ./client:/app
EOL

# Dockerfiles
cat > sst_platform/Dockerfile.backend <<EOL
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOL

cat > sst_platform/Dockerfile.frontend <<EOL
FROM node:18-alpine
WORKDIR /app
COPY client/package*.json ./
RUN npm install
COPY client/ ./
CMD ["npm", "run", "dev", "--", "--host"]
EOL

# Backend starter files
cat > sst_platform/backend/app/main.py <<EOL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import router as api_router

app = FastAPI(title="SST Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

app.include_router(api_router, prefix="/api/v1")
EOL

cat > sst_platform/backend/app/api/v1/router.py <<EOL
from fastapi import APIRouter
from .endpoints import incidents

router = APIRouter()
router.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
EOL

cat > sst_platform/backend/app/api/v1/endpoints/incidents.py <<EOL
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_incidents():
    return [{"id": 1, "location": "Main St", "status": "active"}]
EOL

# Frontend starter files
cat > sst_platform/client/package.json <<EOL
{
  "name": "sst-platform-client",
  "version": "0.0.1",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "chart.js": "^4.0.0",
    "leaflet": "^1.9.4"
  }
}
EOL

cat > sst_platform/client/index.html <<EOL
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SST Platform</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
EOL

cat > sst_platform/client/src/main.jsx <<EOL
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOL

cat > sst_platform/client/src/App.jsx <<EOL
import React from "react";

function App() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">SST Platform</h1>
      <p>Welcome to the demo platform.</p>
    </div>
  );
}

export default App;
EOL

# Docs
cat > sst_platform/docs/architecture.md <<EOL
# Architecture

- Backend: FastAPI (Python)
- Frontend: React + Vite + Tailwind
- Database: SQLite (dev), PostgreSQL (future)
- Realtime: SSE
EOL

cat > sst_platform/docs/api_spec.md <<EOL
# API Spec

- GET /api/v1/incidents — list incidents
- POST /api/v1/incidents — create incident
- GET /api/v1/incidents/{id} — get incident by id
EOL

# Demo data
cat > sst_platform/data/seed/demo_incidents.csv <<EOL
id,location,status
1,Main St,active
2,Central Ave,resolved
EOL

# Seed DB helper
cat > sst_platform/scripts/seed_db.py <<EOL
print("Seeding demo data... (implement later)")
EOL

echo "Scaffold complete!"
