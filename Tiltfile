# -*- mode: Python -*

# import restart_process extension
# load('ext://restart_process', 'docker_build_with_restart')

# Define how to build the Docker image for the FastAPI application
congrats = "🎉 Congrats, you ran a live_update! 🎉"
#docker_build_with_restart(
docker_build(
    "server", 
    context=".", 
    dockerfile="configs/server.Dockerfile",
    ignore=[],
    entrypoint=["sh", "-c", "./start.sh"],
    live_update=[
        sync("src/", "/app/"),
        run("echo '%s'" % congrats, trigger="src/"),
        run("cd /app && pip install --no-cache-dir --ignore-installed -r requirements.txt", trigger="./src/requirements.txt"),
        run("./restart.sh")
    ],
)

# Load Kubernetes manifests
k8s_yaml("configs/mongodb-statefulset.yaml")
k8s_yaml("configs/mongodb-init-job.yaml")
k8s_yaml("configs/server-deployment.yaml")

# Wait for MongoDB ReplicaSet initialization
k8s_resource("mongo-init", resource_deps=["mongodb"])

# Attach the FastAPI service to Tilt
k8s_resource("server", port_forwards=8000)