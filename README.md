## Quick get started guide:
1. Create your Python virtualenv
2. Run this:
```
docker run -e POSTGRES_USER=postgres -e POSTGRESS_PASSWORD=<pass> -e POSTGRES_DB=ads -p 5345:5432 -d postgres
```
3. (Optional) Get a Telegram Bot token & add it to `.env`
4. Complete the `.env` as needed. Run `export $(cat .env)`
5. Run your scraper with: `scrapy crawl <scraper_name>

## Quick note:
This makes use of a notification bot, through the `SpiderBotCallback`, you can disable it in the settings if you want no bot interaction (just data gathering).

# Deployment:
Remember to set database and bot specific variables as environment variable before starting! Open .env file and complete it, then run `source .env`

Database:
- POSTGRES_PASSWORD
- POSTGRES_HOST (if needed)
- POSTGRES_PORT (if needed)

Bot:
- BOT_USER_SETTINGS_FILE
- BOT_TOKEN


#### Zero to hero steps:
1. Install the following:
    * git
    * docker
    * run-one
2. Clone the repository
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
    # Build the image for all scrapers
    docker build -t scraper .
    
    # Build the image for running individual scrapers
    docker build -f Dockerfile-single-spider -t single_scraper .

### To run postgres only (on other port but same volume):

Please see the docker_env.list file and set the following:
    
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=<pass>
    POSTGRES_DB=realestate            // database name
    PGDATA=/var/lib/postgresql/data   // postgres docker volume mount point

Then, you can use this command to start the postgres instance with the path to the env file:

    docker run --env-file "<path/to/docker_env.list>"  -p 5345:5432 -d postgres

### To run scrapers only (make sure you have postgres and httpcache volume up first):
    docker run --network=host -v httpcache:/var/lib/httpcache/ scraper

### Restoring psql backups
    cat <dump_name>.sql | docker exec -i <docker-postgres-container> psql -U postgres -W -d realestate
    
### To rescrape all urls from httpcache (you need to edit the spider name in Dockerfile-only-httpcache first):
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
    To run all scrapers you need only this line:
    * * * * * run-one docker run --network=host -v httpcache:/var/lib/httpcache/ scraper
    To run individual scrapers you'll need one of these for each scraper:
    * * * * * run-one docker run --network=host -v httpcache:/var/lib/httpcache/ -e spider_name=<spider name> single_scraper

    Don't forget the backup script!
    * * * * * run-one /path/to/backup.sh

Disclaimer:
This software and the data gathered/being sent is for my personal use only. I am not responsible for any damages cause by proper/improper use of the software.
This software is in development phase and subject to change. 
Any data retrieved or stored does not contain any personal identifying information. Please contact me concerning data usage clarification/requests of removal.
