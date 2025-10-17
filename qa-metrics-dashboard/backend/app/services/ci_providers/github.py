# Minimal parser stub for potential future ingestion of GitHub Actions job metrics.
# You can expand this to verify webhook signatures and map job/timing data to Metric records.

def parse_workflow_run(payload: dict) -> list[dict]:
    # Returns list of MetricPoint-like dicts
    out: list[dict] = []
    run = payload.get("workflow_run", {})
    pipeline_name = run.get("name", "github-actions")
    duration = run.get("run_duration_ms")
    if duration is not None:
        out.append({
            "pipeline": pipeline_name,
            "name": "ci.duration_ms",
            "ts": run.get("updated_at"),
            "value": float(duration)
        })
    return out
