import json

with open("hc_ladder.json") as f:
    data = json.load(f)

with open("index.html", "w") as f:
    f.write(f"<html><body><h1>{data['message']}</h1></body></html>")
