import os
import re
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


CHARTS_DIR = Path("charts")
DATA_DIR = Path("data")


def ensure_charts_dir():
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)


def parse_time_to_hour(value: str):
    if not value:
        return None
    match = re.match(r"^(\d{1,2}):(\d{2})$", value.strip())
    if not match:
        return None
    hour = int(match.group(1))
    minute = int(match.group(2))
    return hour + minute / 60


def parse_hours_range(value: str):
    if not value or pd.isna(value):
        return None, None, False, False
    text = str(value)
    if "24" in text and "saat" in text:
        return 0.0, 24.0, True, True

    times = re.findall(r"\d{1,2}:\d{2}", text)
    if len(times) < 2:
        return None, None, False, False
    open_hour = parse_time_to_hour(times[0])
    close_hour = parse_time_to_hour(times[1])
    if open_hour is None or close_hour is None:
        return None, None, False, False

    is_24h = open_hour == close_hour == 0.0
    closes_after_midnight = close_hour < open_hour or (close_hour == 0.0 and open_hour > 0)
    return open_hour, close_hour, is_24h, closes_after_midnight or is_24h


def bucket_close_time(open_hour, close_hour, is_24h, after_midnight):
    if is_24h:
        return "24h"
    if after_midnight:
        return "After midnight"
    return "Before midnight"


def load_data():
    kfc = pd.read_csv(DATA_DIR / "kfc.csv")
    mcd = pd.read_csv(DATA_DIR / "mcdonalds.csv")
    shaurma = pd.read_csv(DATA_DIR / "shaurma.csv")
    return kfc, mcd, shaurma


def chart_location_counts(kfc, mcd, shaurma):
    counts = pd.Series({
        "KFC": len(kfc),
        "McDonald's": len(mcd),
        "Shaurma N1": len(shaurma),
    })

    fig, ax = plt.subplots(figsize=(7, 4))
    counts.sort_values(ascending=False).plot(kind="bar", ax=ax, color=["#d62828", "#f77f00", "#003049"])
    ax.set_title("Location Count by Brand")
    ax.set_ylabel("Number of locations")
    ax.set_xlabel("")
    for i, v in enumerate(counts.sort_values(ascending=False)):
        ax.text(i, v + 0.5, str(int(v)), ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "location_counts_by_brand.png", dpi=200)
    plt.close(fig)


def chart_late_night_coverage(kfc, mcd, shaurma):
    def classify_kfc(row):
        open_hour = parse_time_to_hour(str(row.get("openingHour", "")))
        close_hour = parse_time_to_hour(str(row.get("closingHour", "")))
        if open_hour is None or close_hour is None:
            return None
        is_24h = open_hour == close_hour == 0.0
        after_midnight = close_hour < open_hour or (close_hour == 0.0 and open_hour > 0)
        return bucket_close_time(open_hour, close_hour, is_24h, after_midnight)

    def classify_range(value):
        open_hour, close_hour, is_24h, after_midnight = parse_hours_range(value)
        if open_hour is None:
            return None
        return bucket_close_time(open_hour, close_hour, is_24h, after_midnight)

    kfc_bucket = kfc.apply(classify_kfc, axis=1).value_counts()
    mcd_bucket = mcd["hours"].apply(classify_range).value_counts()
    shaurma_bucket = shaurma["dine_in"].apply(classify_range).value_counts()

    buckets = ["Before midnight", "After midnight", "24h"]
    data = pd.DataFrame({
        "KFC": [kfc_bucket.get(b, 0) for b in buckets],
        "McDonald's": [mcd_bucket.get(b, 0) for b in buckets],
        "Shaurma N1": [shaurma_bucket.get(b, 0) for b in buckets],
    }, index=buckets)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    data.T.plot(kind="bar", stacked=True, ax=ax, color=["#4a4e69", "#9a8c98", "#c9ada7"])
    ax.set_title("Late-Night & 24/7 Coverage by Brand")
    ax.set_ylabel("Number of locations")
    ax.set_xlabel("")
    ax.legend(title="Closing window", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "late_night_coverage_by_brand.png", dpi=200)
    plt.close(fig)


def chart_mcd_services(mcd):
    total = len(mcd)
    drive_thru = mcd["drive_thru"].notna().sum()
    mcdelivery = mcd["mcdelivery"].notna().sum()

    labels = ["Drive-thru", "McDelivery"]
    values = [drive_thru, mcdelivery]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels, values, color=["#fcbf49", "#eae2b7"])
    ax.set_title("McDonald's Convenience Services Coverage")
    ax.set_ylabel("Locations with service")
    ax.set_ylim(0, max(values) + 5)
    for bar, value in zip(bars, values):
        pct = (value / total) * 100 if total else 0
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.4, f"{value} ({pct:.0f}%)", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "mcdonalds_services_coverage.png", dpi=200)
    plt.close(fig)


def chart_kfc_opening_hours(kfc):
    opening = kfc["openingHour"].astype(str).value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(7, 4))
    opening.plot(kind="bar", ax=ax, color="#457b9d")
    ax.set_title("KFC Opening Hour Distribution")
    ax.set_ylabel("Number of locations")
    ax.set_xlabel("Opening hour")
    for i, v in enumerate(opening.values):
        ax.text(i, v + 0.3, str(int(v)), ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "kfc_opening_hours.png", dpi=200)
    plt.close(fig)


def main():
    ensure_charts_dir()
    kfc, mcd, shaurma = load_data()
    chart_location_counts(kfc, mcd, shaurma)
    chart_late_night_coverage(kfc, mcd, shaurma)
    chart_mcd_services(mcd)
    chart_kfc_opening_hours(kfc)


if __name__ == "__main__":
    main()
