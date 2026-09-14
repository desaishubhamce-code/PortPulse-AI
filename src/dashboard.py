"""
Port Congestion Dashboard
--------------------------
A Streamlit web dashboard that visualises port congestion predictions.
It reuses the core logic from predict_congestion.py directly — no duplication.

Run with:
    streamlit run dashboard.py
"""

import pandas as pd
import streamlit as st

# Import our prediction functions from predict_congestion.py
from predict_congestion import (
    load_ships,
    compute_estimated_wait_start,
    find_congested_berths,
)
from datetime import timedelta


# ── PAGE CONFIG ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Port Congestion Predictor",
    page_icon="🚢",
    layout="wide",          # use the full browser width
)

st.title("🚢 Port Congestion Predictor")
st.caption("Hackathon demo — predicts berth congestion over the next 24–72 hours.")


# ── LOAD & PROCESS DATA ───────────────────────────────────────────────────────

# @st.cache_data tells Streamlit: "run this once and cache the result"
# so we don't reload the CSV on every UI interaction.
@st.cache_data
def get_data():
    """Load ships, compute wait times, and return everything we need."""
    ships = load_ships("port_congestion_data.csv")
    ships = compute_estimated_wait_start(ships)

    # Reference "now" = earliest ship arrival in the dataset
    now = min(s["arrival_time"] for s in ships)

    # Two prediction windows
    window_24h  = (now, now + timedelta(hours=24))
    window_72h  = (now + timedelta(hours=24), now + timedelta(hours=72))

    reports_24h = find_congested_berths(ships, *window_24h)
    reports_72h = find_congested_berths(ships, *window_72h)

    return ships, now, reports_24h, reports_72h

ships, reference_time, reports_24h, reports_72h = get_data()

st.info(f"📅 Reference time (earliest arrival): **{reference_time.strftime('%Y-%m-%d %H:%M')}**")


# ── SECTION 1: SHIP TABLE ─────────────────────────────────────────────────────

st.subheader("📋 All Ships — Arrival & Berth Overview")

# Build a clean pandas DataFrame for display from our list of ship dicts
ship_rows = []
for s in ships:
    ship_rows.append({
        "Ship Name":         s["ship_name"],
        "Arrival Time":      s["arrival_time"].strftime("%Y-%m-%d %H:%M"),
        "Berth":             s["berth_assigned"],
        "Cargo Type":        s["cargo_type"],
        "Unload Hours":      s["expected_unload_hours"],
        "Queue Position":    s["current_queue_position"],
        "Est. Unload Start": s["estimated_wait_start"].strftime("%Y-%m-%d %H:%M"),
        "Est. Unload End":   s["estimated_unload_end"].strftime("%Y-%m-%d %H:%M"),
    })

ship_df = pd.DataFrame(ship_rows)

# Display the table — use_container_width stretches it across the full page
st.dataframe(ship_df, use_container_width=True, hide_index=True)


# ── SECTION 2: BAR CHART — UTILISATION % PER BERTH ───────────────────────────

st.subheader("📊 Berth Utilisation by Prediction Window")

# Helper: turn a list of report dicts into a DataFrame with % utilisation
def reports_to_df(reports, label):
    rows = []
    for r in reports:
        rows.append({
            "Berth":          r["berth"],
            "Utilisation %":  round(r["utilisation_ratio"] * 100, 1),
            "Window":         label,
            "Ships":          ", ".join(r["ship_names"]),
            "Total Hrs":      r["total_unload_hours"],
        })
    return pd.DataFrame(rows)

df_24 = reports_to_df(reports_24h, "0–24h")
df_72 = reports_to_df(reports_72h, "24–72h")

# Combine both windows into one DataFrame for charting
chart_df = pd.concat([df_24, df_72], ignore_index=True)

# Pivot so each window becomes its own column — Streamlit bar charts need this format
pivot_df = chart_df.pivot(index="Berth", columns="Window", values="Utilisation %").fillna(0)
pivot_df = pivot_df.sort_index()   # sort berths alphabetically (B1, B2, …)

# Draw the grouped bar chart — Streamlit handles the rest
st.bar_chart(pivot_df, use_container_width=True)

# Add a legend note since Streamlit's built-in chart doesn't show units
st.caption("Y-axis = Utilisation % (100% = berth is exactly at capacity; >100% = congested backlog)")


# ── SECTION 3: CONGESTION ALERTS ─────────────────────────────────────────────

st.subheader("🚨 Congestion Alerts")

# We'll show alerts side by side for the two windows
col_left, col_right = st.columns(2)

def render_alerts(column, reports, window_label):
    """Render colour-coded alert cards inside a Streamlit column."""
    column.markdown(f"#### {window_label}")

    if not reports:
        column.success("No active ships in this window.")
        return

    for r in reports:
        util_pct = r["utilisation_ratio"] * 100

        # ── Colour thresholds ──────────────────────────────────────────────
        # Red   → utilisation > 100%  (berth is overloaded)
        # Yellow → 70–100%            (berth is near capacity)
        # Green  → below 70%          (berth has headroom)
        if util_pct > 100:
            # st.error = red box
            column.error(
                f"🔴 **Berth {r['berth']}** — {util_pct:.0f}% utilised  \n"
                f"{r['ships_in_window']} ship(s): {', '.join(r['ship_names'])}"
            )
        elif util_pct >= 70:
            # st.warning = yellow/orange box
            column.warning(
                f"🟡 **Berth {r['berth']}** — {util_pct:.0f}% utilised  \n"
                f"{r['ships_in_window']} ship(s): {', '.join(r['ship_names'])}"
            )
        else:
            # st.success = green box
            column.success(
                f"🟢 **Berth {r['berth']}** — {util_pct:.0f}% utilised  \n"
                f"{r['ships_in_window']} ship(s): {', '.join(r['ship_names'])}"
            )

render_alerts(col_left,  reports_24h, "⏱ Next 24 Hours")
render_alerts(col_right, reports_72h, "📆 24–72 Hours")


# ── FOOTER ────────────────────────────────────────────────────────────────────

st.divider()
st.caption("Data source: port_congestion_data.csv · Congestion logic: predict_congestion.py")
