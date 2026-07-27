from IPython.display import HTML, display

# GV-beta-0002B – wrapper that loads 2A and patches the Target-button click‑handler so SIMBAD pointer works.

import urllib.request, ssl, re, runpy, types, sys, textwrap

RAW = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0002.py"
code = urllib.request.urlopen(RAW, context=ssl._create_unverified_context()).read().decode()

patched = re.sub(
    r"proxy\.addEventListener\([^)]*?=>\s*{[^}]*?}\);",
    textwrap.dedent(r"""
        proxy.addEventListener("click", () => {
            const al = window.aladin_cosmic_command_test;
            if (al?.useSimbadPointer)      al.useSimbadPointer(true);   // Aladin ≥3.8
            else if (al?.setMode)          al.setMode('simbadPointer'); // older API
            else {
                const btn = findNativeSimbadEngine?.();
                btn?.dispatchEvent(new MouseEvent("click", {bubbles:true,cancelable:true,view:window}));
            }
        });
    """).rstrip(),
    code, count=1
)

# execute patched viewer in the current namespace
exec(compile(patched, "GV-beta-0002B", "exec"), globals())