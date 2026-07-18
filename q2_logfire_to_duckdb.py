import os

import dlt
import requests
from dotenv import load_dotenv

load_dotenv()

LOGFIRE_QUERY_URL = "https://logfire-us.pydantic.dev/v2/query"


@dlt.resource(name="records", write_disposition="replace")
def logfire_records():
    """Pull all span/trace records from the Logfire Query API."""
    token = os.getenv("LOGFIRE_READ_TOKEN")
    response = requests.post(
        LOGFIRE_QUERY_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
        json={
            "sql": "SELECT * FROM records",
            "min_timestamp": "1970-01-01T00:00:00Z",
            "limit": 10000,
        },
        timeout=30,
    )
    response.raise_for_status()
    yield response.json()["data"]


@dlt.source
def logfire_source():
    return logfire_records()


def main() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="logfire_traces",
        destination="duckdb",
        dataset_name="agent_traces",
    )
    load_info = pipeline.run(logfire_source())
    print(load_info)


if __name__ == "__main__":
    main()
