# Sprout AI: Multi-Agent Parenting Assistant 👶🤖

Sprout AI is an advanced Multi-Agent system designed to help parents manage complex schedules and tasks. It leverages **Gemini 2.5 Flash** to coordinate between different agents and tools.

## 🚀 Project Overview
- **Core Model:** Gemini 2.5 Flash (Vertex AI)
- **Deployment:** Google Cloud Run (Serverless)
- **Database:** Google Cloud Firestore (NoSQL)
- **Architecture:** Primary-Sub Agent Orchestration

## ✨ Key Features
- **Multi-Agent Coordination:** A Primary Coordinator agent manages intent and delegates tasks to specialized sub-agents.
- **Conflict Detection:** Automatically checks database for schedule overlaps before saving.
- **Bulk Execution:** Handles complex natural language commands like "Clear all my tasks."
- **Persistent Storage:** Real-time data synchronization with Firestore.

## 🛠️ Technical Implementation
- **Function Calling:** Used for seamless interaction between the LLM and Python tools.
- **Model Context Protocol (MCP):** Implemented for structured tool communication.
- **API-Based:** Fully containerized Flask application.

## 🔗 Project Links
- **Live Demo (Cloud Run):** [YAHAN APNA CLOUD RUN LINK PASTE KARO]
- **Video Demo:** [YAHAN APNA VIDEO LINK YA GOOGLE DRIVE LINK PASTE KARO]

## 📂 Structure
- `app.py`: Main Orchestrator and Agent logic.
- `database.py`: Firestore tools and database connection.
- `requirements.txt`: Project dependencies.
