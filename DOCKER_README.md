# DiagramCraft AI — Docker Setup Guide

## Prerequisites

Your friend's laptop needs **only ONE thing** installed:

- **Docker Desktop** — download from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
  - Available for Windows, Mac, and Linux
  - Docker Compose is included with Docker Desktop

> **That's it!** No Python, Node.js, MongoDB, or LaTeX installation needed.

---

## Quick Start (3 Steps)

### Step 1: Set up the API Key

Copy the example env file and add your Groq API key:

```bash
cp .env.example .env
```

Edit `.env` and replace `your_groq_api_key_here` with your actual key:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

> Get a free Groq API key at [https://console.groq.com/keys](https://console.groq.com/keys)

### Step 2: Build and Start

```bash
docker compose up --build
```

First build will take **10-15 minutes** (downloads LaTeX packages). After that, it starts in seconds.

### Step 3: Open the App

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)

---

## Useful Commands

| Command | Description |
|---------|-------------|
| `docker compose up --build` | Build and start all services |
| `docker compose up -d` | Start in background (detached) |
| `docker compose down` | Stop all services |
| `docker compose logs -f` | View live logs |
| `docker compose logs backend` | View backend logs only |
| `docker compose restart backend` | Restart backend only |

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Docker Network                    │
│                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐  │
│  │ Frontend │───>│ Backend  │───>│   MongoDB    │  │
│  │ (Nginx)  │    │ (FastAPI)│    │              │  │
│  │ Port 3000│    │ Port 8000│    │  Port 27017  │  │
│  └──────────┘    └──────────┘    └──────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

- **Frontend** serves the React app and proxies `/api` + `/output` requests to backend
- **Backend** generates diagrams using Groq AI + LaTeX
- **MongoDB** stores diagram history

---

## Troubleshooting

### "Port already in use"
Stop any local services using ports 3000, 8000, or 27017, or change the ports in `docker-compose.yml`.

### "LaTeX compilation failed"
This is usually an AI generation issue, not a Docker issue. Try regenerating the diagram.

### First build is slow
The backend image downloads LaTeX packages (~500MB). This only happens once — subsequent builds use Docker cache.
