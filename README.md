# InstaFollowChecker

Python tool that analyzes your official Instagram data export to identify accounts that don't follow you back.

## Technical Details

- Parses Instagram data export (JSON format)
- Compares "following" vs "followers" lists
- Outputs clean list of non-reciprocal accounts
- Optional CSV export

## File Structure

```
InstaFollowChecker/
├── main.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Usage

1. Download your Instagram data export
2. Run the script and point it to the data folder
3. View results

## Requirements

- Python 3.8+

## License

MIT License