# Runtime Signal Translator

A scenario-based project for translating cloud and runtime security signals into clear technical, operational, and business meaning.

This app is designed to help break down security findings in a way that is useful across different stakeholders, including security leaders, engineers, SRE, DevOps, and customer-facing teams.

## Purpose

The project focuses on helping users answer questions like:

- What does this signal likely mean?
- Why does it matter?
- Who cares most about it?
- What should happen next?
- How can it be explained in business terms?


## What It Does

The app lets you explore predefined scenarios across areas such as:

- Container Runtime
- Kubernetes Behavior
- API Security
- Identity / Access
- Cloud Exposure
- DevOps / CI-CD Context

For each scenario, the app helps translate the signal through four views:

- **Scenario Explorer** — signal, meaning, and impact
- **Persona Lens** — how different stakeholders interpret it
- **Value Translation** — technical risk to business relevance
- **CSM Action Plan** — follow-up questions, next steps, and customer-facing value

<img width="1452" height="1196" alt="image" src="https://github.com/user-attachments/assets/4baae2ab-27bf-4dfc-b09b-34a828f7e34b" />
<img width="1093" height="1053" alt="image" src="https://github.com/user-attachments/assets/9f316e72-6f57-476e-ba87-be2897296107" />
<img width="1094" height="681" alt="image" src="https://github.com/user-attachments/assets/ccc64235-773d-479e-8854-42a9cdd96367" />
<img width="1096" height="623" alt="image" src="https://github.com/user-attachments/assets/e4c8978b-29eb-4ed8-b32d-156a9a7ad039" />




## Why This Project Exists

Security findings are often technically correct but hard to prioritize or explain. This project is meant to show a more structured way to connect runtime and cloud signals to:

- Risk
- Operational impact
- Stakeholder communication
- Customer value

## Use Cases

This project can support:

- Interview preparation
- Customer success storytelling
- Technical account management conversations
- Security-to-business translation practice
- Scenario-based learning



## Tech

- Python
- Streamlit

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
