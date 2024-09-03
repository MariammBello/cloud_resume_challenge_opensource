# Flask MongoDB Dockerized Application

This project is a simple web application built with Python's Flask framework and MongoDB. The application tracks the number of views by storing and updating a counter in a MongoDB database. The entire setup is containerized using Docker, making it easy to run anywhere.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Set Up MongoDB](#2-set-up-mongodb)
  - [3. Build and Run the Application](#3-build-and-run-the-application)
- [Environment Variables](#environment-variables)
- [Testing the Application](#testing-the-application)
- [Stopping the Containers](#stopping-the-containers)
- [Deploying the Application](#deploying-the-application)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/) if you don't have it installed.
- **Git**: [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to clone the repository.

## Getting Started

Follow these steps to get the application up and running on your local machine.

### 1. Clone the Repository

First, clone this repository to your local machine:


### 2. Set Up MongoDB

You need to run a MongoDB container to store the data for the application. Use the following command to start a MongoDB container:

```bash
docker run -d --name mongodb-container -p 27017:27017 \
-e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
-e MONGO_INITDB_ROOT_PASSWORD=secret \
mongo
```

### 3. Build and Run the Application

Now, let's build and run the Flask application:

1. **Build the Docker Image**:

   ```bash
   docker build -t flask-mongo-app .
   ```

2. **Run the Flask Container**:

   ```bash
   docker run -d -p 5000:5000 --name flask-app-container --network function-app-network \
   -e MONGO_CONNECTION_STRING="mongodb://mongoadmin:secret@mongodb-container:27017/" \
   -e MONGO_DATABASE_NAME="resume_challenge" \
   flask-mongo-app
   ```

## Environment Variables

The application uses the following environment variables:

- **`MONGO_CONNECTION_STRING`**: The connection string for MongoDB, including the credentials and the host.
- **`MONGO_DATABASE_NAME`**: The name of the database where the data will be stored.

These can be set in the Dockerfile or passed at runtime when starting the container.

## Testing the Application

After the containers are running, you can test the application by visiting the `/views` endpoint in your browser or using `curl`:

```bash
curl http://localhost:5000/views
```

This will return a JSON object with the current view count, which increments each time you access the endpoint.

## Stopping the Containers

To stop the running containers, use the following commands:

```bash
docker stop flask-app-container
docker stop mongodb-container
```

To remove the containers:

```bash
docker rm flask-app-container
docker rm mongodb-container
```

## Deploying the Application

You can deploy this application to any platform that supports Docker. Simply build the Docker image and push it to a container registry like Docker Hub, AWS ECR, or Azure Container Registry. Then, you can deploy the image using a cloud service like AWS ECS, Azure Kubernetes Service (AKS), or Google Kubernetes Engine (GKE).
