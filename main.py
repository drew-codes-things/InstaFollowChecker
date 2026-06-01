import argparse
import csv
import glob
import json
import os
import sys
from datetime import datetime, timezone


USE_COLOR = True

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def col(text, code):
    return f"{code}{text}{RESET}" if USE_COLOR else text


def find_file(folder, candidates):
    for pattern in candidates:
        direct_matches = glob.glob(os.path.join(folder, pattern))
        if direct_matches:
            return direct_matches[0]
        recursive_matches = glob.glob(os.path.join(folder, "**", pattern), recursive=True)
        if recursive_matches:
            return recursive_matches[0]
    return None


def find_all_followers_files(folder):
    direct = glob.glob(os.path.join(folder, "followers_*.json"))
    recursive = glob.glob(os.path.join(folder, "**", "followers_*.json"), recursive=True)
    matches = sorted(set(direct + recursive))
    return matches


def iter_string_list_data_entries(payload):
    """Recursively yield dict entries that contain Instagram string_list_data."""
    if isinstance(payload, list):
        for item in payload:
            yield from iter_string_list_data_entries(item)
        return

    if not isinstance(payload, dict):
        return

    sld = payload.get("string_list_data")
    if isinstance(sld, list) and sld:
        for entry in sld:
            if isinstance(entry, dict):
                yield entry

    for value in payload.values():
        yield from iter_string_list_data_entries(value)


def entries_to_user_map(entries):
    users = {}
    for entry in entries:
        username = entry.get("value")
        timestamp = entry.get("timestamp")
        if not username:
            continue
        users[username.lower()] = {
            "username": username,
            "timestamp": timestamp,
        }
    return users


def load_following(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return entries_to_user_map(iter_string_list_data_entries(data))


def load_followers_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return entries_to_user_map(iter_string_list_data_entries(data))


def load_followers(folder):
    files = find_all_followers_files(folder)
    if not files:
        return {}
    merged = {}
    for path in files:
        merged.update(load_followers_from_file(path))
    if len(files) > 1:
        print(f"  Merged {len(files)} followers files: {', '.join(os.path.basename(p) for p in files)}")
    return merged


def format_ts(ts):
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).strftime("%Y-%m-%d")
    except (ValueError, OSError, TypeError):
        return ""


def profile_url(username):
    return f"https://www.instagram.com/{username}/"


def print_section(title, usernames_dict, show_date=False, color=None):
    header = f"  {title} ({len(usernames_dict)})"
    print(f"\n{'='*50}")
    print(col(header, color) if color else header)
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


def write_txt(path, title, usernames_dict, show_date=False):
    with open(path, "w", encoding="utf-8") as f:
        now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        f.write(f"{title} -- {now}\n")
        f.write("=" * 50 + "\n")
        if not usernames_dict:
            f.write("(none)\n")
            return
        for key in sorted(usernames_dict):
            info = usernames_dict[key]
            line = info["username"]
            if show_date:
                date = format_ts(info.get("timestamp"))
                if date:
                    line += f"  [{date}]"
            f.write(line + "\n")


def write_combined_report(path, not_following_back, not_followed_back, mutual, summary):
    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Instagram Follow Report -- {now}\n")
        f.write("=" * 50 + "\n\n")

        sections = [
            ("Not following you back", not_following_back, True),
            ("You don't follow back", not_followed_back, True),
            ("Mutual follows", mutual, False),
        ]
        for title, data, show_date in sections:
            f.write(f"\n{title} ({len(data)})\n")
            f.write("-" * 40 + "\n")
            if not data:
                f.write("  (none)\n")
            else:
                for key in sorted(data):
                    info = data[key]
                    line = info["username"]
                    if show_date:
                        date = format_ts(info.get("timestamp"))
                        if date:
                            line += f"  [{date}]"
                    f.write(line + "\n")

        f.write("\nSummary\n")
        f.write("-" * 40 + "\n")
        for label, val in summary:
            f.write(f"  {label:<26}{val}\n")


def write_csv(path, usernames_dict):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "followed_since", "profile_url"])
        writer.writeheader()
        for key in sorted(usernames_dict):
            info = usernames_dict[key]
            writer.writerow({
                "username": info["username"],
                "followed_since": format_ts(info.get("timestamp")),
                "profile_url": profile_url(info["username"]),
            })


def parse_args():
    p = argparse.ArgumentParser(
        description="Analyse Instagram follower/following JSON exports."
    )
    p.add_argument(
        "data_dir",
        nargs="?",
        default=None,
        help=(
            "Path to the folder containing followers/following export files "
            "(defaults to the current working directory)"
        ),
    )
    p.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colour in terminal output",
    )
    return p.parse_args()


def main():
    global USE_COLOR
    args = parse_args()
    if args.no_color:
        USE_COLOR = False

    folder = args.data_dir if args.data_dir else os.getcwd()
    if not os.path.isdir(folder):
        print(f"Error: folder not found: {folder}")
        sys.exit(1)

    followers_files = find_all_followers_files(folder)
    following_path = find_file(folder, ["following.json", "following_*.json", "following*.json"])

    if not followers_files:
        print("Error: Could not find any followers file (expected followers_1.json, followers_2.json, etc.).")
        sys.exit(1)
    if not following_path:
        print("Error: Could not find following file (expected following.json).")
        sys.exit(1)

    print(f"Loading followers from: {', '.join(os.path.basename(p) for p in followers_files)}")
    print(f"Loading following from: {os.path.basename(following_path)}")

    try:
        followers = load_followers(folder)
        following = load_following(following_path)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)

    not_following_back = {k: v for k, v in following.items() if k not in followers}
    not_followed_back = {k: v for k, v in followers.items() if k not in following}
    mutual = {k: v for k, v in following.items() if k in followers}

    print_section(
        "Not following you back (you follow them, they don't follow you)",
        not_following_back, show_date=True, color=RED,
    )
    print_section(
        "You don't follow back (they follow you, you don't follow them)",
        not_followed_back, show_date=True, color=YELLOW,
    )
    print_section("Mutual follows", mutual, color=GREEN)

    summary = [
        ("Following:", len(following)),
        ("Followers:", len(followers)),
        ("Mutual:", len(mutual)),
        ("Not following back:", len(not_following_back)),
        ("You don't follow back:", len(not_followed_back)),
    ]
    print(f"\n{'='*50}")
    print("  Summary")
    print(f"{'='*50}")
    for label, val in summary:
        print(f"  {label:<26}{val}")

    saved = []

    write_txt(
        os.path.join(folder, "not_following_back.txt"),
        "Not following you back", not_following_back, show_date=True,
    )
    saved.append("not_following_back.txt")

    write_txt(
        os.path.join(folder, "not_followed_back.txt"),
        "You don't follow back", not_followed_back, show_date=True,
    )
    saved.append("not_followed_back.txt")

    write_txt(
        os.path.join(folder, "mutual.txt"),
        "Mutual follows", mutual,
    )
    saved.append("mutual.txt")

    write_combined_report(
        os.path.join(folder, "report.txt"),
        not_following_back, not_followed_back, mutual, summary,
    )
    saved.append("report.txt")

    write_csv(
        os.path.join(folder, "not_following_back.csv"),
        not_following_back,
    )
    saved.append("not_following_back.csv")

    print(f"\n  Saved to {folder}/")
    for name in saved:
        print(f"    {name}")


if __name__ == "__main__":
    main()
