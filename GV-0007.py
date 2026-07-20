# GV-0007
# Galaxy Viewer — Aladin Lite with Fetch + Find buttons (clean build)

from IPython.display import display, HTML

html = """
<div style="width:100%; max-width:900px; margin:auto;">

    <h3>Galaxy Viewer — GV-0007</h3>

    <div id="aladin-lite-div" style="width:100%; height:600px; border:1px solid #ccc;"></div>

    <br>

    <input id="coordBox" type="text" value="53.174798 -27.799445" style="width:60%; padding:6px;"/>

    <button onclick="fetchCoords()">Fetch</button>
    <button onclick="findGalaxy()">Find Galaxy</button>

    <div id="status" style="margin-top:10px; font-family:monospace;"></div>

</div>

<script src="https://aladin.u-strasbg.fr/AladinLite/api/v3/latest/aladin.js"></script>

<script>

let aladin;

function initAladin() {
    aladin = A.aladin('#aladin-lite-div', {
        survey: "P/DSS2/color",
        target: "53.174798 -27.799445",
        fov: 0.02
    });
}

function fetchCoords() {
    let c = aladin.getRaDec();
    let val = c[0].toFixed(6) + " " + c[1].toFixed(6);
    document.getElementById("coordBox").value = val;
    document.getElementById("status").innerHTML = "✔ Coordinates fetched: " + val;
}

function findGalaxy() {

    let coords = document.getElementById("coordBox").value;

    document.getElementById("status").innerHTML = "🔎 Searching: " + coords;

    aladin.gotoObject(coords);

    setTimeout(function(){
        document.getElementById("status").innerHTML = "✔ Loaded target: " + coords;
    }, 1000);
}

setTimeout(initAladin, 500);

</script>
"""

display(HTML(html))
