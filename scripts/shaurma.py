import argparse
import csv
import html as html_lib
import os
import re
import sys
from datetime import datetime, timezone


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def extract_cards(payload: str):
    parts = payload.split('address_card')
    if len(parts) <= 1:
        return []
    blocks = []
    for chunk in parts[1:]:
        end_idx = chunk.find('</div>')
        if end_idx == -1:
            continue
        blocks.append(chunk[:end_idx])
    return blocks


def extract_name(block: str):
    match = re.search(r"<h2[^>]*>\s*<b>(.*?)</b>\s*</h2>", block, re.S)
    if not match:
        return None
    return normalize_space(html_lib.unescape(match.group(1)))


def extract_field(block: str, label: str):
    pattern = rf"{label}.*?<span>(.*?)</span>"
    match = re.search(pattern, block, re.S)
    if not match:
        return None
    return normalize_space(html_lib.unescape(match.group(1)))


def extract_phone(block: str):
    match = re.search(r"tel:([^\"\s]+)", block)
    if not match:
        return None
    return normalize_space(html_lib.unescape(match.group(1)))


def parse_rows(payload: str):
    rows = []
    for block in extract_cards(payload):
        rows.append(
            {
                "name": extract_name(block),
                "address": extract_field(block, r"Ünvan:"),
                "phone": extract_phone(block),
                "dine_in": extract_field(block, r"Dine-in:"),
            }
        )
    return [row for row in rows if row.get("name") or row.get("address")]


def normalize_rows(rows, source_url):
    scraped_at = datetime.now(timezone.utc).isoformat()
    out = []
    for row in rows:
        row["source_url"] = source_url
        row["scraped_at"] = scraped_at
        out.append(row)
    return out


def write_csv(rows, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = [
        "name",
        "address",
        "phone",
        "dine_in",
        "source_url",
        "scraped_at",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main(input_path, output_path, source_url):
    with open(input_path, "r", encoding="utf-8") as handle:
        payload = handle.read()

    rows = parse_rows(payload)
    if not rows:
        print("Input file did not contain usable location data.")
        return 1

    normalized = normalize_rows(rows, source_url or input_path)
    write_csv(normalized, output_path)
    print(f"Saved {len(normalized)} rows to {output_path}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Shaurma N1 locations.")
    parser.add_argument("--input", required=True, help="Path to saved HTML")
    parser.add_argument(
        "--output",
        default=os.path.join("data", "shaurma.csv"),
        help="Output CSV path (default: data/shaurma.csv)",
    )
    parser.add_argument("--source-url", default=None, help="Source URL for metadata")
    args = parser.parse_args()
    sys.exit(main(args.input, args.output, args.source_url))
