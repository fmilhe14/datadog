This repository contains the code for the Datadog techical homework.

# What has been done ? 

I have chosen to create a simple Flask API to ask for the retrieval of page_views reports.
Once reports are asked, the API will create several tasks and publish it in a queue. 
Some workers will pull the messages from the queue and try to download and aggregate the reports.
Once the report has been successfully treated, top 25 articles for the given day and hour by total pageviews are 
saved in a CSV file.

The architecture of the code is the following : 

Flask -> Queue -> Workers -> Local Storage

And, in order to get the state of a task, flask application and workers write in a Document oriented database 
(in our development case, a TinyDB)

- FYI : Some reports pre aggregated are available in the data/reports folder.

# How to run the code ? 

In order to launch the API:

- If you have docker, docker-compose :  

`make run`

- Otherwise: 

```
virtualenv --no-site-packages -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python -m datadog
```

If you wish to test it, here some curl examples : 

The following query will ask for reports from  2020-01-01 15:00:00 until 2020-01-01 19:00:00.

```
curl -X GET \
  http://127.0.0.1:8080/ask_page_views \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 1b049522-62e0-4d57-b7ec-d93d91ed7018' \
  -H 'cache-control: no-cache' \
  -d '{
	"start_date": "2020010115",
	"end_date": "2020010119"
}'
```

You could also ask for just one report : 

The following query will ask for reports of 2020-01-01 15:00:00.

```
curl -X GET \
  http://127.0.0.1:8080/ask_page_views \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 1b049522-62e0-4d57-b7ec-d93d91ed7018' \
  -H 'cache-control: no-cache' \
  -d '{
	"start_date": "2020010115"
}'
```

If you wish to know the state of a certain task : 

```
curl -X GET \
  http://127.0.0.1:8080/get_task_state \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 466fbce9-bf73-4bcf-afa8-b5a2c00556eb' \
  -H 'cache-control: no-cache' \
  -d '{
	"date": "2020010115"
}'
```

If the task has been created, the output will look like : 

```
{
    "data_path": "./data/reports/2020-01-01 15:00:00.csv",
    "date": "2020010115",
    "max_tries": 1,
    "status": "success",
    "try_count": 0
}
```

Otherwise, you will get prompted this message : 

```
{
    "message": "This task does not exist"
}
```

If you wish to launch the tests : 

- If you have docker, docker-compose :  


`make test`


- Otherwise : 

```
virtualenv --no-site-packages -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
py.test -s tests tests/unit -vv
```

# Additional questions :

## What additional things would you want to operate this application in a production setting?

In order to run the application in production, several improvements need to be done : 

- First of all, the configuration should be removed from the main method.
- Implement a MongoDB database as TinyDB's purpopse isn't to be used in production. The MongoDB should be 
hosted in the cloud and have replication.
- Implement a different queue. Indeed, we will want to distribute our application. For that, we could you different
message brokers, such as a Redis queue for instance.
- We would need to implement a new writer, as the current one is currently writing locally. We could store the data 
in S3, GCS ...
- We would need to deploy the API and the workers differently as they do not scale equally. For that we could 
use Kubernetes. We would deploy the API and expose it thought a service + ingress for it to be accessible 
to external IPs. For the workers we would probably need to have several pods, each pod will read from the same 
message broker and will be responsible for the handling of a specific task.

## What might change about your solution if this application needed to run automatically for each hour of the day?
To do so, the best solution would be to use a tool such as Apache Airflow, or Luigi.
We would create a DAG, and schedule it to run on an hourly basis. 
The DAG would be made of a single pod operator that could run on a Kubernetes cluster. 
This pod would be schedule to run on a node, execute the export task, then kill itself.

This pod could do one of the following : 

- A first solution could be to make a call to the API that we have created. The API being on an other cluster
and reachable by our pod.
- An other solution could be to only launch the worker with the desired date on the pod, as we do not really 
need the API.


## How would you test this application?

In order to do an end-to-end test, I would need to create a Mock for the Wikimedia client in order to 
return the same file everytime. 

We would need to start the api, start a worker, simulate a code to the API and at the end we'd need 
to test if the report is equal to what was expected.

Furthermore, we should also test the case where the report has already been computed. 

## How you’d improve on this application design?

A better move could be to distribute the computation on several nodes. We could do a simple 
map reduce job (map on the pair (domain, page)) to obtain such elements : [(.de, page), [1,3,4,5]], reduce it to get
the count views. After that we could just group on the domain key and take the 25 top values.

This job could be triggered via our worflow management system (airflow, luigi) every hour.

This job could be written using Apache Spark or Apache Beam.