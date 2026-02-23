KFC AZ branches scrape context

Status
- Network access from this machine is blocked by a corporate filter (Bank of Baku) and returns "Web Page Blocked" / 503 for `kfc.az` and `api.kfc.az`.

Script
- `scripts/kfc.py` scrapes branches and writes `data/kfc.csv`. It supports offline parsing via `--input` (HTML or JSON).

Next steps (last 2 requested)
- Provide the exact XHR/Fetch URL from DevTools that returns the branches JSON; we’ll wire it into `scripts/kfc.py` and rerun.
- Provide a saved HTML or JSON response path; we’ll run: `python scripts/kfc.py --input <path> --output data\kfc.csv`.
