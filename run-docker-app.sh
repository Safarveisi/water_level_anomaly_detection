# Use this script for testing purposes only (build image, but do not push to docker hub)

# Version of the app (image tag)
v=$1
target_image=ciaa/anomaly:$v
# Get all local docker images
images=$(docker images --format '{{.Repository}}:{{.Tag}}')

# Check if the target image already exists
if $(echo "$images" | grep -q "^${target_image}$"); then
  echo "Image $target_image exists. Creating the container ..."
else
  echo "Image $target_image does not exist. Creating the image ..."
  ./build-image.sh $v
fi

# Start a container and map port 8501 of the container into 8502 of the local host
container_id=$(docker run -d -p 8502:8501 $target_image)

cleanup() {
    echo -e "\nStopping and removing the container..."
    docker stop "$container_id" > /dev/null
    docker rm "$container_id" > /dev/null
    exit 0
}

# Trap ctrl-c
trap cleanup INT

echo "Container is running. Press Ctrl + C to stop and remove it."
while true
do
  sleep 1
done