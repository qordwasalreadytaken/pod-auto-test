import json
import os
import sys

# Force flush to see output in GitHub Actions
sys.stdout.reconfigure(line_buffering=True)
print("✅ Runnin build_pages.py...")

# Confirm current directory contents 
print("📂 Current directory:")
for f in os.listdir("."):
    print(" -", f)

# Check if hc_ladder.json exists
if not os.path.exists("hc_ladder.json"):
    print("❌ hc_ladder.json not found!")
    sys.exit(1)
else:
    print("✅ Found hc_ladder.json")

# Load data
with open("hc_ladder.json") as f:
    characters = json.load(f)

print(f"✅ Loaded {len(characters)} characters")

# Build HTML
lines = [
    "<!DOCTYPE html>",
    "<html><head><title>Hardcore Ladder</title></head><body>",
    "<h1>Hardcore Ladder Characters</h1>",
    "<table border='1' cellpadding='5'>",
    "<tr><th>Name</th><th>Title</th><th>Class</th><th>Level</th><th>Life</th><th>FCR</th><th>MF</th></tr>"
]

for char in characters:
    name = char.get("Name", "Unknown")
    title = char.get("Title", "")
    cls = char.get("Class", "Unknown")
    level = char.get("Stats", {}).get("Level", "?")
    life = char.get("Stats", {}).get("Life", "?")
    fcr = char.get("Bonus", {}).get("FasterCastRate", 0)
    mf = char.get("Bonus", {}).get("MagicFind", 0)

    lines.append(f"<tr><td>{name}</td><td>{title}</td><td>{cls}</td><td>{level}</td><td>{life}</td><td>{fcr}%</td><td>{mf}%</td></tr>")

lines.extend(["</table>", "</body></html>"])

# Write output
with open("index.html", "w") as f:
    f.write("\n".join(lines))

print("✅ index.html generated successfully")
