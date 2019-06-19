# Payment MVP

### Sample .env
```
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB_ENDPOINT=db
POSTGRES_PORT=5432
POSTGRES_DB=db

APP_HOST=0.0.0.0
APP_PORT=8080

ADMIN_LOGIN=admin
ADMIN_PASSWORD=admin
```

### Run
```
$ docker-compose up
```

### Default `admin` user will be created
Consider `admin` user as a default user to take fee from all external transfers between users.
