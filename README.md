# InstaFollowChecker

A simple Python script that parses your Instagram data export and tells you who isn't following you back, who you aren't following back, and who your mutual follows are.

No login, no API, no third-party services — it only reads the JSON files Instagram gives you directly.

---

## How to get your Instagram data

1. Open Instagram → **Settings** → **Your activity** → **Download your information**
2. Select **Some of your information** and tick **Followers and following**
3. Set format to **JSON**, request the download, and wait for the email
4. Extract the ZIP — you'll find `followers_1.json` and `following.json` inside the `connections/followers_and_following/` folder
5. Copy both files into the same folder as `main.py`

---

## Usage

```bash
python main.py
```

No dependencies beyond the Python standard library.

---

## Output

The script prints three sections:

| Section | What it means |
|---------|---------------|
| **Not following you back** | Accounts you follow that don't follow you |
| **You don't follow back** | Accounts that follow you that you don't follow |
| **Mutual follows** | Accounts where you both follow each other |

A summary count is printed at the end, and the "not following back" list is also saved to `not_following_back.txt` in the same folder.

Where available, the date you followed each account is shown in brackets next to the username.

---

## File detection

The script automatically looks for `followers_1.json` and `following.json` in the current directory. If Instagram names them slightly differently in your export, rename them to match or place them in the same folder — the script will find them.

---

## License

MIT
