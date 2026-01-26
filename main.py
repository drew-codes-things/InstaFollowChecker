import json

FOLLOWERS_FILE = "followers_1.json"
FOLLOWING_FILE = "following.json"


def load_following(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    usernames = set()
    for item in data.get("relationships_following", []):
        username = item.get("title")
        if username:
            usernames.add(username.lower())

    return usernames


def load_followers(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    usernames = set()
    for item in data:
        for entry in item.get("string_list_data", []):
            username = entry.get("value")
            if username:
                usernames.add(username.lower())

    return usernames


followers = load_followers(FOLLOWERS_FILE)
following = load_following(FOLLOWING_FILE)

not_following_back = sorted(following - followers)

print(f"\nNot following you back ({len(not_following_back)}):\n")
for user in not_following_back:
    print(user)
