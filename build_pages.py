import json

# Read from data.json (already created by fetch_data.py)
with open("hc_ladder.json") as f:
    data = json.load(f)

# Write an HTML page that includes the message
with open("index.html", "w") as f:
    f.write(f"""
<!DOCTYPE html>
<html>
<head><title>Generated Page</title></head>
<body>
  <h1>{data['message']}</h1>
</body>
</html>
""")
