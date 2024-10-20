# Building a Full DevOps Pipeline for a Resume Counter Web Application Using Docker, GitHub Actions, and EC2

## Overview of the Project:
In this project, I’ve been working on building and automating a full CI/CD pipeline for a simple web application—a resume counter app. The frontend of the app displays a static webpage, and the backend, built using Flask, manages a MongoDB database that keeps track of how many times the page has been viewed.

The purpose of this project is to not only create the application itself but also to understand and implement modern DevOps best practices. These practices include containerization using Docker, continuous integration and deployment using GitHub Actions, and hosting on a cloud environment, specifically AWS EC2.

The goal is to ensure that every time I update my code (frontend or backend), it triggers an automated process that builds my application, updates my Docker images, and deploys them to my EC2 instance—without any manual intervention.

## Tools and Technologies Used:
Docker: To containerize both the frontend (served by Nginx) and the backend (Flask API). This ensures the app can run consistently across different environments.

* GitHub Actions: For automating the build, push, and deployment of the application using a CI/CD pipeline.

* AWS EC2: The cloud instance used to host the application.

* MongoDB: To store and retrieve the page views for the resume counter.

* GitHub Container Registry (GHCR): Used to store the built Docker images before deploying them to the EC2 instance.

# Project Breakdown for Beginners:
Let’s break down the full process of creating this automated CI/CD pipeline.

## Step 1: Writing the Application Code
The app is split into two main components: the frontend and the backend.

- Frontend: This is the part of the app the user interacts with. It’s a static webpage written in HTML/CSS that displays a welcome message and a counter for how many times the page has been viewed.

- Backend: The backend is a Flask-based API that connects to a MongoDB database. It increments the view counter every time the frontend makes a request to it and then sends the updated view count back to be displayed on the frontend.

## Step 2: Dockerizing the Application
Docker allows you to package your application and its dependencies into a container, ensuring that it runs the same way on any machine.For this project, I created Dockerfiles for both the frontend and backend:

**Frontend Dockerfile**: This Dockerfile uses Nginx to serve the static HTML files:
```
FROM nginx:alpine
COPY frontend/ /usr/share/nginx/html
EXPOSE 80
```

**Backend Dockerfile**: This Dockerfile sets up the Flask app, installs the necessary dependencies, and exposes port 5000:
```
FROM python:3.9-slim
WORKDIR /app
COPY backend/ /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "main.py"]
```

## Step 3: Building CI/CD Pipeline with GitHub Actions
To automate the deployment process, I created a GitHub Actions workflow (main.yml) that does the following:

- **Triggers the Workflow:** The workflow is triggered every time a push is made to the main branch or manually through the GitHub interface.
- **Checkout the Code:** The workflow first checks out the latest code from the repository using the actions/checkout@v3 action.
- **Build the Docker Images:** The workflow builds separate Docker images for the frontend and backend using their respective Dockerfiles.
- **Push Images to GitHub Container Registry:** After building the Docker images, they are pushed to GHCR so that they can be pulled later for deployment.
- **Copy the Deployment Script to EC2:**

A deploy script (deploy.sh) is copied to the EC2 instance. This script automates the process of pulling the latest Docker images and restarting the containers.
- **Deploy to EC2:** The deploy script is executed via SSH, ensuring the updated application is pulled and deployed on the EC2 instance.
Checkout the mainyml documentation here to see full breakdown [mainyml.md](mainyml.md)


## Step 4: Deployment on AWS EC2
The EC2 instance serves as the cloud host for both the frontend and backend.

### Deploy Script (deploy.sh): 
This script stops and removes the old Docker containers, pulls the latest images from GHCR, and starts new containers. Here’s an example of how it looks:

``` 
#!/bin/bash

# Frontend deployment
echo "Stopping and removing old frontend containers..."
docker stop frontend || true
docker rm frontend || true

echo "Pulling latest frontend images from GHCR..."
docker pull ghcr.io/mariammbello/resume-frontend:latest

echo "Starting Frontend container..."
docker run -d --name frontend -p 80:80 ghcr.io/mariammbello/resume-frontend:latest

# Backend deployment
echo "Stopping and removing old backend containers..."
docker stop backend || true
docker rm backend || true

echo "Pulling latest backend images from GHCR..."
docker pull ghcr.io/mariammbello/resume-backend:latest

echo "Starting Backend container..."
docker run -d --name backend -p 5000:5000 \
  -e MONGO_CONNECTION_STRING="mongodb://mongodb:27017/" \
  -e MONGO_DATABASE_NAME="resume_challenge" \
  ghcr.io/mariammbello/resume-backend:latest

echo "Deployment complete!"
```

## Step 5: Automating with Docker Compose
While the above deploy script works fine, we can further simplify and optimize this process using Docker Compose. Docker Compose allows us to manage multiple containers with a single YAML configuration file.

Here’s an example of a Docker Compose file for this project:

```
version: '3'
services:
  frontend:
    image: ghcr.io/mariammbello/resume-frontend:latest
    ports:
      - "80:80"
    networks:
      - mynetwork

  backend:
    image: ghcr.io/mariammbello/resume-backend:latest
    environment:
      MONGO_CONNECTION_STRING: "mongodb://mongodb:27017/"
      MONGO_DATABASE_NAME: "resume_challenge"
    ports:
      - "5000:5000"
    networks:
      - mynetwork

  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    networks:
      - mynetwork

networks:
  mynetwork:
    driver: bridge

``` 
In this docker-compose.yml, we define all three services (frontend, backend, and MongoDB) and ensure they can communicate via a network (mynetwork). Docker Compose makes it easier to spin up or manage the entire app with a single command: ``` docker-compose up -d ```

## Requirements for Setting This Up
**Codebase:**
* Frontend code (HTML/CSS/JS) in the frontend/ directory.
* Backend code (Flask app) in the backend/ directory.

**Docker Setup:**
* Docker installed locally and on your EC2 instance.
* Docker Compose installed on the EC2 instance.

**GitHub Actions Setup:**
* A GitHub repository with the above folder structure.
* GitHub Secrets added for HOST, KEY, GITHUB_TOKEN, etc.

**EC2 Instance:**
* An Ubuntu EC2 instance with Docker and Docker Compose installed.
* Open the required ports (80 for frontend, 5000 for backend) in the EC2 security groups.

**MongoDB:**
* MongoDB running as part of the Docker Compose network.

## Conclusion
This project illustrates how to build, containerize, and automate the deployment of a simple web application. By leveraging Docker, GitHub Actions, and EC2, I’ve created a fully automated pipeline that updates my app every time I push new changes to GitHub.

For those new to DevOps, this project covers a wide array of concepts, from Docker containerization to CI/CD automation. Each step, from coding to deployment, is crucial in modern development workflows.

Now, with a working setup in place, the next step could be adding security features, such as SSL certificates, and optimizing the setup for scalability and performance, especially as the application grows in complexity.

This experience not only deepens your knowledge of deploying cloud applications but also sets the foundation for building more advanced and scalable systems in the future!