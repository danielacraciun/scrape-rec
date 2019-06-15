# Deployment:
Remember to set POSTGRES_PASSWORD as environment variable before starting!

Run: `export POSTGRES_PASSWORD=<pass>`

### Create volumes:
    docker volume create pgdata
    docker volume create httpcache

### Build the docker image:
    docker build -t scraper .

### Run docker compose:
    docker-compose up -d

### To run postgres only (on other port but same volume):
    docker run -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=<pass> -e POSTGRES_DB=realestate -e PGDATA=/var/lib/postgresql/data -p 5345:5432 -d postgres

### To run scrapers only (make sure you have postgres and httpcache volume up first):
    docker run --network=host -v httpcache:/var/lib/httpcache/ scraper
