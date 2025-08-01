import json

with open("hc_ladder.json") as f:
    data = json.load(f)

lines = [
    "<!DOCTYPE html>",
    "<html><head><title>Ladder</title></head><body>",
    f"<h1>{data['ladder']} Top Characters</h1>",
    "<ul>",
]

for char in data["top_characters"]:
    lines.append(f"<li>{char['name']} ({char['class']}, Level {char['level']})</li>")

lines.extend(["</ul>", "</body></html>"])

with open("index.html", "w") as f:
    f.write("\n".join(lines))
