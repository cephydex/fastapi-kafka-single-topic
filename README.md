# FastAPI with GraphQL example app

# Based on code from:
Check out [this repo](https://github.com/cephydex/fastapi-kafka-single-topic)

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

Navigate to: 
[http://localhost:5002/graphql](http://localhost:5002/graphql).

[kafka UI](http://localhost:8070).<br/>
[Producer service](http://localhost:8074/docs).<br/>
[Consumer 1 service](http://localhost:8071/docs).<br/>
[Consumer 2 service](http://localhost:8072/docs).<br/>
[Consumer 3 service](http://localhost:8073/docs).<br/>
<!-- 8070 - Kafka UI -->
<!-- 8071 - Consumer 1 service -->
<!-- 8072 - Consumer 2 service -->
<!-- 8073 - Consumer 3 service -->
<!-- 8074 - Producer service -->