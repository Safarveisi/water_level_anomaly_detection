v=$1

docker build --no-cache --progress=plain -t ciaa/novelty:$v . &> build.log