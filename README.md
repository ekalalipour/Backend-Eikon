<font size='7'>#Backend-Eikon#</font><br>
<font size='4'>This repository contains a simple ETL pipeline implemented in Python using Flask. The application allows you to process CSV files, derive features from them, and upload the processed data into a PostgreSQL database table.</font>

<font size='4'>##Installation##</font><br>
Clone this repository to your local machine.
Make sure you have Docker installed and running.

Build and Run the Docker Container
To build and run the Docker container, follow these steps:

1) Open a terminal and navigate to the project directory.
2) Run the following command to build the Docker image: docker build -t backend-eikon .
3) Once the image is built, run the following command to start the container: docker run -p 8080:8080 backend-eikon

<font size='4'>__API Endpoints:__</font>

<font size='3'>GET Request</font><br>
  This endpoint retrieves the summary of experiments, including the total number of experiments per user, the average number of experiments, and    the most commonly experimented compound for each user. URL: http://127.0.0.1:8080/experiment_summary

<font size='3'>POST Request(triggers the etl procces)</font><br>
  After running the docker image, you can use Postman to send a post request to trigger the etl process and send the data to database.              URL: http://127.0.0.1:8080/etl
  
  This endpoint triggers the ETL process. It loads the CSV files, processes them to derive features, and uploads the data into the PostgreSQL       database table. Note that the table will be truncated before entering the new data to ensure freshness.

<font size='4'>__Database Query__</font><br>
  The PostgreSQL database used in this application was created using ElephantSQL, a managed PostgreSQL database service.
  To verify that the data has been successfully uploaded to the PostgreSQL database, you can run the following query: 
    __SELECT * FROM experiment_summary;__

  Here's the query used to create the table:

  __CREATE TABLE experiment_summary (
    user_id INTEGER PRIMARY KEY,
    total_experiments INTEGER,
    average_experiments FLOAT,
    most_common_compound_structure TEXT[]
  );__



