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


def get_env():
    """Detect where the app is running."""
    if os.environ.get("KUBERNETES_SERVICE_HOST"):
        return "kubernetes"
    if os.environ.get("AWS_EXECUTION_ENV") or \
            os.path.exists("/sys/hypervisor/uuid"):
        return "ec2"
    return "local"


@app.route("/")
def home():
    uptime = datetime.now() - START_TIME
    total_seconds = int(uptime.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.1)
    env = get_env()

    if env == "kubernetes":
        env_info = {
            "env_type": "Kubernetes",
            "hostname": socket.gethostname(),
            "pod_ip": socket.gethostbyname(socket.gethostname()),
            "namespace": os.environ.get("POD_NAMESPACE", "default"),
            "node_name": os.environ.get("NODE_NAME", "unknown"),
        }
    elif env == "ec2":
        env_info = {
            "env_type": "EC2",
            "hostname": socket.gethostname(),
            "pod_ip": socket.gethostbyname(socket.gethostname()),
            "namespace": None,
            "node_name": None,
        }
    else:
        env_info = {
            "env_type": "Local",
            "hostname": socket.gethostname(),
            "pod_ip": socket.gethostbyname(socket.gethostname()),
            "namespace": None,
            "node_name": None,
        }

    context = {
        "language": f"Python {sys.version.split()[0]}",
        "python_impl": platform.python_implementation(),
        "framework": f"Flask {flask.__version__}",
        "server": "Gunicorn",
        "port": "5000",
        "os": f"{platform.system()} {platform.machine()}",
        "uptime": f"{hours}h {minutes}m {seconds}s",
        "mem_used": round(mem.used / (1024 ** 2)),
        "mem_total": round(mem.total / (1024 ** 2)),
        "mem_pct": mem.percent,
        "cpu_pct": cpu,
        **env_info,
    }
    return render_template("index.html", **context)


if __name__ == "__main__":
    app.run(debug=False)
