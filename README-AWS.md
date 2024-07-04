# A basic introduction to Anyscale and AWS Managed Airflow

## 1. Getting airflow up and running

1. Create an S3 bucket that will be used by Amazon Managed Airflow (MWAA).
2. Create a requirements.txt file (a sample is in the /aws folder)
3. Upload to the S3 bucket using the S3 UI or AWS CLI.
4. Use the AWS UI to Launch Amazon Managed Airflow (MWAA).
    1. When asked to identify/create an S3 bucket for Airflow, make sure the bucket created in step 1 is used.
    2. When asked to identify the location for the requirements.txt file, point at the `s3://<bucketname>/requirements.txt` that you uploaded in step 3.
    3. When asked to identify the dags folder, make sure that you include a trailing `/` - ex: `s3://<bucketname>/dags/`

This will need a VPC with private subnets, not the default for AWS Anyscale Clouds created with `anyscale cloud setup`. This can be accomplished with the TF Modules if wanting to run in the same VPC, however it shouldn't be a requirement for Airflow.

**Note:** This takes 20-30min to create

## 2. Authenticating to anyscale
#### 1. Generate an anyscale platform API Key
1. Go to the anyscale console
2. Click on your username in the top right corner and select `API Keys`.
3. Select the 'AI Platform' tab and click 'Create'

#### 2. Add the Anyscale Airflow Provider
1. Create a requirements.txt (sample in `/aws/requirements.txt`)
2. Upload the requirements.txt file to the S3 bucket created for use with MWAA
3. [Edit the MWAA Configuration](https://docs.aws.amazon.com/mwaa/latest/userguide/working-dags-dependencies.html#configuring-dag-dependencies-installing) to point to the requirements.txt


#### 2. Add the API Key to airflow
1. Go to the AWS Airflow page, click on the Open Airflow UI to connect to the Airflow webserver, and click on `Admin` in the top menu bar.
2. Click on `Connections` and then `+`.
3. Fill in the following fields:
    - Connection Id: `anyscale`
    - Conn Type: `Anyscale`
    - API Key: `<your API Key>`


## 3. Running a simple DAG

### Checkout the dag under `dags/sample_anyscale_job_workflow.py`
This is a simple DAG that runs a job on anyscale. It uses the `SubmitAnyscaleJob` operator to run a job on anyscale. 

### Running the DAG
1. Upload the contents of dags to S3. ex cli command: `aws s3 cp dags/ s3://<bucketname>/dags/ --recursive
2. Click on the `trigger` button next to the `anyscale_job` DAG.
3. Click on the `Graph View` tab to see the progress of the DAG.
4. Click on the `Logs` tab to see the logs of the DAG.
5. Navigate to the Anyscale job page to see the job running.