import duckdb

con = duckdb.connect(".dlt/data/dev/logfire_traces.duckdb", read_only=True)

last_trace = con.sql(
    "SELECT trace_id FROM agent_traces.records GROUP BY trace_id ORDER BY MAX(start_timestamp) DESC LIMIT 1"
).fetchone()[0]

total_input_tokens = con.sql(
    "SELECT SUM(attributes__gen_ai_usage_input_tokens) FROM agent_traces.records WHERE trace_id = ?",
    params=[last_trace],
).fetchone()[0]

print(f"Total input tokens for last run ({last_trace}): {total_input_tokens}")
