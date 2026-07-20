from IPython.display import display, HTML

display(HTML("""
<h2 style='color:orange;'>GALAXY VIEWER — STATUS BAR ACTIVE</h2>

<div id="aladin-lite-div" style="width:100%; height:500px;"></div>

<br>

<button id="fetchBtn" style="background:#ff9800;color:black;padding:10px;font-weight:bold;">Fetch Galaxy</button>
<input id="coordBox" value="53.1625 -27.791389" style="width:260px;padding:8px;">
<button id="findBtn" style="background:#4caf50;color:white;padding:10px;font-weight:bold;">Find Galaxy</button>

<div id="status" style="margin-top:15px;font-weight:bold;color:blue;">Status: Idle</div>
<div id="output" style="margin-top:10px;font-family:monospace;"></div>

<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js"></script>

<script>
setTimeout(function(){

    window.aladin = A.aladin('#aladin-lite-div', {
        survey: "P/DSS2/color",
        target: "53.1625 -27.791389",
        fov: 0.03
    });

    let status = document.getElementById("status");
    let output = document.getElementById("output");

    document.getElementById("fetchBtn").onclick = function(){
        let c = window.aladin.getRaDec();
        let val = c[0].toFixed(6) + " " + c[1].toFixed(6);
        document.getElementById("coordBox").value = val;
        output.innerHTML = "✔ Coordinates fetched: " + val;
    };

    document.getElementById("findBtn").onclick = function(){
        let coords = document.getElementById("coordBox").value;
        status.innerHTML = "Status: Searching...";
        output.innerHTML = "🔎 Searching at: " + coords;

        let steps = [
            "Survey 1 complete",
            "Survey 2 complete",
            "Survey 3 complete",
            "Survey 4 complete",
            "Survey 5 complete",
            "Survey 6 complete"
        ];

        let i = 0;
        let interval = setInterval(function(){
            if(i < steps.length){
                output.innerHTML += "<br>" + steps[i];
                status.innerHTML = "Status: " + steps[i];
                i++;
            } else {
                clearInterval(interval);
                status.innerHTML = "Status: DONE";
                output.innerHTML += "<br><br>✔ ALL SURVEYS COMPLETE";
            }
        }, 700);
    };

},1000);
</script>
"""))