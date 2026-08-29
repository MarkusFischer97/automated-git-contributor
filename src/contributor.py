import json
from datetime import datetime, timezone
from pathlib import Path


COUNTER_FILE = Path(__file__).parent.parent / "data" / "counter.json"


def load_counter():
    with COUNTER_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_counter(data):
    with COUNTER_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


README_FILE = Path(__file__).parent.parent / "README.md"


def update_readme(data):
    with README_FILE.open("r", encoding="utf-8") as file:
        content = file.read()

    start_marker = "<!-- AUTO-STATUS:START -->"
    end_marker = "<!-- AUTO-STATUS:END -->"

    last_run = datetime.fromisoformat(data["last_run"])
    formatted_last_run = last_run.strftime("%d %B %Y, %H:%M %Z")

    status = (
        f"{start_marker}\n\n"
        f"Run count: {data['run_count']}  \n\n"
        f"Last run: {formatted_last_run}\n\n"
        f"{end_marker}"
    )

    if start_marker not in content or end_marker not in content:
        raise ValueError(
            "README is missing the required AUTO-STATUS markers."
        )

    start = content.index(start_marker)
    end = content.index(end_marker) + len(end_marker)

    updated_content = content[:start] + status + content[end:]

    with README_FILE.open("w", encoding="utf-8") as file:
        file.write(updated_content)


def main():
    data = load_counter()

    data["run_count"] += 1
    data["last_run"] = datetime.now(timezone.utc).isoformat()

    save_counter(data)

    update_readme(data)

    print(f"Automated contributor run #{data['run_count']}")
    print(f"Last run: {data['last_run']}")


if __name__ == "__main__":
    main()