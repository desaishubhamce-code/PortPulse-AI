# Setup Guide

## Prerequisites

- Python 3.8 or higher — [download here](https://www.python.org/downloads/)
- `pip` (comes bundled with Python)
- A terminal / command prompt

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/desaishubhamce-code/PortPulse-AI.git
cd PortPulse-AI

# 2. Install dependencies
pip install streamlit pandas
```

No environment variables or database setup required — the app runs entirely from the included CSV file.

## Running the Dashboard

```bash
streamlit run src/dashboard.py
```

Streamlit will start a local web server and open the dashboard automatically. If it doesn't open, visit:

```
http://localhost:8501
```

## Running the Predictor (CLI only)

If you just want the text output without the dashboard:

```bash
python src/predict_congestion.py
```

## Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install streamlit pandas` |
| `FileNotFoundError: port_congestion_data.csv` | Make sure you run the command from the `PortPulse-AI/` root, not from inside `src/` |
| Port 8501 already in use | Run `streamlit run src/dashboard.py --server.port 8502` |
