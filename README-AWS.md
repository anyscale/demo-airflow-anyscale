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
This is a simple DAG that runs a job on anyscale. It uses the `SubmitAnyscaleJob` operator to run a job on anyscale. Make sure that the `ANYSCALE_CONN_ID` matches the name of the Connection you created above.

### Running the DAG
1. Upload the contents of dags to S3. ex cli command: `aws s3 cp dags/ s3://<bucketname>/dags/ --recursive`
2. Click the `trigger` button next to the `anyscale_job` DAG.
3. Click the `Graph View` tab to see the progress of the DAG.
4. Click the `Logs` tab to see the logs of the DAG.
5. Navigate to the Anyscale job page to see the job running.

## Additional Notes for AWS

The above configuration depends on the security of the MWAA environment to secure the API key. This can also be done with Secrets Manager.
AWS has [provided a guide](https://docs.aws.amazon.com/mwaa/latest/userguide/connections-secrets-manager.html) on how to add AWS Secrets Manager
access to MWAA. This requires small changes to the IAM Policy associated with the Role used by MWAA (granting it access to read secrets), and editing
the MWAA environment to include some advanced optional configurations. Using Secrets Manager, you no longer need to create the connection in the
Airflow Connection Admin section. Rough steps are as follows:

1. Modify the IAM Policy for the MWAA Role to include Secrets Manager access. ex policy which limits access to secrets in a given account, in a given region, and that start with `airflow/`:

```
{
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetResourcePolicy",
                "secretsmanager:GetSecretValue",
                "secretsmanager:DescribeSecret",
                "secretsmanager:ListSecretVersionIds"
            ],
            "Resource": "arn:aws:secretsmanager:us-west-2:367974485317:secret:airflow/*"
        },
        {
            "Effect": "Allow",
            "Action": "secretsmanager:ListSecrets",
            "Resource": "*"
        }
```

2. Modify the Airflow environment Configuration. Changing this setting takes ~20min for AWS to update the environment. The following example installs the appropriate secrets backend provider as well as tells Airflow to look for connections in Secrets Manager that are going to be named with the following prefix: `airflow/connections`:

```
secrets.backend : airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
secrets.backend_kwargs : {"connections_prefix" : "airflow/connections", "variables_prefix" : "airflow/variables"}
```

3. Create a secret in AWS Secrets Manager. This should be an "Other" type of Secret and created with Key/Pair values. A full list of valid options can be found in the [Airflow AWS Secrets Manager Provider](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/secrets-backends/aws-secrets-manager.html) documentation.
    1. For the Anyscale integration, you will need `conn_type: anyscale`, `conn_id: <your_connection_name>`, and `key: <anyscale_api_key>`. 
    2. Naming the Secret should include `airflow/connections/<anyscale_connection_name>` where `<anyscale_connection_name>` is the name you'd like to use for the connection. ex:
```
conn_type: anyscale
conn_id: anyscale_secret
key: aph0_xxxxxxxxxx

Secret Name: airflow/connections/anyscale_secret
```

4. Modify the DAG to use the name of the connection stored in secrets manager. The Secrets Manager Connection configuration will search for connections under the connections prefix value configured in Step 2. An example of this is in `anyscale_job_aws_secretsmanager.py`