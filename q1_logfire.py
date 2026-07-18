import logfire
from dotenv import load_dotenv

load_dotenv()

# Instrument the agent with Logfire (Question 1)
logfire.configure()
logfire.instrument_pydantic_ai()

from agent import SearchDeps, get_ollama_agent
from ingest import build_index, load_faq_data


def main() -> None:
    agent = get_ollama_agent()
    deps = SearchDeps(index=build_index(load_faq_data()))

    question = "How do I run Ollama locally?"
    print(f"Question: {question}")
    result = agent.run_sync(question, deps=deps)
    print(f"Answer: {result.output}")


if __name__ == "__main__":
    main()
