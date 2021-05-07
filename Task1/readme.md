Refer to the attached diagram, here are the details of data pipeline

1. Assuming all files are sent and stored in bucket A, we create a bucket B and create a DAG in cloud composer(airflow) to validate the file(e.g. format, extension ). Once files pass the validation , the DAG will move appropriated files to bucket B. We can set a fixed schedule of this DAG like run every 5 mins depending on the files ingestion activities.
2. A cloud function (with trigger event = object created in bucket B) will be created so that once any objects are created in bucket B, the cloud function will trigger a DAG in composer. This DAG is responsible for grouping files according to date and sending them to the folder (name: yyyy-mm-dd) in bucket C. 
3. A DAG (consolidator) is responsible for consolidating data which is scheduled to run  periodically (every 10 mins/every hour/once a day, depends on how we group the data) and store the result in bucket D.



Remarks:
1. Regarding the scheduler, actually we can use cloud function + cloud scheduler instead of cloud composer given that the daily data volume is limited. However, cloud composer has a great UI and better logging and retry handling. Also it is auto scaling but only maximum 4GB memory and 9 mins running limitation on cloud function.Although composer is more expensive(it will create K8s clusters), for long term we should still adopt cloud composer.
2. An additional DAG / cloud function can be created for log collection(e.g. the error in consolidator DAG, the outdated files in bucket A. For monitoring, we can output these information for analysis. Also we can check airflow UI and stackdriver to see if any error exist in each components
3. When all components are set up, two main DAG(validation and consolidator) are scheduled. Once partners send files to bucket A, validation DAG will send files to bucket B. With any files sent to bucket B, cloud function will be triggered to group these files in bucket C and finally consolidator DAG will do the rest and save the result in bucket D. We can see No need to manually trigger.
4. For deployment , just make sure all service accounts of each component have the right to access each other.
5. To be cost effective, we can create a DAG to housekeep the files in all buckets after a retention period.
