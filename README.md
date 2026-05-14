# AI Guardrail & Proxy Proxy

## Overview
This project demonstrates the "LLM-as-a-Judge" and Guardrail pattern. It acts as a safety middleware layer between an autonomous AI agent and the end user.

## The Problem Solved
Large Language Models are susceptible to prompt injection, jailbreaks, and going off-topic (e.g., a travel bot giving financial advice). A single model cannot reliably generate an answer *and* critique its own safety simultaneously. This architecture uses a secondary, smaller "Judge" model to evaluate the primary model's output before it is ever shown to the user.

## Tech Stack
* **Python 3.10+**
* **Ollama Cloud:** For both the Primary Generator model and the Secondary Judge model.

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