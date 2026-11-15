# Neura — AI & Technology Academy

A responsive, interactive learning website for a CS101 project. It uses **Python + Flask** for the backend and HTML, CSS, and JavaScript for the frontend.

## Features

- Six short learning modules about AI, machine learning, neural networks, LLMs, prompt engineering, and responsible AI.
- Lesson content loaded from Flask API endpoints.
- Progress tracking saved in the browser with `localStorage`.
- Interactive quiz with server-side answer checking and explanations.
- Mini learning assistant connected to a Python endpoint.
- Responsive layout for desktop, tablet, and mobile.
- Health-check endpoint for deployment platforms.

## Important note about the assistant

The Neura Assistant is a **prepared-response classroom demo**, not a live large language model. The assignment description in the class chat says Python is required for the backend and does not specify that a real LLM API must be connected. If the instructor later requires a live model, the `/api/assistant` route can be connected to an approved LLM provider using a private environment variable. Never put an API key in frontend JavaScript or commit it to GitHub.

## Run locally

You need Python 3.10 or newer.

### 1. Open a terminal in this project folder

```bash
cd cs101_ai_tech_academy
```

### 2. Create and activate a virtual environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install packages

```bash
pip install -r requirements.txt
```

### 4. Start the website

```bash
python app.py
```

Open this address in your browser:

```text
http://127.0.0.1:5000
```

Stop the server with `Ctrl + C`.

## Deploy online with Render

1. Create a GitHub account if you do not already have one.
2. Create a new repository, for example `neura-ai-tech-academy`.
3. Upload the project files to the repository. Do not upload your virtual environment or private API keys.
4. Sign in to Render and choose **New → Web Service**.
5. Connect the GitHub repository.
6. Render should detect `render.yaml`. If it asks for settings, use:
   - Runtime: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
7. Create the service and wait for the deployment to finish.
8. Render will provide a public URL similar to `https://your-service-name.onrender.com`. Use the exact URL shown in your Render dashboard when submitting the project.

The free hosting options and their limits can change. Check the current Render dashboard for available plans and sleep/usage limits.

## Project structure

```text
cs101_ai_tech_academy/
├── app.py
├── requirements.txt
├── Procfile
├── render.yaml
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## Backend routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Render the website |
| `/api/lesson/<lesson_id>` | GET | Return lesson content |
| `/api/quiz` | GET | Return quiz questions without answers |
| `/api/quiz/submit` | POST | Check submitted answers on the server |
| `/api/assistant` | POST | Return a prepared educational explanation |
| `/health` | GET | Health check for hosting |

## AI tools and development process

For an honest project report, list only the tools actually used during your work. Example wording you can adapt:

- ChatGPT: planning the site structure, drafting educational content, and assisting with Python/HTML/CSS/JavaScript code.
- Flask: Python web framework used to build the backend.
- Render: hosting platform used to publish the web application.
- GitHub: source-code repository used for deployment.

Review and test the code yourself before submission, and follow your instructor's rules about disclosing AI assistance.
