# API Deployment

### Python Setup
To set up python run `pip install requirements.txt` to install python packages.

### Run on Local Device
To deploy the API on local machine run `python sentimentAnalysis.py`.
API will be deployed on `localhost:5000`

### Run on Docker
* Build Docker Container
    ```
    docker build . -t investitweets:v1
    ```
* Run Docker Container
    ```
    docker run -p 5000:5000 investitweets:v1
    ```




