# Agentic AI Multimodal RAG Chatbot

An enterprise-grade Agentic Retrieval-Augmented Generation (RAG) system powered by **LangGraph**, **Hugging Face**, **Deepgram**, and **Flask**, with workflow automation orchestrated via **n8n** and containerized with **Docker**.

Unlike traditional static RAG pipelines, this system implements an autonomous multi-agent state machine that rewrites ambiguous queries, retrieves contextual knowledge, evaluates factual groundedness, and mitigates hallucinations through self-correcting routing loops.

## Architecture Overview

```text
User Query / Multimodal Document
        |
  +-----+---------------------+
  |                           |
Upload                    Chat Query
  |                           |
Deepgram / PyPDF       Query Rewriter
  |                           |
Ingestion              Retriever & Grader
                              |
                         Generator Agent
                              |
                       Hallucination Check
                         /            \
                   Grounded       Hallucinated
                       |                |
                 Deliver API       Retry rewriter
                       |             (max 2 attempts)
                  n8n webhook
```

## Core Capabilities

- **4+ Autonomous AI Agents (LangGraph):** query rewriting, retrieval and grading, constrained generation, and hallucination checking with retry routing.
- **Multimodal Ingestion:** native parsing for `.pdf`, `.docx`, `.csv`, and `.txt`, plus Deepgram Nova-2 transcription for `.mp3`, `.wav`, and `.m4a` audio.
- **External Workflow Automation:** n8n webhook dispatch for notifications and downstream pipelines.
- **Containerized Infrastructure:** Flask and n8n services orchestrated with Docker Compose and health checks.

## Tech Stack

| Domain | Technology |
|---|---|
| **Orchestration** | LangChain, LangGraph |
| **Embeddings & LLM** | Hugging Face Transformers, Sentence-Transformers |
| **Audio Processing** | Deepgram Nova-2 SDK |
| **Backend Framework** | Flask (Python 3.11) |
| **Automation** | n8n |
| **Containerization** | Docker, Docker Compose |
| **Document Parsers** | PyPDF, python-docx, Pandas |

## Project Structure

```text
agentic-rag-chatbot/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── app.py
├── src/
│   ├── graph/
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── workflow.py
│   ├── ingestion/
│   │   ├── audio_service.py
│   │   └── parsers.py
│   └── integrations/
│       └── n8n_client.py
└── tests/
```

## Getting Started

### Prerequisites

- [Git](https://git-scm.com/)
- [Docker & Docker Compose](https://www.docker.com/)
- Python 3.11+ for local execution

### Clone and Configure

```bash
git clone https://github.com/<YOUR-USERNAME>/agentic-rag-chatbot.git
cd agentic-rag-chatbot
cp .env.example .env
```

Populate `.env` with your credentials:

```ini
HUGGINGFACEHUB_API_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxx"
DEEPGRAM_API_KEY="your_deepgram_key"
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxx"
N8N_WEBHOOK_URL="http://localhost:5678/webhook/rag-events"
```

## Running the Application

### Docker Compose

```bash
docker compose up --build -d
docker compose ps
```

- Flask REST API: `http://localhost:5000`
- n8n Automation Console: `http://localhost:5678`

### Local Virtual Environment

```bash
python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

## API Documentation

### Ingest a Multimodal File

`POST /api/upload` accepts `multipart/form-data` with a `file` field.

```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@meeting_audio.mp3"
```

Example response:

```json
{
  "char_count": 4210,
  "document_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "filename": "meeting_audio.mp3",
  "format": ".mp3",
  "message": "File processed and indexed successfully",
  "status": "success"
}
```

### Multi-Agent Chat Query

`POST /api/chat` accepts JSON and runs the LangGraph pipeline:

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What were the key takeaways from the Q3 roadmap audio meeting?",
    "session_id": "session_101"
  }'
```

Example response:

```json
{
  "hallucination_evaluation": "grounded",
  "optimized_query": "Key concepts, facts, and context for: What were the key takeaways from the Q3 roadmap audio meeting?",
  "query": "What were the key takeaways from the Q3 roadmap audio meeting?",
  "response": "Based on retrieved sources, here is the synthesized answer...",
  "retrieved_context": ["Verified context chunk 1...", "Verified context chunk 2..."],
  "session_id": "session_101",
  "total_attempts": 1
}
```

## License

Distributed under the MIT License. See `LICENSE` for more information.