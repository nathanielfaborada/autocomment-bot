# Autocomment Bot

Automation bot for Facebook auto-commenting using Pyppeteer (headless Chromium).

## Requirements

- Python 3.8+
- Google Chrome installed at `C:\Program Files\Google\Chrome\Application\chrome.exe`

## Setup

1. Install dependencies:

```bash
pip install pyppeteer python-dotenv
```

2. Create a `.env` file in the project root with your account credentials:

```env
ACCOUNT1_EMAIL=your_email@gmail.com
ACCOUNT1_PASSWORD=your_password

ACCOUNT2_EMAIL=your_email@gmail.com
ACCOUNT2_PASSWORD=your_password

ACCOUNT3_EMAIL=your_email@gmail.com
ACCOUNT3_PASSWORD=your_password

ACCOUNT4_EMAIL=your_email@gmail.com
ACCOUNT4_PASSWORD=your_password
```

> **Note:** Never commit your `.env` file to version control.

## Usage

```bash
python autocomment.py
```

## Contributors

Students of College of Mary Immaculate  
Bachelor of Science in Computer Science — BSCS 2-A

- [nathanielfaborada](https://github.com/nathanielfaborada)
- [johnpaul-bodino](https://github.com/johnpaul-bodino)
