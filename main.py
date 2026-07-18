import time
from typing import Literal

from dotenv import load_dotenv
from pydantic_ai.exceptions import ModelHTTPError

load_dotenv()

from agent import SearchDeps, faq_agent, get_ollama_agent
from ingest import build_index, load_faq_data


def build_search_deps() -> SearchDeps:
    """Build search dependencies with FAQ index."""
    return SearchDeps(index=build_index(load_faq_data()))


def ask_question(question: str, deps: SearchDeps, agent, max_retries: int = 3) -> str:
    """Ask a question with retry on rate limit."""
    for attempt in range(max_retries):
        try:
            return agent.run_sync(question, deps=deps).output
        except ModelHTTPError as e:
            if e.status_code == 429 and attempt < max_retries - 1:
                wait_time = 60 * (attempt + 1)
                print(f"Rate limit hit. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise


def main(
    questions: list[str] | None = None,
    model: Literal["openrouter", "ollama"] = "ollama",
    delay: float = 5.0,
) -> None:
    """Run FAQ agent with questions."""
    questions = questions or ["I just discovered the course. Can I join it?"]
    agent = get_ollama_agent() if model == "ollama" else faq_agent
    deps = build_search_deps()

    # Run the agent a few times with different questions and open your project on Logfire to see the traces.
    for i, question in enumerate(questions):
        print(f"Question: {question}")
        print(f"Answer: {ask_question(question, deps, agent)}\n")

        if model == "openrouter" and i < len(questions) - 1:
            time.sleep(delay)


if __name__ == "__main__":
    course_questions = [
        "Hey, I didn't manage to register before the cohort started. Can I still join and submit the homework assignments?",
        "If I take this course at my own pace instead of following a live cohort, will I still get a certificate at the end?",
        "Where exactly can I find the deadlines for each homework? Are they shown in my local timezone?",
        "How is the 2024 cohort different from the 2023 one? Is it worth starting with the older version if I want to go faster?",
        "I'm a bit lost on where to begin. Should I start with the videos, the GitHub repo, or jump straight into the homeworks?",
    ]
    main(course_questions, model="ollama")
