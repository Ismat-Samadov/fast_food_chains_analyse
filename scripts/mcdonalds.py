import argparse
import csv
import html as html_lib
import os
import re
import sys
from datetime import datetime, timezone


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def extract_with_bs4(payload: str):
    try:
        from bs4 import BeautifulSoup  # type: ignore
    except Exception:
        return None

    soup = BeautifulSoup(payload, "html.parser")
    blocks = soup.select("div.publication")
    if not blocks:
        return []

    rows = []
    for block in blocks:
        name = None
        h2 = block.select_one("h2")
        if h2:
            name = normalize_space(h2.get_text(" ", strip=True))
        data = {
            "name": name,
            "address": None,
            "phone": None,
            "hours": None,
            "drive_thru": None,
            "mcdelivery": None,
        }

        for desc in block.select("div.mcd-publication__text-description"):
            text = normalize_space(desc.get_text(" ", strip=True))
            text = text.replace("McDelivery®", "McDelivery")
            if "Ünvan:" in text:
                data["address"] = text.split("Ünvan:", 1)[1].strip()
            elif "Telefon nömrəsi:" in text:
                data["phone"] = text.split("Telefon nömrəsi:", 1)[1].strip()
            elif "İş saatları:" in text:
                data["hours"] = text.split("İş saatları:", 1)[1].strip()
            elif "Drive thru:" in text:
                data["drive_thru"] = text.split("Drive thru:", 1)[1].strip()
            elif "McDelivery:" in text:
                data["mcdelivery"] = text.split("McDelivery:", 1)[1].strip()

        if any(value for value in data.values()):
            rows.append(data)

    return rows


def extract_publication_blocks(payload: str):
    payload = html_lib.unescape(payload)
    parts = payload.split('<div class="publication">')
    if len(parts) <= 1:
        return []
    blocks = []
    for chunk in parts[1:]:
        end_idx = chunk.find('</div>\n                        </div>')
        if end_idx == -1:
            end_idx = chunk.find('</div>\n                    </div>')
        if end_idx == -1:
            end_idx = chunk.find('</div>')
        blocks.append(chunk[:end_idx])
    return blocks


def extract_field(block: str, label: str):
    pattern = rf"{label}\s*</b>\s*([^<]+)"
    match = re.search(pattern, block)
    if not match:
        return None
    return normalize_space(html_lib.unescape(match.group(1)))


def extract_name(block: str):
    match = re.search(r"<h2>\s*<b>(.*?)</b>\s*</h2>", block, re.S)
    if not match:
        return None
    return normalize_space(html_lib.unescape(match.group(1)))


def extract_with_regex(payload: str):
    blocks = extract_publication_blocks(payload)
    if not blocks:
        return []

    rows = []
    for block in blocks:
        rows.append(
            {
                "name": extract_name(block),
                "address": extract_field(block, r"Ünvan:"),
                "phone": extract_field(block, r"Telefon nömrəsi:"),
                "hours": extract_field(block, r"İş saatları:"),
                "drive_thru": extract_field(block, r"Drive thru:"),
                "mcdelivery": extract_field(block, r"McDelivery®?:"),
            }
        )
    return rows


def normalize_rows(rows, source_url):
    scraped_at = datetime.now(timezone.utc).isoformat()
    out = []
    for row in rows:
        if not row.get("name") and not row.get("address"):
            continue
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
        "hours",
        "drive_thru",
        "mcdelivery",
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

    rows = extract_with_bs4(payload)
    if rows is None or rows == []:
        rows = extract_with_regex(payload)

    if not rows:
        print("Input file did not contain usable location data.")
        return 1

    normalized = normalize_rows(rows, source_url or input_path)
    write_csv(normalized, output_path)
    print(f"Saved {len(normalized)} rows to {output_path}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse McDonald's Azerbaijan locations.")
    parser.add_argument("--input", required=True, help="Path to saved HTML")
    parser.add_argument(
        "--output",
        default=os.path.join("data", "mcdonalds.csv"),
        help="Output CSV path (default: data/mcdonalds.csv)",
    )
    parser.add_argument("--source-url", default=None, help="Source URL for metadata")
    args = parser.parse_args()
    sys.exit(main(args.input, args.output, args.source_url))
