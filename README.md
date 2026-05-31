# InstaFollowChecker

Compares Instagram export files to show:

- who you follow that does not follow you back
- who follows you that you do not follow back
- mutual follows

## Input Files

Place Instagram export JSON files in one folder:

- `followers_1.json` (and optional `followers_2.json`, etc.)
- `following.json` (or matching `following*.json`)

## Usage

```bash
python main.py /path/to/export
python main.py --no-color
```

Outputs:
- `not_following_back.txt`
- `not_followed_back.txt`
- `mutual.txt`
- `report.txt`
- `not_following_back.csv`

## Requirements

- Python 3.8+
- No third-party dependencies.

## License

MIT

