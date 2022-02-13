import json

POST_PATH = "posts.json"


def _open_json():
    with open(POST_PATH, encoding='utf-8') as f:
        json_data = json.load(f)

    return json_data


def save_to_json(post):
    json_data = _open_json()
    json_data.append(post)

    try:
        with open(POST_PATH, 'w') as f:
            json.dump(json_data, f)
    except Exception:
        return False

    return True


def find_tags():
    json_data = _open_json()
    tags = []
    for item in json_data:
        text = item["content"].split()
        for word in text:
            if word.startswith("#"):
                word = word.translate({ord(i): None for i in '#!,.?'})
                tags.append(word)

    return tags


def find_posts_by_tag(tag):
    json_data = _open_json()
    posts = []
    for item in json_data:
        text = item["content"].split()
        for word in text:
            if word.startswith("#"):
                if word.translate({ord(i): None for i in '#!,.?'}) == tag:
                    posts.append(item)

    return posts
