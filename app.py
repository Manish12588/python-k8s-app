import os
import sys
import socket
import platform
from datetime import datetime

import flask
import psutil
from flask import Flask, render_template

app = Flask(__name__)
START_TIME = datetime.now()


@app.route("/")
def home():
    uptime = datetime.now() - START_TIME
    total_seconds = int(uptime.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.1)

    context = {
        "language": f"Python {sys.version.split()[0]}",
        "framework": f"Flask {flask.__version__}",
        "server": "Gunicorn",
        "port": "5000",
        "os": f"{platform.system()} {platform.machine()}",
        "python_impl": platform.python_implementation(),

        "hostname": socket.gethostname(),
        "pod_ip": socket.gethostbyname(socket.gethostname()),
        "namespace": os.environ.get("POD_NAMESPACE", "default"),
        "node_name": os.environ.get("NODE_NAME", "unknown"),
        "uptime": f"{hours}h {minutes}m {seconds}s",

        "mem_used": round(mem.used / (1024 ** 2)),
        "mem_total": round(mem.total / (1024 ** 2)),
        "mem_pct": mem.percent,
        "cpu_pct": cpu,
    }
    return render_template("index.html", **context)


#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000)  # nosec B104
if __name__ == "__main__":
    app.run(debug=True)