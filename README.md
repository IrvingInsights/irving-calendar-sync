# Irving Calendar Sync

One-way sync from a Notion Tasks database to Google Calendar.

This repo is intentionally small and operational. It should be boring, observable, and separate from Irving OS.

## Files

- `notion_google_sync.py`: sync script.
- `.github/workflows/notion-google-sync.yml`: manual GitHub Actions workflow. The schedule is currently disabled until credentials are configured.

## Required Environment Variables

| Variable | Description |
|---|---|
| `NOTION_API_TOKEN` | Notion integration secret |
| `NOTION_TASKS_DB_ID` | 32-character Notion Tasks database ID |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | JSON string for Google service account |
| `DOMAIN_CALENDAR_MAPPING` | JSON mapping of Notion domains to Google Calendar IDs |
| `TIMEZONE` | IANA timezone, defaults to `America/New_York` |

## Usage

```bash
pip install -r requirements.txt
python notion_google_sync.py
```

## Boundary

This repo exists only if a custom Notion-to-Google sync remains necessary. If Codex automations or calendar connectors fully cover the workflow later, retire this repo rather than expanding it.
