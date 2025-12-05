cd ./ || { echo "Dizine geçilemedi."; exit 1; }

# if container not exsist
if [ ! "$(docker ps -a -q -f name=backup_psql)" ]; then
    # if image not exsist, create new image
    if [ -z "$(docker images -q backup_psql)" ]; then
        echo "Image not found. Creating new image..."
        docker build -t backup_psql .
    fi
    # start new container
    echo "Container starting..."
    docker run -d --name backup_psql backup_psql
else
    # if exsist container just started
    if [ "$(docker ps -aq -f status=exited -f name=backup_psql)" ]; then
        echo "Find stopped container, starting..."
        docker start backup_psql
    else
        echo "Container already running."
    fi
fi
