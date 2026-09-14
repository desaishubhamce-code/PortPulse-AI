"""
Port Congestion Predictor
--------------------------
Reads ship arrival data from port_congestion_data.csv and predicts
which berths will be congested in the next 24-72 hours.

Congestion is defined as: a berth where the total backlog of unload
time exceeds the available hours in the prediction window.
"""

import csv
from datetime import datetime, timedelta


# ── 1. LOAD DATA ─────────────────────────────────────────────────────────────

def load_ships(filepath):
    """Read the CSV file and return a list of ship dictionaries."""
    ships = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ships.append({
                "ship_name":             row["ship_name"],
                # Parse the arrival time string into a Python datetime object
                "arrival_time":          datetime.strptime(row["arrival_time"], "%Y-%m-%d %H:%M"),
                "berth_assigned":        row["berth_assigned"],
                "cargo_type":            row["cargo_type"],
                # Convert numeric strings to the right types
                "expected_unload_hours": float(row["expected_unload_hours"]),
                "current_queue_position": int(row["current_queue_position"]),
            })
    return ships


# ── 2. FEATURE ENGINEERING ───────────────────────────────────────────────────

def compute_estimated_wait_start(ships):
    """
    For each ship, estimate when it will actually START unloading.

    Logic: ships at the same berth must wait for all ships ahead of them
    in the queue to finish unloading first.

    We do this berth-by-berth:
      - Sort ships at a berth by queue position.
      - Each ship's unload start = max(its arrival time, previous ship's unload end).
    """
    # Group ships by berth
    berths = {}
    for ship in ships:
        berth = ship["berth_assigned"]
        berths.setdefault(berth, []).append(ship)

    for berth, berth_ships in berths.items():
        # Sort by queue position so we process them in order
        berth_ships.sort(key=lambda s: s["current_queue_position"])

        previous_end = None  # tracks when the previous ship finishes unloading

        for ship in berth_ships:
            if previous_end is None:
                # First ship at this berth — starts unloading on arrival
                ship["estimated_wait_start"] = ship["arrival_time"]
            else:
                # Must wait until the berth is free (or arrive later, whichever is later)
                ship["estimated_wait_start"] = max(ship["arrival_time"], previous_end)

            # Calculate when this ship will finish unloading
            ship["estimated_unload_end"] = (
                ship["estimated_wait_start"]
                + timedelta(hours=ship["expected_unload_hours"])
            )

            # This ship's end time becomes the "previous end" for the next ship
            previous_end = ship["estimated_unload_end"]

    return ships


# ── 3. CONGESTION DETECTION ──────────────────────────────────────────────────

def find_congested_berths(ships, window_start, window_end):
    """
    Identify berths that are congested within a given time window.

    A berth is considered congested if:
      - More than one ship's unloading window overlaps within the prediction period.
      - The total queued unload hours at that berth exceed the available hours
        in the window (i.e., the berth cannot keep up).

    Returns a list of congestion report dictionaries.
    """
    # Group ships whose activity falls inside the prediction window
    berth_activity = {}

    for ship in ships:
        start = ship["estimated_wait_start"]
        end   = ship["estimated_unload_end"]

        # Check if this ship's unloading overlaps with our prediction window
        overlaps = start < window_end and end > window_start
        if not overlaps:
            continue

        berth = ship["berth_assigned"]
        berth_activity.setdefault(berth, []).append(ship)

    # Now assess congestion for each active berth
    window_hours = (window_end - window_start).total_seconds() / 3600
    reports = []

    for berth, active_ships in berth_activity.items():
        total_unload_hours = sum(s["expected_unload_hours"] for s in active_ships)
        ship_count         = len(active_ships)

        # Utilisation ratio: how overloaded is this berth?
        # > 1.0 means the berth cannot finish all ships in time → congested
        utilisation = total_unload_hours / window_hours

        is_congested = utilisation > 1.0 or ship_count > 2

        reports.append({
            "berth":               berth,
            "ships_in_window":     ship_count,
            "total_unload_hours":  round(total_unload_hours, 1),
            "window_hours":        round(window_hours, 1),
            "utilisation_ratio":   round(utilisation, 2),
            "congested":           is_congested,
            "ship_names":          [s["ship_name"] for s in active_ships],
        })

    # Sort by utilisation descending so the worst berths appear first
    reports.sort(key=lambda r: r["utilisation_ratio"], reverse=True)
    return reports


# ── 4. PRINT RESULTS ─────────────────────────────────────────────────────────

def print_report(reports, window_label):
    """Print a human-readable congestion report for a time window."""
    print(f"\n{'='*60}")
    print(f"  Congestion Report — {window_label}")
    print(f"{'='*60}")

    if not reports:
        print("  No ships active in this window.")
        return

    for r in reports:
        status = "🔴 CONGESTED" if r["congested"] else "🟢 Clear"
        print(f"\n  Berth {r['berth']}  {status}")
        print(f"    Ships in window  : {r['ships_in_window']}")
        print(f"    Total unload hrs : {r['total_unload_hours']}h / {r['window_hours']}h available")
        print(f"    Utilisation      : {r['utilisation_ratio']*100:.0f}%")
        print(f"    Ships            : {', '.join(r['ship_names'])}")


# ── 5. MAIN ──────────────────────────────────────────────────────────────────

def main():
    # Load and enrich ship data
    ships = load_ships("port_congestion_data.csv")
    ships = compute_estimated_wait_start(ships)

    # Use the earliest arrival as the reference "now"
    now = min(s["arrival_time"] for s in ships)

    print(f"\nReference time (earliest arrival): {now.strftime('%Y-%m-%d %H:%M')}")

    # Define two prediction windows
    windows = [
        ("Next 24 hours", now, now + timedelta(hours=24)),
        ("24–72 hours",   now + timedelta(hours=24), now + timedelta(hours=72)),
    ]

    for label, w_start, w_end in windows:
        reports = find_congested_berths(ships, w_start, w_end)
        print_report(reports, label)

    print("\n")


if __name__ == "__main__":
    main()
