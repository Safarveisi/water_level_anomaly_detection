# Unsupervised Novelty Detection Using the Local Outlier Factor (LOF)

Novelty detection is a critical technique used in scenarios where a set of "normal" data is available and the aim is to identify "new" or "novel" data points that deviate from this established norm. Unlike outlier detection, which assumes the dataset may be mostly clean while containing a few outliers, novelty detection presumes the reference data for training is devoid of any anomalies. This approach is highly beneficial in environments where the concept of "novel" is relative to a predefined baseline of normalcy, and is applicable as incoming data is continuously assessed.

## Usage

To use the application, run the Docker container in detached mode. The app is deployed as a [Streamlit](https://streamlit.io/) dashboard and is accessible on port `8502` of your localhost. Users can select a station UUID from the `selectbox` to view water level measurements over the last hour (the prediction window) and detect any novelties. The unsupervised machine learning model is trained on a six-hour reference period, allowing it to identify novelties within the prediction window effectively.

```bash
# Make sure the docker image is available
./build-image.sh <tag of the docker image>
# Run a container in detached mode
./run-docker-app.sh <tag of the docker image>
```

## Monotirng the app logs

We use `Filebeat --> Elasticsearch --> Kibana` stack to monitor the logs of the docker container spawned above (logs are located at `/var/lib/docker/containers` of the host machine). All three services will run in their own docker containers. First, change the working directory to `/elastic-start-local` and run the following command to start a single-node Elastic cluster: 

```bash
./start.sh
```

To stop the cluster:

```bash
./stop.sh
```

To remove volumes and containers (Filebeat, Elasticsearch, and Kibana):

```bash
./uninstall.sh
```

## About the API

[PEGELONLINE](https://www.pegelonline.wsv.de/webservice/ueberblick) provides web services that publish real-time raw data of various hydrological parameters, such as water levels, from federal waterways for up to 30 days retrospectively. These web services are free to use, although the data is provided "as is" without verification from the managing waterway and shipping offices.

## Table of files and directories

|           File/Directory        |             Description           |
|:-------------------------------:|:---------------------------------:|
| `water_level_anomaly_detection` | Contains all source code for the application. |
| `.python-version` | Specifies the Python version used in app development. |
| `build-image.sh` | Script to build the Docker image; logs are directed to `build.log`. |
| `Dockerfile` | Provides instructions to build the Docker image. |
| `run-docker-app.sh` | Script to launch the Docker container and instantiate the app. |
| `setup-env.sh` | Script to set up the virtual environment and install development dependencies in the dev mode. | 