# Building a Full DevOps Pipeline for a Cloud Resume Counter Application Using Docker, GitHub Actions, and EC2

## Overview of the Project:
This project focuses on creating and automating a full CI/CD (Continuous Integration/ Continuous Deployment) pipeline for a simple web application—a resume counter app. The frontend is a static webpage, and the backend, built using Flask, connects to a MongoDB database to track and display how many times the page has been viewed.

Originally inspired by the Cloud Resume Challenge, this project has evolved to embrace Free and Open Source Software (FOSS) principles, aiming to minimize dependencies on paid cloud services and reduce costs. The original project, which used proprietary services like Azure and Cosmos DB, was prone to limitations, including paid features and service disruptions when subscriptions lapsed. This version, however, replaces those components with free-tier AWS EC2 and open-source solutions like MongoDB, making it more scalable and cost-effective while maintaining functionality.

The project demonstrates the ability to build scalable cloud applications using open-source tools and services while maintaining a free-tier cloud infrastructure on AWS.

### Project Goals:
- **Automation:** Ensure that every time code (frontend or backend) is updated, an automated process is triggered to build the application, update Docker images, and deploy them to an AWS EC2 instance.
- **FOSS and Low Cost:** Replace paid and proprietary services with free-tier, open-source alternatives without compromising on functionality. The application should run on free-tier cloud infrastructure and use open-source tools.
- **Application Features:** Users can view the resume webpage and see a real-time page view counter that updates with each visit.

### Tools and Technologies Used:
- **Amazon EC2 (Free Tier):** The web app is hosted on an AWS EC2 instance. EC2 provides scalable compute capacity in the cloud, and the free-tier option ensures that hosting is cost-free for the first year.
- **Docker:** Both the frontend (served via Nginx) and the backend (Flask API) are containerized using Docker. Docker ensures consistency in how the app runs across different environments.
- **GitHub Actions**: Used for continuous integration and deployment (CI/CD), GitHub Actions automates the build, push, and deployment process. It builds Docker images, pushes them to GitHub Container Registry (GHCR), and deploys the app to EC2.
- **MongoDB:** A NoSQL database used to store and retrieve the page view count. MongoDB runs in a Docker container, making it easy to deploy and manage as part of the app.
- **GitHub Container Registry (GHCR):** Used to store built Docker images before they are deployed to EC2.
- **Frontend (HTML/CSS/JavaScript):** The frontend is a static webpage that interacts with the backend API to display the updated page view count.
- **Backend (Flask in Python):** The backend API, built with Flask, handles requests from the frontend and interacts with the MongoDB database to update the page view counter.

### How the System Works:
The application consists of three core components—frontend, backend, and database—each of which is containerized using Docker. The backend fetches and updates the page view count stored in MongoDB and sends the updated count to the frontend, which displays it on a static HTML webpage.

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
see [Codes Documentation](codesdoc.md) for details of code

## Step 3: Building CI/CD Pipeline with GitHub Actions
To automate the deployment process, I created a GitHub Actions workflow (main.yml) that does the following:

- **Triggers the Workflow:** The workflow is triggered every time a push is made to the main branch or manually through the GitHub interface.
- **Checkout the Code:** The workflow first checks out the latest code from the repository using the actions/checkout@v3 action.
- **Build the Docker Images:** The workflow builds separate Docker images for the frontend and backend using their respective Dockerfiles.
- **Push Images to GitHub Container Registry:** After building the Docker images, they are pushed to GHCR so that they can be pulled later for deployment.
- **Copy the Deployment Script to EC2:**

A deploy script (deploy.sh) is copied to the EC2 instance. This script automates the process of pulling the latest Docker images and restarting the containers.
- **Deploy to EC2:** The deploy script is executed via SSH, ensuring the updated application is pulled and deployed on the EC2 instance.
Checkout the [Codes Documentation](codesdoc.md) documentation here to see full breakdown 


## Step 4: Deployment on AWS EC2
The EC2 instance serves as the cloud host for both the frontend and backend.

### Deploy Script (deploy.sh): 
This script stops and removes the old Docker containers, pulls the latest images from GHCR, and starts new containers. Here’s an example of how it looks:

``` 
#!/bin/bash

# Stop and remove old containers
echo "Stopping and removing old containers..."
docker compose down || true

# Pull latest images from GHCR
echo "Pulling latest images from GHCR..."
docker pull ghcr.io/mariammbello/resume-frontend:latest
docker pull ghcr.io/mariammbello/resume-backend:latest

# Start everything using Docker Compose
echo "Starting containers..."
docker compose up -d --pull always

echo "Update complete!"

```

## Step 5: Automating with Docker Compose
We can further simplify and optimize this process using Docker Compose. Docker Compose allows us to manage multiple containers with a single YAML configuration file.

Here’s an example of a Docker Compose file for this project:

```
version: '3'

services:
  frontend:
    # build:
    #   context: ./frontend    # Directory containing the frontend Dockerfile and build context
    #   dockerfile: Dockerfile  # Specify the Dockerfile to use (optional if named "Dockerfile")
    image: ghcr.io/mariammbello/resume-frontend:latest
    ports:
      - "80:80"
    networks:
      - mynetwork

  backend:
    # build:
    #   context: ./backend     # Directory containing the backend Dockerfile and build context
    #   dockerfile: Dockerfile  # Specify the Dockerfile to use (optional if named "Dockerfile")
    image: ghcr.io/mariammbello/resume-backend:latest
    ports:
      - "5000:5000"
    environment:
      MONGO_CONNECTION_STRING: mongodb://mongodb:27017/
      MONGO_DATABASE_NAME: resume_challenge
    networks:
      - mynetwork

  mongodb:
    image: mongo:latest
    networks:
      - mynetwork
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db  # Volume mount for MongoDB data persistence

networks:
  mynetwork:
    driver: bridge

volumes:
  mongo-data:  # This defines the mongo-data volume

``` 
In this docker-compose.yml, we define all three services (frontend, backend, and MongoDB) and ensure they can communicate via a network (mynetwork). Docker Compose makes it easier to spin up or manage the entire app with a single command: ``` docker-compose up -d ```

In the Docker Compose file, I've switched from using build (commented out) to image. Here’s why:

Image refers to pre-built Docker images that are pulled from a registry (e.g., GHCR). This is faster and more efficient in production environments because the images are already built.
Build is necessary when you are actively developing and making frequent changes to the code. You only need to build once and push the image to a registry, then use image in subsequent deployments.

## Requirements for Setting This Up
**Codebase:**
* Frontend code (HTML/CSS/JS) in the frontend/ directory.
* Backend code (Flask app) in the backend/ directory.

**Docker Setup:**
* Docker installed locally and on your EC2 instance.
* Docker Compose installed on the EC2 instance.

**GitHub Actions Setup:**
* A GitHub repository with the above folder structure.
* GitHub Secrets added for HOST, KEY,etc.

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