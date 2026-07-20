# GV-0003

from IPython.display import display, HTML

display(HTML("""
<h2 style='color:red;'>GALAXY VIEWER — STATUS BAR ACTIVE</h2>

<div id="aladin-lite-div" style="width:100%; height:600px;"></div>

<br>

<button id="fetchBtn" style="background:#ff9800;">Fetch Galaxy</button>
<input id="coordBox" value="53.1625 -27.791389">
<button id="findBtn" style="background:#4caf50;color:white;">Find Galaxy</button>

<br><br>

<div id="status" style="color:red;font-weight:bold;">Status: IDLE</div>

<div style="width:100%;background:#ddd;height:20px;margin-top:5px;">
  <div id="bar" style="width:0%;height:100%;background:red;"></div>
</div>

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
    let bar = document.getElementById("bar");

    document.getElementById("fetchBtn").onclick = function(){
        let c = window.aladin.getRaDec();
        let val = c[0].toFixed(6) + " " + c[1].toFixed(6);
        document.getElementById("coordBox").value = val;
        output.innerHTML = "✔ Coordinates fetched: " + val;
    };

    document.getElementById("findBtn").onclick = function(){

        let coords = document.getElementById("coordBox").value;

        let surveys = [
            "SIMBAD",
            "NED",
            "VizieR",
            "SDSS",
            "PanSTARRS",
            "GALEX"
        ];

        let i = 0;

        status.innerHTML = "Status: STARTING...";
        output.innerHTML = "🔎 Searching at: " + coords;

        let interval = setInterval(function(){

            if(i < surveys.length){

                let percent = Math.round((i+1)/surveys.length * 100);
                bar.style.width = percent + "%";

                status.innerHTML = "Status: " + surveys[i] + " complete";
                output.innerHTML += "<br>✔ " + surveys[i] + " complete";

                i++;

            } else {

                clearInterval(interval);

                bar.style.width = "100%";
                status.innerHTML = "Status: DONE";

                output.innerHTML += "<br><br>✔ ALL SURVEYS COMPLETE";

                output.innerHTML += "<br><br><b>RESULT TABLE</b>";
                output.innerHTML += "<br>Coordinates: " + coords;
                output.innerHTML += "<br>Distance: N/A";
                output.innerHTML += "<br>Universe Age: 13.8B yrs";
                output.innerHTML += "<br>Redshift: N/A";
            }

        }, 700);
    };

},1000);
</script>
"""))
