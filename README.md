# A basic introduction to Anyscale and Airflow

## 1. Getting airflow up and running
Run `docker-compose up` in the root directory of this repository. This will start the airflow webserver and scheduler. You can access the webserver at `localhost:8080`. The default username and password are `airflow` and `airflow` respectively.

## 2. Authenticating to anyscale
#### 1. Generate an anyscale platform API Key
1. Go to the anyscale console
2. Click on your username in the top right corner and select `API Keys`.
3. Select the 'AI Platform' tab and click 'Create'

#### 2. Add the API Key to airflow
1. Go to the airflow webserver and click on `Admin` in the top right corner.
2. Click on `Connections` and then `Create`.
3. Fill in the following fields:
    - Conn Id: `anyscale`
    - Conn Type: `Anyscale`
    - Password: `<your API Key>`

## 3. Running a simple DAG

### Checkout the dag under `dags/sample_anyscale_job_workflow.py`
This is a simple DAG that runs a job on anyscale. It uses the `SubmitAnyscaleJob` operator to run a job on anyscale. 

### Running the DAG
1. Go to the airflow webserver and click on `DAGs` in the top left corner.
2. Click on the `trigger` button next to the `anyscale_job` DAG.
3. Click on the `Graph View` tab to see the progress of the DAG.
4. Click on the `Logs` tab to see the logs of the DAG.
5. Navigate to the Anyscale job page to see the job running.
