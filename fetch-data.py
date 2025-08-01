import json
data = {"message": "Hello from API!"}
with open("hc_ladder.json", "w") as f:
    json.dump(data, f, indent=2)
