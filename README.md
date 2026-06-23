# AI Guardrail & Proxy Middleware

## Overview
This project establishes an enterprise-grade "LLM-as-a-Judge" safety layer. Operating as asynchronous middleware between autonomous AI agents and end-users, it intercepts, evaluates, and deterministically routes generated outputs to prevent policy violations, prompt injections, and off-topic domain drift.

## Architectural Paradigm
Large Language Models exhibit structural vulnerabilities when tasked with simultaneous generation and self-critique. This architecture deploys a decoupled, secondary "Judge" model enforcing strict validation matrices before output delivery.

## Tech Stack
* **Python 3.10+** (Asynchronous execution topology)
* **Ollama Cloud/Local:** Core inference engine for both Primary Generator and Secondary Judge models.
* **Pydantic:** Strict configuration and schema enforcement.

## Environment Initialization (Local Development)
1. Clone the repository and establish an isolated virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
## Setup Instructions
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment.
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file and add your API key:
   `OLLAMA_API_KEY=your_api_key_here`

## Usage
Run the guardrail proxy:
`python guardrail.py`