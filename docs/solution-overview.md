# Solution Overview

PortPulse AI is a berth congestion prediction tool. It takes ship arrival time, expected unload hours, cargo type, and current queue position as input, and calculates berth utilization for two time windows: the next 0-24 hours and 24-72 hours.

Based on utilization percentage, each berth is classified into a risk level:
- Red (Congested): utilization > 100%
- Yellow (Warning): utilization 70-100%
- Green (Safe): utilization below 70%

The results are shown through an interactive Streamlit dashboard with a full ship table, a bar chart comparing berth utilization, and color-coded alerts, so operators can identify problem berths at a glance and act before congestion actually occurs.
