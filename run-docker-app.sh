# Version of the app
v=$1

# Maps port 8501 of the container into 8502 of the local host
container_id=$(docker run -d -p 8502:8501 ciaa/novelty:$v)

cleanup() {
    echo -e "\nStopping and removing the container..."
    docker stop "$container_id" > /dev/null
    docker rm "$container_id" > /dev/null
    exit 0
}

trap cleanup SIGINT

echo "Container is running. Press Ctrl + C to stop and remove it."
while true
do
  sleep 1
done