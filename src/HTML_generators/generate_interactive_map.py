import os

def generate_interactive_map(objects, path, file_name):
    data = []
    for obj in objects:
        data.append(
            {
                "name": obj.name,
                "category": obj.category,
                "coords": obj.coords,
                "id": obj.id
            }
        )

    html = f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/css/interactive_map_style.css">
    <title>Интерактивная карта</title>
</head>

<body>
    <div class="zoom-buttons">
        <button id="zoom-in" onclick="zoomIn()">+</button>
        <button id="zoom-out" onclick="zoomOut()">-</button>
    </div>
    <svg id="map" width="1100" height="1100"></svg>

    <script src="https://d3js.org/d3.v7.min.js"></script>
    <script>
        var objects = {data};
    </script>
    <script src="/static/scripts/interactive_map_scripts.js"></script>
</body>

</html>
"""
    if not os.path.exists(path):
        os.mkdir(path)
    with open(f"{path}/{file_name}", 'w', encoding="utf-8") as file:
        file.write(html)
