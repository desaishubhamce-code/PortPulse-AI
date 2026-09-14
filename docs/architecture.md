# Architecture

**Data Layer:** Ship data (name, arrival time, assigned berth, cargo type, expected unload hours, queue position) is loaded from a CSV file using Pandas.

**Logic Layer (predict_congestion.py):** Processes the raw ship data to calculate per-berth utilization percentages for two time windows (0-24h and 24-72h), and classifies each berth's congestion risk based on utilization thresholds.

**Presentation Layer (dashboard.py):** A Streamlit app that imports the logic layer functions, caches the computed results, and renders:
1. A table of all ships with berth and cargo details
2. A bar chart of utilization % per berth for both time windows
3. Color-coded risk alerts (red/yellow/green) per berth

**Flow:** CSV data → predict_congestion.py (compute utilization + risk) → dashboard.py (visualize) → browser (Streamlit UI)
