"""Streamlit dashboard cho Day 13 Observability.

Đọc dữ liệu trực tiếp từ data/logs.jsonl và dựng đúng 6 panel theo contract
trong config/dashboard.yaml (latency, traffic, errors, cost, tokens, quality).
Ngưỡng threshold vẽ trên biểu đồ được lấy thẳng từ config/slo.yaml và
config/dashboard.yaml để không bị lệch giữa dashboard và SLO chính thức.

Chạy:
    streamlit run scripts/dashboard.py

Tùy chọn tự động refresh mỗi 30 giây (theo dashboard.yaml -> refresh_seconds)
cần gói streamlit-autorefresh. Nếu chưa cài, dashboard vẫn chạy bình thường,
chỉ là bạn phải tự bấm nút "Refresh ngay" hoặc F5.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import streamlit as st
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
LOGS_PATH = REPO_ROOT / "data" / "logs.jsonl"
DASHBOARD_CONFIG_PATH = REPO_ROOT / "config" / "dashboard.yaml"
SLO_PATH = REPO_ROOT / "config" / "slo.yaml"

st.set_page_config(page_title="Day 13 AI Observability", layout="wide")

try:
    from streamlit_autorefresh import st_autorefresh

    st_autorefresh(interval=30_000, key="dashboard_autorefresh")
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Load config (nguồn chuẩn cho tên panel, đơn vị, threshold)
# ---------------------------------------------------------------------------

@st.cache_data(ttl=10)
def load_dashboard_config() -> dict:
    payload = yaml.safe_load(DASHBOARD_CONFIG_PATH.read_text(encoding="utf-8"))
    return payload["dashboard"]


@st.cache_data(ttl=10)
def load_slo_config() -> dict:
    return yaml.safe_load(SLO_PATH.read_text(encoding="utf-8"))


@st.cache_data(ttl=5)
def load_logs() -> pd.DataFrame:
    if not LOGS_PATH.exists():
        return pd.DataFrame()

    rows = []
    with LOGS_PATH.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if not rows:
        return pd.DataFrame()

    df = pd.json_normalize(rows)
    if "ts" in df.columns:
        df["ts"] = pd.to_datetime(df["ts"], utc=True, errors="coerce")
    return df


def panel_by_id(dashboard_cfg: dict, panel_id: str) -> dict:
    for panel in dashboard_cfg["panels"]:
        if panel["id"] == panel_id:
            return panel
    raise KeyError(f"Panel '{panel_id}' không có trong contract")


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

dashboard_cfg = load_dashboard_config()
slo_cfg = load_slo_config()
df = load_logs()

st.title(dashboard_cfg["title"])
st.caption(
    f"Nguồn dữ liệu: data/logs.jsonl · "
    f"Time range: {dashboard_cfg['time_range_minutes']} phút · "
    f"Refresh: {dashboard_cfg['refresh_seconds']}s · "
    f"SLO window: {slo_cfg.get('window', 'n/a')}"
)

col_a, col_b = st.columns([3, 1])
with col_b:
    if st.button("Refresh ngay"):
        load_logs.clear()
        st.rerun()

if df.empty:
    st.warning(
        "Chưa có data/logs.jsonl hoặc file rỗng. Chạy app + load test trước:\n\n"
        "uvicorn app.main:app --reload --env-file .env\n"
        "python scripts/load_test.py"
    )
    st.stop()

# Lọc theo time range cấu hình trong dashboard.yaml (mặc định 60 phút)
time_range = timedelta(minutes=dashboard_cfg["time_range_minutes"])
now = df["ts"].max()
window_start = now - time_range
df_window = df[df["ts"] >= window_start].copy()

st.caption(
    f"Đang hiển thị {len(df_window)} log record trong cửa sổ "
    f"{window_start.strftime('%Y-%m-%d %H:%M:%S UTC')} → "
    f"{now.strftime('%Y-%m-%d %H:%M:%S UTC')}"
)

responses = df_window[df_window["event"] == "response_sent"].copy()
requests_recv = df_window[df_window["event"] == "request_received"].copy()
requests_fail = df_window[df_window["event"] == "request_failed"].copy()

row1 = st.columns(3)
row2 = st.columns(3)

# --- Panel 1: Latency (P50/P95/P99) ---------------------------------------
with row1[0]:
    panel = panel_by_id(dashboard_cfg, "latency")
    st.subheader(panel["title"])
    if responses.empty or "latency_ms" not in responses.columns:
        st.info("Chưa có response_sent event nào trong cửa sổ này.")
    else:
        p50 = responses["latency_ms"].quantile(0.50)
        p95 = responses["latency_ms"].quantile(0.95)
        p99 = responses["latency_ms"].quantile(0.99)
        threshold = panel["threshold"]["value"]

        m1, m2, m3 = st.columns(3)
        m1.metric("P50", f"{p50:.0f} {panel['unit']}")
        m2.metric(
            "P95", f"{p95:.0f} {panel['unit']}",
            delta=f"ngưỡng {threshold}", delta_color="inverse",
        )
        m3.metric("P99", f"{p99:.0f} {panel['unit']}")

        chart_df = responses.set_index("ts")[["latency_ms"]].rename(
            columns={"latency_ms": "latency (ms)"}
        )
        st.line_chart(chart_df)
        if p95 > threshold:
            st.error(f"P95 latency ({p95:.0f}ms) đang VƯỢT threshold {threshold}ms")
        else:
            st.success(f"P95 latency trong ngưỡng cho phép ({threshold}ms)")

# --- Panel 2: Traffic -------------------------------------------------------
with row1[1]:
    panel = panel_by_id(dashboard_cfg, "traffic")
    st.subheader(panel["title"])
    if requests_recv.empty:
        st.info("Chưa có request_received event nào trong cửa sổ này.")
    else:
        per_minute = (
            requests_recv.set_index("ts")
            .resample("1min")
            .size()
            .rename("requests_per_minute")
        )
        st.line_chart(per_minute)
        st.metric("Tổng request trong cửa sổ", int(requests_recv.shape[0]))

# --- Panel 3: Errors ---------------------------------------------------------
with row1[2]:
    panel = panel_by_id(dashboard_cfg, "errors")
    st.subheader(panel["title"])
    total_req = len(requests_recv)
    total_fail = len(requests_fail)
    error_rate = (total_fail / total_req * 100) if total_req else 0.0
    threshold = panel["threshold"]["value"]

    st.metric(
        "Error rate", f"{error_rate:.2f}%",
        delta=f"ngưỡng {threshold}%", delta_color="inverse",
    )
    if total_fail and "error_type" in requests_fail.columns:
        breakdown = requests_fail["error_type"].value_counts()
        st.bar_chart(breakdown)
    else:
        st.success("Không có request_failed nào trong cửa sổ này.")
    if error_rate > threshold:
        st.error(f"Error rate đang VƯỢT threshold {threshold}%")

# --- Panel 4: Cost -----------------------------------------------------------
with row2[0]:
    panel = panel_by_id(dashboard_cfg, "cost")
    st.subheader(panel["title"])
    if responses.empty or "cost_usd" not in responses.columns:
        st.info("Chưa có dữ liệu cost.")
    else:
        total_cost = responses["cost_usd"].sum()
        threshold = panel["threshold"]["value"]
        st.metric(
            "Tổng cost trong cửa sổ", f"${total_cost:.4f}",
            delta=f"ngưỡng ${threshold}", delta_color="inverse",
        )
        per_minute_cost = (
            responses.set_index("ts")["cost_usd"].resample("1min").sum()
        )
        st.bar_chart(per_minute_cost)
        if total_cost > threshold:
            st.error(f"Cost đang VƯỢT threshold ${threshold}")

# --- Panel 5: Tokens ---------------------------------------------------------
with row2[1]:
    panel = panel_by_id(dashboard_cfg, "tokens")
    st.subheader(panel["title"])
    if responses.empty or "tokens_in" not in responses.columns:
        st.info("Chưa có dữ liệu token.")
    else:
        total_in = int(responses["tokens_in"].sum())
        total_out = int(responses["tokens_out"].sum())
        threshold = panel["threshold"]["value"]
        m1, m2 = st.columns(2)
        m1.metric("Tokens in", f"{total_in:,}")
        m2.metric("Tokens out", f"{total_out:,}")
        st.bar_chart(
            pd.DataFrame(
                {"tokens_in": [total_in], "tokens_out": [total_out]}, index=["tổng"]
            )
        )
        if max(total_in, total_out) > threshold:
            st.warning(f"Một field token đang vượt threshold {threshold}")

# --- Panel 6: Quality proxy ---------------------------------------------------
with row2[2]:
    panel = panel_by_id(dashboard_cfg, "quality")
    st.subheader(panel["title"])
    if responses.empty or "quality_score" not in responses.columns:
        st.info("Chưa có dữ liệu quality_score.")
    else:
        mean_quality = responses["quality_score"].mean()
        threshold = panel["threshold"]["value"]
        st.metric(
            "Quality score trung bình", f"{mean_quality:.3f}",
            delta=f"ngưỡng {threshold}",
        )
        chart_df = responses.set_index("ts")[["quality_score"]]
        st.line_chart(chart_df)
        if mean_quality < threshold:
            st.error(f"Quality score đang DƯỚI threshold {threshold}")
        else:
            st.success(f"Quality score đạt ngưỡng tối thiểu {threshold}")
