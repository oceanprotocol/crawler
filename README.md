
# OCEAN CRAWLER

This tool will be used to crawl and extract data from condo oriented websites

## Requirements

Docker & docker-compose installed


## Configuration

Create the following directories:
```
~/db/mongo
~/db/sql
```


**If you are using a M1 Macbook, add ```platform: linux/amd64``` in ```docker-compose.yml```  under ```mysql-db```

## Deployment

Go to root directory and run
```docker-compose  --env-file .connections.env up --build --force-recreate -d```

## Post deployment

Create a database in MongoDB named int-parser and 2 collections called ```config``` and ```spider-config```
Insert the test data from [here](mongodb-test-data.json) to  ```config```  and [here](spider-config-test-data.json) to ```spider-config```

In mysql, insert the data from [here](sql-test-data.sql)
## Run


In order to run, go to [kafka-monitor](kafka-monitor) folder and run ```sh feedItem.sh```

For live logs visit ```localhost:105```

## License
GNU General Public License v3.0 or later

See LICENSE to see the full text.
