# FastAPI with GraphQL example app

# Based on code from:
Check out [this repo](https://github.com/moluwole/fastapi-graphql)

# How to use this repository

1. Fork/Clone repo

2. Build docker images for project

```sh
docker-compose build .
```

3. Run project in containers

```sh
docker-compose up -d
```

4. Exec into api docker container

```
docker exec -ti graphql-api bash
```

5. Run database migrations

```
masonite-orm migrate
```

Navigate to [http://localhost:5002/graphql](http://localhost:5002/graphql).