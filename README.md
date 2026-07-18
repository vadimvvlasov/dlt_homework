# dlt Workshop Homework — LLM Zoomcamp 2026

Homework for the [dlt Workshop](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/workshops/dlt/homework.md).

The task: take the FAQ agent from Module 1, instrument it with Pydantic Logfire for observability, pull the trace data with dlt into DuckDB, and analyze it.

## Stack

- **Agent**: Pydantic AI with local Ollama (`granite4.1:8b`)
- **Observability**: Pydantic Logfire
- **Data pipeline**: dlt + DuckDB

## Project structure

| File | Purpose |
|---|---|
| `agent.py` | FAQ agent definition, supports OpenRouter and Ollama |
| `ingest.py` | Downloads FAQ data and builds minsearch index |
| `main.py` | General-purpose runner for multiple questions |
| `q1_logfire.py` | Runs the agent with Logfire instrumentation (Question 1) |

## Setup

```bash
uv init
uv add openai minsearch requests python-dotenv pydantic-ai logfire
uv add "dlt[duckdb]"
```

Add to `.env` (make sure `.env` is in `.gitignore`):

```
OPENAI_API_KEY=sk-YOUR_KEY_HERE
LOGFIRE_TOKEN=<your write token>
LOGFIRE_READ_TOKEN=<your read token>
```

This project uses local Ollama instead of OpenAI. Additional `.env` keys required:

```
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

---

## Answers

### Question 1 — Spans per agent run

> For the query "How do I run Ollama locally?", how many spans does a single agent run produce?

Script: [q1_logfire.py](q1_logfire.py)

```bash
uv run python q1_logfire.py
```

**Answer: 5**

(q1.png)
---

### Question 2 — Tables in DuckDB

> How many tables did dlt create in the `agent_traces` schema?

```sql
SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'agent_traces';
```

**Answer:** <!-- TODO: fill in after running dlt pipeline -->

---

### Question 3 — Input token usage

> What is the range of total input token usage for the agent run from Q1?

```sql
-- sum gen_ai.usage.input_tokens across all LLM calls within the trace
```

**Answer:** <!-- TODO: fill in after querying DuckDB -->
