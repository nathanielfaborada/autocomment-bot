# Autocomment & Autowatcher Bot

Automation bots for Facebook auto-commenting and YouTube auto-watching.

## Requirements

- Python 3.10+
- Chromium (included in `chrome-win/`)

## Installation

1. Install dependencies:

```bash
pip install pyppeteer python-dotenv requests
```

2. If Chromium is not yet downloaded:

```bash
py chromium_downloader.py
```

## Configuration

Edit `.env` with your settings:

```env
CHROME_PATH=C:\path\to\chrome-win\chrome.exe

# YouTube Watcher
YOUTUBE_VIDEO_URL=https://www.youtube.com/watch?v=YOUR_VIDEO_ID
WATCH_DURATION_SECONDS=120
NUM_WATCHERS=4
```

## Usage

**YouTube Auto-Watcher:**
```bash
py autowatcher.py
```

Opens `NUM_WATCHERS` browser windows simultaneously, each watching the video for ~`WATCH_DURATION_SECONDS` seconds (with slight random variation).

**Facebook Auto-Commenter:**
```bash
py autocomment.py
```

## Notes

- `chrome-win/`, `chromium-win.zip`, and `.env` are excluded from git
- Audio is muted on all watcher sessions
