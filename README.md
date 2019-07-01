# Deployment:

#### Zero to hero steps:
1. Install the following:
    * git
    * docker
    * run-one
2. Clone the repostory
3. Build the scraper docker image
4. Create pgdata and httpcache docker volumes

For debugging, to run scrapers manually:
1. Install:
    * python2 pip
    * virtualenvwrapper
2. Create python3 virtualenvironment
3. Install requirements.txt

## Docker

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

### To rescrape all urls from httpcache you need to edit the spider name in Dockerfile-only-httpcache and then:
    docker build -t scraper_only_httpcache . -f Dockerfile-only-httpcache
    docker run --network=host -v httpcache:/var/lib/httpcache/ scraper_only_httpcache


## Crontab    

### Make sure the current user is in the docker group, add it if needed:
    sudo usermod -aG docker $USER

### Make sure you have run-one installed, this is used to ensure that only one instance of the scraper is running at any given time
    sudo apt-get install run-one

### Optional: If you have the virtualenv created you can run the python script
    python setup_crontab.py

### This is the crontab command, set this in a user's crontab (the user must be in the docker group):
    * * * * * run-one docker run --network=host -v httpcache:/var/lib/httpcache/ scraper
    * * * * * run-one /path/to/backup.sh