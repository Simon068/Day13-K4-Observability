from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.cli import configure_utf8_stdio


REQUIRED_PANEL_IDS = frozenset(
    {"latency", "traffic", "errors", "cost", "tokens", "quality"}
)
REQUIRED_PANEL_FIELDS = (
    "title",
    "source",
    "events",
    "fields",
    "aggregations",
    "query",
    "unit",
    "threshold",
)


class DashboardConfigError(ValueError):
    pass


def load_dashboard_config(path: Path) -> dict:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DashboardConfigError(f"Dashboard config not found: {path}") from exc
    except yaml.YAMLError as exc:
        raise DashboardConfigError(f"Dashboard config is not valid YAML: {exc}") from exc

    dashboard = payload.get("dashboard") if isinstance(payload, dict) else None
    if not isinstance(dashboard, dict):
        raise DashboardConfigError("Missing 'dashboard' object")
    if dashboard.get("schema_version") != 1:
        raise DashboardConfigError("'dashboard.schema_version' must equal 1")
    if dashboard.get("time_range_minutes") != 60:
        raise DashboardConfigError("'dashboard.time_range_minutes' must equal 60")
    refresh_seconds = dashboard.get("refresh_seconds")
    if not isinstance(refresh_seconds, int) or not 15 <= refresh_seconds <= 30:
        raise DashboardConfigError("'dashboard.refresh_seconds' must be between 15 and 30")

    panels = dashboard.get("panels")
    if not isinstance(panels, list) or len(panels) != 6:
        raise DashboardConfigError("Dashboard must contain exactly 6 panels")
    panel_ids = {
        panel.get("id") for panel in panels if isinstance(panel, dict) and panel.get("id")
    }
    if panel_ids != REQUIRED_PANEL_IDS:
        missing = ", ".join(sorted(REQUIRED_PANEL_IDS - panel_ids)) or "none"
        extra = ", ".join(sorted(panel_ids - REQUIRED_PANEL_IDS)) or "none"
        raise DashboardConfigError(
            f"Invalid panel IDs; missing: {missing}; unsupported: {extra}"
        )

    for panel in panels:
        if not isinstance(panel, dict):
            raise DashboardConfigError("Each dashboard panel must be a YAML object")
        panel_id = panel["id"]
        for field in REQUIRED_PANEL_FIELDS:
            if panel.get(field) in (None, "", []):
                raise DashboardConfigError(f"Missing or empty: {panel_id}.{field}")
        if not all(isinstance(panel[field], list) for field in ("events", "fields", "aggregations")):
            raise DashboardConfigError(
                f"'{panel_id}.events/fields/aggregations' must be lists"
            )

        threshold = panel["threshold"]
        if not isinstance(threshold, dict):
            raise DashboardConfigError(f"'{panel_id}.threshold' must be a YAML object")
        if threshold.get("aggregation") not in panel["aggregations"]:
            raise DashboardConfigError(
                f"'{panel_id}.threshold.aggregation' must be one of the panel aggregations"
            )
        if threshold.get("operator") not in {"lte", "gte"}:
            raise DashboardConfigError(
                f"'{panel_id}.threshold.operator' must be 'lte' or 'gte'"
            )
        if not isinstance(threshold.get("value"), (int, float)):
            raise DashboardConfigError(f"'{panel_id}.threshold.value' must be numeric")

    return payload


def main() -> int:
    configure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Validate the Day 13 dashboard contract")
    parser.add_argument(
        "--config",
        type=Path,
        default=REPO_ROOT / "config" / "dashboard.yaml",
        help="Path to dashboard YAML",
    )
    args = parser.parse_args()

    try:
        load_dashboard_config(args.config)
    except DashboardConfigError as exc:
        print(f"INVALID: {exc}")
        return 1

    print(f"VALID: {len(REQUIRED_PANEL_IDS)}/6 panels are present in the dashboard contract.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
