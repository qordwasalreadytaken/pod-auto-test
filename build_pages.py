with open("index.html", "w") as f:
    f.write("""
<!DOCTYPE html>
<html>
<head><title>Dynamic JSON Demo</title></head>
<body>
  <h1 id="output">Loading...</h1>
  <script>
    fetch("hc_ladder.json")
      .then(res => res.json())
      .then(data => {
        document.getElementById("output").textContent = data.message;
      });
  </script>
</body>
</html>
""")
