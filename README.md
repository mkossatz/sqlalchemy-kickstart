```Shell
podman run \
    --name postgres \
    -d \
    -p 5432:5432 \
    -e POSTGRES_PASSWORD=toor \
    -e POSTGRES_USER=root \
    -e POSTGRES_DB=database-name \
    docker.io/postgres:13-alpine
```