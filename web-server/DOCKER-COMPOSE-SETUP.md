## Start docker-compose file

docker-compose up -d

#### Update container configuration

If you want to change some container configuration:

```shell
docker-compose up -d --no-deps --build {service-name}
```

#### Connect to container:

```shell
docker-compose exec {service-name} bash
```
rabbitmq:
```shell
docker-compose exec rabbitmq3 bash
```
mongodb:
```shell
docker-compose exec mongodb_container bash
```

#### Restart everything:

```shell
docker-compose restart
```

#### Stop everything:

```shell
docker-compose stop
```

#### Remove everything:

```shell
docker-compose down -v
```

