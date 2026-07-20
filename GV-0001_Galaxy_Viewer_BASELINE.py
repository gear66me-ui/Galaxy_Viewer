
from IPython.display import display, HTML

display(HTML("""
<h2 style='color:orange;'>GALAXY VIEWER — GV-0001 BASELINE</h2>

<div id="aladin-lite-div" style="width:100%; height:600px;"></div>

<br>

<button id="fetchBtn" style="background:#ff9800;color:black;padding:10px;font-weight:bold;">
Fetch Galaxy
</button>

<input id="coordBox" value="53.1625 -27.791389" style="width:260px;padding:8px;">

<button id="findBtn" style="background:#4caf50;color:white;padding:10px;font-weight:bold;">
Find Galaxy
</button>

<div id="output" style="margin-top:10px;font-family:monospace;"></div>

<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js"></script>

<script>
setTimeout(function(){

    if (typeof A === "undefined") {
        document.getElementById("output").innerHTML = "❌ Aladin failed to load";
        return;
    }

    window.aladin = A.aladin('#aladin-lite-div', {
        survey: "P/DSS2/color",
        target: "53.1625 -27.791389",
        fov: 0.03
    });

    let output = document.getElementById("output");

    document.getElementById("fetchBtn").onclick = function(){
        let c = window.aladin.getRaDec();
        let val = c[0].toFixed(6) + " " + c[1].toFixed(6);
        document.getElementById("coordBox").value = val;
        output.innerHTML = "✔ Coordinates fetched: " + val;
    };

    document.getElementById("findBtn").onclick = function(){
        let coords = document.getElementById("coordBox").value;
        output.innerHTML = "🔎 Searching at: " + coords + "<br>⏳ Engine coming in GV-0002";
    };

},1000);
</script>
"""))
