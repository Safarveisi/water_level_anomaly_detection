# Use this script for testing/debugging purposes only

# TAG
v=$1

docker build . --no-cache --progress=plain --file Dockerfile --tag ciaa/anomaly:$v &> build_image.log