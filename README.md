# InstaFollowChecker

A Python tool that analyzes your downloaded Instagram data export to show exactly who isn't following you back.

## Features

- Parses official Instagram data export files
- Identifies non-followers (people you follow who don't follow back)
- Clean, readable output
- Optional export of results to CSV

## Installation

```bash
git clone https://github.com/drew-codes-things/InstaFollowChecker.git
cd InstaFollowChecker
pip install -r requirements.txt
```

## Usage

1. Download your Instagram data from Instagram settings
2. Run the script and point it to your data folder
3. View the list of accounts that don't follow you back

```bash
python main.py
```

## Requirements

- Python 3.8+
- Your Instagram data export (JSON format)

## License

MIT License