import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timezone

import requests


BASE_URL = "https://kfc.az/az/branches"
API_HOST = "https://api.kfc.az"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    )
}


def fetch(session: requests.Session, url: str, verify: bool) -> requests.Response:
    resp = session.get(url, headers=DEFAULT_HEADERS, timeout=30, verify=verify)
    resp.raise_for_status()
    return resp


def extract_next_data(html: str):
    match = re.search(
        r'__NEXT_DATA__"\s+type="application/json">\s*(\{.*?\})\s*</script>',
        html,
        re.S,
    )
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None


def extract_build_id(html: str):
    for pattern in [
        r"/_next/static/([^/]+)/_buildManifest\.js",
        r"/_next/static/([^/]+)/_ssgManifest\.js",
        r"/_next/static/([^/]+)/",
    ]:
        match = re.search(pattern, html)
        if match:
            return match.group(1)
    return None


def iter_lists(obj):
    if isinstance(obj, dict):
        for value in obj.values():
            yield from iter_lists(value)
    elif isinstance(obj, list):
        if obj:
            yield obj
        for item in obj:
            yield from iter_lists(item)


def score_list(items):
    if not items or not any(isinstance(item, dict) for item in items):
        return 0
    key_hits = 0
    length = 0
    keys_of_interest = {
        "name",
        "title",
        "address",
        "phone",
        "city",
        "region",
        "district",
        "latitude",
        "longitude",
        "lat",
        "lng",
        "location",
        "workingHours",
        "openingHours",
        "opening_hours",
    }
    for item in items:
        if not isinstance(item, dict):
            continue
        length += 1
        for key in item.keys():
            if key in keys_of_interest:
                key_hits += 1
    return key_hits + min(length, 50)


def find_best_list(obj):
    best_list = None
    best_score = 0
    for candidate in iter_lists(obj):
        score = score_list(candidate)
        if score > best_score:
            best_score = score
            best_list = candidate
    return best_list


def flatten(value, prefix="", out=None):
    if out is None:
        out = {}
    if isinstance(value, dict):
        for key, val in value.items():
            new_prefix = f"{prefix}.{key}" if prefix else str(key)
            flatten(val, new_prefix, out)
    elif isinstance(value, list):
        out[prefix] = json.dumps(value, ensure_ascii=False)
    else:
        out[prefix] = value
    return out


def normalize_rows(items, source_url):
    rows = []
    scraped_at = datetime.now(timezone.utc).isoformat()
    for item in items:
        if not isinstance(item, dict):
            continue
        row = flatten(item)
        row["source_url"] = source_url
        row["scraped_at"] = scraped_at
        rows.append(row)
    return rows


def write_csv(rows, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row.keys()})
    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def try_load_json(resp):
    try:
        return resp.json()
    except ValueError:
        return None


def load_input_payload(input_path):
    with open(input_path, "r", encoding="utf-8") as handle:
        content = handle.read()
    try:
        return json.loads(content), "json"
    except json.JSONDecodeError:
        return content, "html"


def main(output_path, verify, input_path):
    if input_path:
        payload, kind = load_input_payload(input_path)
        if kind == "json":
            best_list = find_best_list(payload)
            if best_list:
                rows = normalize_rows(best_list, input_path)
                write_csv(rows, output_path)
                print(f"Saved {len(rows)} rows to {output_path}")
                return 0
        else:
            next_data = extract_next_data(payload)
            if next_data:
                best_list = find_best_list(next_data)
                if best_list:
                    rows = normalize_rows(best_list, input_path)
                    write_csv(rows, output_path)
                    print(f"Saved {len(rows)} rows to {output_path}")
                    return 0
        print("Input file did not contain usable branch data.")
        return 1

    session = requests.Session()

    html = None
    try:
        print(f"Fetching {BASE_URL}")
        resp = fetch(session, BASE_URL, verify)
        html = resp.text
    except requests.RequestException as exc:
        print(f"Warning: failed to fetch branches page ({exc}). Trying API endpoints.")

    if html:
        next_data = extract_next_data(html)
        if next_data:
            print("Found __NEXT_DATA__ payload")
            best_list = find_best_list(next_data)
            if best_list:
                rows = normalize_rows(best_list, BASE_URL)
                write_csv(rows, output_path)
                print(f"Saved {len(rows)} rows to {output_path}")
                return 0

        build_id = extract_build_id(html)
        if build_id:
            next_data_url = f"https://kfc.az/_next/data/{build_id}/az/branches.json"
            print(f"Fetching {next_data_url}")
            resp = fetch(session, next_data_url, verify)
            payload = try_load_json(resp)
            if payload:
                best_list = find_best_list(payload)
                if best_list:
                    rows = normalize_rows(best_list, next_data_url)
                    write_csv(rows, output_path)
                    print(f"Saved {len(rows)} rows to {output_path}")
                    return 0

    candidate_endpoints = [
        f"{API_HOST}/branches",
        f"{API_HOST}/branches?lang=az",
        f"{API_HOST}/branches?locale=az",
        f"{API_HOST}/branch",
        f"{API_HOST}/branch?lang=az",
        f"{API_HOST}/stores",
        f"{API_HOST}/stores?lang=az",
        f"{API_HOST}/locations",
        f"{API_HOST}/locations?lang=az",
        f"{API_HOST}/api/branches",
        f"{API_HOST}/api/branches?lang=az",
        f"{API_HOST}/api/branches/az",
        f"{API_HOST}/api/stores",
        f"{API_HOST}/v1/branches",
        f"{API_HOST}/v1/branches?lang=az",
    ]

    for url in candidate_endpoints:
        try:
            print(f"Fetching {url}")
            resp = fetch(session, url, verify)
        except requests.RequestException:
            continue
        payload = try_load_json(resp)
        if payload is None:
            continue
        best_list = find_best_list(payload)
        if best_list:
            rows = normalize_rows(best_list, url)
            write_csv(rows, output_path)
            print(f"Saved {len(rows)} rows to {output_path}")
            return 0

    print("Failed to find branch data. Try inspecting API calls in the browser.")
    return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape KFC Azerbaijan branches.")
    parser.add_argument(
        "--output",
        default=os.path.join("data", "kfc.csv"),
        help="Output CSV path (default: data/kfc.csv)",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate verification (use only if your network MITMs TLS).",
    )
    parser.add_argument(
        "--input",
        help="Path to a saved HTML or JSON response to parse without network access.",
    )
    args = parser.parse_args()
    verify = not args.insecure
    sys.exit(main(args.output, verify, args.input))
