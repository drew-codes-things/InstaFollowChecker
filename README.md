# InstaFollowChecker

Python tool that analyses your official Instagram data export to identify accounts that don't follow you back.

## What it does

- Compares your `following.json` and `followers_1.json` export files
- Shows who doesn't follow you back, who you don't follow back, and mutual follows
- Exports results to `.txt` files and a `not_following_back.csv` with username and follow date
- Colour-coded terminal output (disable with `--no-color`)

## Required Instagram Export Files

Download your Instagram data at **Settings -> Your activity -> Download your information**. Request JSON format. Once downloaded, locate these two files inside the zip:

```
connections/
    followers_1.json
    following/
        following.json
```

Point the script at the folder containing those files.

## File Structure

```
InstaFollowChecker/
    main.py
    requirements.txt
    README.md
    LICENSE
```

## Installation

### Linux (Recommended - Virtual Environment)

```bash
git clone https://github.com/drew-codes-things/InstaFollowChecker.git
cd InstaFollowChecker

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### macOS / Windows (Simple Method)

```bash
git clone https://github.com/drew-codes-things/InstaFollowChecker.git
cd InstaFollowChecker

pip install -r requirements.txt
```

## Usage

```bash
# Point at the folder containing followers_1.json and following.json
python main.py /path/to/instagram_export

# Defaults to current directory if no path given
python main.py

# Disable colour output
python main.py /path/to/export --no-color
```

## Sample Output

```
==================================================
  Not following you back (52)
==================================================
  someuser          [2023-04-10]
  anotheraccount    [2022-11-01]
  ...

==================================================
  Summary
==================================================
  Following:                120
  Followers:                 68
  Mutual:                    68
  Not following back:        52
  You don't follow back:      0

  Saved to /path/to/instagram_export/
    not_following_back.txt
    not_followed_back.txt
    mutual.txt
    report.txt
    not_following_back.csv
```

## Output Files

| File | Contents |
|---|---|
| `not_following_back.txt` | Accounts you follow that don't follow back |
| `not_followed_back.txt` | Accounts that follow you but you don't follow back |
| `mutual.txt` | Mutual follows |
| `report.txt` | Combined report with all three sections and summary |
| `not_following_back.csv` | CSV with `username` and `followed_since` columns |

## Requirements

- Python 3.8+

## License

MIT License
