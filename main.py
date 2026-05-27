import json
import os
import glob
import sys
from datetime import datetime


def find_file(candidates):
    """Find the first existing file from a list of candidate names/globs."""
    for pattern in candidates:
        matches = glob.glob(pattern)
        if matches:
            return matches[0]
    return None


def load_following(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    usernames = {}
    # Handle both possible structures
    items = data if isinstance(data, list) else data.get("relationships_following", [])
    for item in items:
        # New export format: title at top level
        username = item.get("title")
        timestamp = None
        # Also check string_list_data (some export versions use this)
        for entry in item.get("string_list_data", []):
            if entry.get("value"):
                username = entry["value"]
                timestamp = entry.get("timestamp")
        if username:
            usernames[username.lower()] = {
                "username": username,
                "timestamp": timestamp,
            }
    return usernames


def load_followers(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    usernames = {}
    items = data if isinstance(data, list) else []
    for item in items:
        for entry in item.get("string_list_data", []):
            username = entry.get("value")
            timestamp = entry.get("timestamp")
            if username:
                usernames[username.lower()] = {
                    "username": username,
                    "timestamp": timestamp,
                }
    return usernames


def format_ts(ts):
    if not ts:
        return ""
    try:
        return datetime.utcfromtimestamp(int(ts)).strftime("%Y-%m-%d")
    except (ValueError, OSError):
        return ""


def print_section(title, usernames_dict, show_date=False):
    print(f"\n{'='*50}")
    print(f"  {title} ({len(usernames_dict)})")
    print(f"{'='*50}")
    if not usernames_dict:
        print("  (none)")
        return
    for key in sorted(usernames_dict):
        info = usernames_dict[key]
        line = f"  {info['username']}"
        if show_date:
            date = format_ts(info.get("timestamp"))
            if date:
                line += f"  [{date}]"
        print(line)


def main():
    # Auto-detect files
    followers_path = find_file(["followers_1.json", "followers*.json"])
    following_path = find_file(["following.json", "following*.json"])

    if not followers_path:
        print("Error: Could not find followers file (expected followers_1.json).")
        print("Make sure your Instagram data export files are in the same folder as this script.")
        sys.exit(1)
    if not following_path:
        print("Error: Could not find following file (expected following.json).")
        sys.exit(1)

    print(f"Loading: {followers_path}  +  {following_path}")

    try:
        followers = load_followers(followers_path)
        following = load_following(following_path)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)

    not_following_back = {k: v for k, v in following.items() if k not in followers}
    not_followed_back  = {k: v for k, v in followers.items() if k not in following}
    mutual             = {k: v for k, v in following.items() if k in followers}

    print_section("Not following you back (you follow them, they don't follow you)",
                  not_following_back, show_date=True)
    print_section("You don't follow back (they follow you, you don't follow them)",
                  not_followed_back, show_date=True)
    print_section("Mutual follows", mutual)

    print(f"\n{'='*50}")
    print(f"  Summary")
    print(f"{'='*50}")
    print(f"  Following:            {len(following)}")
    print(f"  Followers:            {len(followers)}")
    print(f"  Mutual:               {len(mutual)}")
    print(f"  Not following back:   {len(not_following_back)}")
    print(f"  You don't follow back:{len(not_followed_back)}")

    # Optional: save not-following-back to a text file
    out_path = "not_following_back.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"Not following you back — {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC\n")
        f.write("=" * 50 + "\n")
        for key in sorted(not_following_back):
            info = not_following_back[key]
            date = format_ts(info.get("timestamp"))
            line = info['username']
            if date:
                line += f"  [{date}]"
            f.write(line + "\n")
    print(f"\n  Saved to: {out_path}")


if __name__ == "__main__":
    main()
