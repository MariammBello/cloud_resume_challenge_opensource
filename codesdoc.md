# Main.yml file breakdown
This is a break down for each part of the GitHub Actions workflow file (main.yml) step by step. This guide will explain each line and how it contributes to automating the CI/CD pipeline for deploying the frontend and backend of your application to an AWS EC2 instance. 

1. Workflow Name and Trigger
name: Deploy_Application
This specifies the name of the workflow. In this case, it's called Deploy_Application. This name appears in the GitHub Actions interface, making it easier to identify.

```
on:
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - 'frontend/**'
      - 'backend/**'
      - '.github/workflows/main.yml'
```

* on: This section defines when the workflow should be triggered. It listens for specific events.
* workflow_dispatch: This allows you to manually trigger the workflow from the GitHub interface.
* push: This triggers the workflow when changes are pushed to the main branch.
* branches: This limits the trigger to pushes made on the main branch only.
* paths: This defines which directories or files should trigger the workflow when changes are made. It watches changes in the frontend/, backend/, and .github/workflows/main.yml paths.

**2. Environment Variables**
```
env:
  FRONTEND_IMAGE_NAME: mariammbello/resume-frontend
  BACKEND_IMAGE_NAME: mariammbello/resume-backend
``` 
* env: This section defines environment variables that are reused throughout the workflow.
* FRONTEND_IMAGE_NAME: The name of the frontend Docker image that will be built and pushed to GitHub Container Registry (GHCR).
* BACKEND_IMAGE_NAME: The name of the backend Docker image that will be built and pushed to GHCR.

**3. Job Definition**
```
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
``` 

* jobs: This section defines the jobs that will run in this workflow.
* build-and-deploy: This is the name of the job that will handle both building and deploying your application.
* runs-on: Specifies the runner environment. ubuntu-latest means that the job will run on the latest version of Ubuntu.
* permissions: Specifies the permissions required to run the job.
* contents: read: Allows the job to read the repository content.
* packages: write: Allows the job to write packages to GHCR (GitHub Container Registry).

**4. Steps in the Job**
Each step performs a specific task in the job. Let's go through each step:
```
steps:
    - name: 'Checkout GitHub Action'
      uses: actions/checkout@v3
```

* name: This is a human-readable label for the step. In this case, it's called Checkout GitHub Action.
* uses: This specifies a pre-built action provided by GitHub. actions/checkout@v3 checks out (downloads) your repository's code so the workflow can access it. It's essential to do this before running any build commands.

```
    - name: 'Set up Docker Buildx'
      uses: docker/setup-buildx-action@v2
``` 

* Set up Docker Buildx: This step sets up Docker Buildx, a tool that enables advanced Docker builds, such as multi-platform builds and caching.
* uses: The docker/setup-buildx-action@v2 action prepares the environment to use Buildx for building Docker images.`

```
    - name: 'Login to GitHub Container Registry'
      run: echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
```

* Login to GitHub Container Registry: This step logs into GHCR, where the Docker images will be pushed.
* run: Runs a shell command. In this case: ``` ${{ secrets.GITHUB_TOKEN }}```: Retrieves a GitHub token stored as a secret in your repository settings. Secrets are sensitive values (like passwords or keys) that are securely stored and used in workflows.
* docker login: Logs into GHCR using the GitHub token and the GitHub actor (user or bot triggering the workflow).

**5. Building and Pushing Docker Images**
```
    - name: 'Build Frontend Docker Image'
      run: |
        docker build -t ghcr.io/${{ env.FRONTEND_IMAGE_NAME }}:latest -f frontend/Dockerfile .
```

* Build Frontend Docker Image: This step builds the frontend Docker image using the frontend/Dockerfile.
docker build: This command builds a Docker image.
* -t ghcr.io/${{ env.FRONTEND_IMAGE_NAME }}:latest: Tags the image with a name (GHCR path and image name) and marks it as the latest version.
* -f frontend/Dockerfile: Specifies the Dockerfile used to build the frontend image.
* . (dot): Refers to the build context, meaning the entire current directory is used for building the image.

```
    - name: 'Build Backend Docker Image'
      run: |
        docker build -t ghcr.io/${{ env.BACKEND_IMAGE_NAME }}:latest -f backend/Dockerfile .
```

* Build Backend Docker Image: This step builds the backend Docker image in a similar way to the frontend.
```
    - name: 'Push Frontend Docker Image'
      run: |
        docker push ghcr.io/${{ env.FRONTEND_IMAGE_NAME }}:latest
```
* Push Frontend Docker Image: Pushes the built frontend Docker image to GHCR so that it can be pulled later during deployment.
```
    - name: 'Push Backend Docker Image'
      run: |
        docker push ghcr.io/${{ env.BACKEND_IMAGE_NAME }}:latest
```
* Push Backend Docker Image: Pushes the built backend Docker image to GHCR.

**6. Deploying to EC2**
This section copies the deployment script to the EC2 instance and runs it via SSH.

```
    - name: 'Copy deploy.sh to EC2'
      uses: appleboy/scp-action@v0.1.7
      with:
        host: ${{ secrets.HOST }}
        username: ubuntu
        key: ${{ secrets.KEY }}
        port: 22
        source: "deploy.sh"
        target: /home/ubuntu
        strip_components: 0
        overwrite: true
``` 
* Copy deploy.sh to EC2: Copies the deploy.sh script from your repository to the EC2 instance.
* uses: The appleboy/scp-action@v0.1.7 is an action that securely copies files to a remote server using SCP (Secure Copy Protocol).
* host: Refers to the EC2 instance’s public IP address, stored in GitHub Secrets.
* username: Specifies the SSH username (ubuntu for EC2 instances).
* key: The private SSH key, securely stored in GitHub Secrets.
* source: The source file (deploy.sh) in your repository.
* target: The destination on the EC2 instance.
* strip_components: Removes leading path components from the source before copying. This is 0 because it is not required, since the script is not nested.
* overwrite: This ensures the file is overwritten

```
    - name: 'Deploy to EC2 via SSH'
      uses: appleboy/ssh-action@v1.0.3
      with:
        host: ${{ secrets.HOST }}
        username: ubuntu
        key: ${{ secrets.KEY }}
        port: 22
        script: |
          chmod +x /home/ubuntu/deploy.sh
          sudo sh /home/ubuntu/deploy.sh
```

* Deploy to EC2 via SSH: Connects to the EC2 instance using SSH and runs the deploy.sh script.
* uses: The appleboy/ssh-action@v1.0.3 action is used to run SSH commands on a remote server.
* chmod +x /home/ubuntu/deploy.sh: Makes the deploy.sh script executable.
* sudo sh /home/ubuntu/deploy.sh: Runs the deployment script with superuser privileges.

**Summary: How Secrets Work**
Secrets in GitHub: Secrets (like GITHUB_TOKEN, HOST, and KEY) are stored securely in your GitHub repository under Settings > Secrets. These secrets are injected into your workflow to ensure sensitive information (such as tokens, SSH keys, and IP addresses) is not exposed in the code.

How Secrets are Used: When GitHub runs your workflow, it retrieves these secrets and substitutes them into your code where they are referenced (e.g., secrets.GITHUB_TOKEN).

Final Thoughts
This workflow automates the entire process of building Docker images for both the frontend and backend, pushing them to GHCR, and deploying the latest versions to an EC2 instance via SSH. This setup ensures a continuous integration/continuous deployment (CI/CD) pipeline, eliminating the need for manual deployments.

For more details on GitHub Actions or Docker, you can refer to their official documentation:

GitHub Actions Docs
Docker Docs

# docker-compose.yml breakdown

Here’s a comprehensive breakdown of the docker-compose.yml file and what each line means, including the context for why each part is used

Breakdown of the docker-compose.yml File:
```
version: '3'
``` 
**version:** This defines the version of the Docker Compose file format you’re using. Version '3' is widely supported and commonly used in production environments. It ensures compatibility with various Docker Compose features and services.

**Frontend Service:**
```
services:
  frontend:
    image: ghcr.io/mariammbello/resume-frontend:latest
    ports:
      - "80:80"
    networks:
      - mynetwork
``` 
- **services:** This section defines the different services (containers) that make up your application. In this case, you have three services: frontend, backend, and MongoDB.

- **frontend: **This is the name of the service (container) that will run your frontend code. It serves the frontend of the resume counter app, which displays the static HTML.

- **image:** Instead of building the Docker image every time you deploy, we use a pre-built image stored in a container registry (GHCR - GitHub Container Registry).

```ghcr.io/mariammbello/resume-frontend```: The full path to the Docker image in the registry. The ```:latest```  tag ensures that the most recent version of the image is pulled. This speeds up deployment because you only need to rebuild the image when the code changes significantly.
ports: This defines port mappings between the container and the host machine.

- **"80:80":** The first 80 refers to the port on the host machine (the EC2 instance), and the second 80 refers to the port inside the container. This means that your frontend service will be accessible on port 80 of the EC2 instance.
- **networks:** This allows the frontend to communicate with other services (backend and MongoDB) on a shared Docker network.
- **mynetwork:** The network the frontend service will be part of, enabling communication with the backend and MongoDB.

**Backend Service:**
```
  backend:
    image: ghcr.io/mariammbello/resume-backend:latest
    ports:
      - "5000:5000"
    environment:
      MONGO_CONNECTION_STRING: mongodb://mongodb:27017/
      MONGO_DATABASE_NAME: resume_challenge
    networks:
      - mynetwork
``` 

- **backend:** This is the name of the service that will run the backend of your resume counter app. The backend interacts with the MongoDB database to store and retrieve the view counts.
- **image:** Like the frontend, the backend uses a pre-built image from the GitHub Container Registry.
```ghcr.io/mariammbello/resume-backend```: The Docker image path and the latest tag to ensure the most recent backend code is used.
- **ports:** This maps port 5000 of the EC2 instance to port 5000 in the container, allowing you to access the backend API via the public IP of the EC2 instance on port 5000.
- **environment**: These are environment variables passed into the container. Environment variables are used to configure the backend to connect to MongoDB.

- **MONGO_CONNECTION_STRING:** Defines the URL used by the backend to connect to the MongoDB instance. In this case, ```mongodb://mongodb:27017/``` refers to the MongoDB service (named mongodb in this Compose file) and the default MongoDB port (27017).

- **MONGO_DATABASE_NAME:** Specifies the name of the database where the data is stored, in this case, resume_challenge.
- **networks:** Like the frontend, the backend is also part of the mynetwork Docker network to allow communication with MongoDB and the frontend.

**MongoDB Service:**
```
  mongodb:
    image: mongo:latest
    networks:
      - mynetwork
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db`
``` 

- **mongodb:** This defines the MongoDB database service. MongoDB is used to store and manage the resume counter's data (e.g., the page view count).
- **image:** The image being used here is the latest official MongoDB image from Docker Hub.

- **mongo**: This pulls the most recent version of the MongoDB image.
**networks**: Like the frontend and backend, MongoDB is also part of the mynetwork Docker network to allow communication between all the services.
- **ports:** This maps port 27017 of the EC2 instance to port 27017 in the MongoDB container. MongoDB listens on this port by default, allowing the backend to connect to the database.
- **volumes**: This mounts a volume to persist MongoDB data.
- **mongo-data**:/data/db: This mounts the named volume mongo-data to the /data/db directory inside the MongoDB container. This ensures that the data stored in MongoDB is not lost when the container is stopped or removed.

**Network Definition:**
```
networks:
  mynetwork:
    driver: bridge
```
- **networks:** This section defines custom networks that services can use to communicate with each other.
- **mynetwork:** This is the name of the network used by all three services (frontend, backend, MongoDB). All services connected to the same network can communicate with each other by their service names (e.g., mongodb in this case).
- **driver**: bridge: The bridge network driver is the default driver used by Docker Compose. It creates an isolated network for all the services, allowing them to communicate internally without exposing unnecessary ports externally.

**Why Use image Instead of build:**
The build process is useful when you are actively developing code for the first time or testing in the local environment, without a need to push to the container registry. However, once the images are ready and stored in a container registry (e.g., GHCR), you don’t need to rebuild the images every time you deploy. Instead you can pull the pre-built image from the container registry and deploy it directly.

**By using image instead of build:**
- **Speeds up Deployment:** Instead of building the image from scratch every time, you’re pulling a pre-built image from a registry. This speeds up the deployment process.
- **Reduces Errors:** Using a pre-built image ensures consistency between different environments (e.g., development, staging, production) because the same image is being used.
- **Good for CI/CD**: In a CI/CD pipeline, you can build the image once during the CI phase, push it to a registry, and then simply pull the image for deployment. This is more efficient than building the image in every environment.
**Summary of Key Features:**
- **Containers for Each Service:** Separate containers for frontend, backend, and MongoDB to isolate the responsibilities of each service.
- **Network Configuration:** All services are part of the same Docker network, which allows them to communicate securely and privately.
- **Port Mapping:** Each service has ports exposed on the host machine (EC2 instance) to allow external access to the frontend, backend, and database.
- **Data Persistence:** The volume for MongoDB ensures that database data is not lost between container restarts or recreations.
This setup is ideal for small to medium-sized applications and helps implement modern DevOps practices with containerization and automation.

# deploy.sh

This bash script is automating the process of stopping, pulling, and restarting your Docker containers using Docker Compose and the latest images from GitHub Container Registry (GHCR).

Here’s a step-by-step breakdown:

**1. Stop and Remove Old Containers:**
```
docker compose down || true
``` 
- **docker compose down**: This command stops and removes all the running containers defined in the docker-compose.yml file. It also removes any associated networks.
- ```|| true:``` This ensures that even if docker compose down encounters an error (e.g., if there are no containers running), the script will continue executing without stopping.

**2. Pull the Latest Images from GHCR:**
```
docker pull ghcr.io/mariammbello/resume-frontend:latest
docker pull ghcr.io/mariammbello/resume-backend:latest
``` 
- **docker pull:** This command pulls the latest versions of the Docker images for both the frontend and backend from the GitHub Container Registry (GHCR).
```ghcr.io/mariammbello/resume-frontend```: Refers to the latest version of the frontend image stored in GHCR.
```ghcr.io/mariammbello/resume-backend```: Refers to the latest version of the backend image stored in GHCR.
**3. Start the Containers Using Docker Compose:**
```
docker compose up -d --pull always
```
- **docker compose up -d:** This command starts or restarts all the services defined in the docker-compose.yml file in detached mode (-d), meaning the containers will run in the background.
- **--pull:** This flag ensures that Docker Compose pulls the latest images from the registry before starting the containers. If newer versions of the images exist, they will be used.

**4. Completion Message:**
```
echo "Update complete!"
``` 
This outputs a simple message to indicate that the script has completed its tasks successfully.

Summary:
The script ensures that old containers are stopped and removed.
It pulls the latest images for the frontend and backend from the registry (GHCR).
After pulling the latest images, it uses Docker Compose to spin up the containers in the background using the latest versions of the images.
Finally, it prints "Update complete!" to indicate that the deployment process is finished.
This is a streamlined deployment script for a CI/CD pipeline, ensuring that the most recent version of your app (frontend and backend) is deployed to your environment.


# Dockerfiles breakdown
Docker allows us to package our application, along with all its dependencies and environment configurations, into lightweight, standalone containers. This ensures that the application runs consistently across any environment, whether it's on your local machine, a development server, or in the cloud.
For this project, I created separate Dockerfiles for both the frontend and backend components.

**Frontend Dockerfile:** The frontend serves static HTML files through an Nginx web server, which is responsible for handling incoming HTTP requests and returning web pages.

Here’s the breakdown of the frontend Dockerfile:

Dockerfile
```
FROM nginx:alpine
COPY frontend/ /usr/share/nginx/html
EXPOSE 80
```
**1. FROM nginx:alpine:** This line specifies the base image to use for the container. In this case, we are using an official, lightweight version of Nginx based on the Alpine Linux distribution.
Nginx is a widely-used web server that's ideal for serving static content (HTML, CSS, JavaScript) and handling HTTP requests.
Alpine Linux is known for being extremely lightweight and fast, which reduces the size of the final image, making it more efficient for deployment.

**2. COPY frontend/ /usr/share/nginx/html:** This command copies the contents of the frontend/ directory from the project folder on the host machine into the /usr/share/nginx/html directory inside the container.
```/usr/share/nginx/html``` is the default directory where Nginx looks for files to serve as the root of the website. By copying your static HTML files into this directory, Nginx will serve these files when the container starts.
**3. EXPOSE 80:** This tells Docker that the container will listen for incoming requests on port 80, which is the default HTTP port.
Expose doesn't actually open ports, but it makes it easier to map the container's port to the host machine's port when running the container (e.g., docker run -p 80:80 maps port 80 on the container to port 80 on the host machine).
What happens:
Once this Dockerfile is built and the container is run, Nginx will serve the static files from the frontend/ directory on port 80. This effectively makes your resume webpage accessible through a web browser.

**Backend Dockerfile:**
Purpose:
The backend is built using Flask, a lightweight Python web framework. It connects to a MongoDB database and provides an API to increment and return the page view count whenever the frontend requests it.

Here’s the breakdown of the backend Dockerfile:

Dockerfile
```
FROM python:3.9-slim
WORKDIR /app
COPY backend/ /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "main.py"]
```

**1. FROM python:3.9-slim:** This line specifies that the base image for this container is Python 3.9, but a lightweight "slim" version. Slim images contain only the essential libraries and tools, which makes the image smaller and quicker to download.
Python 3.9: This is the runtime environment required to run your Flask application, as Flask is a Python framework.
Slim version: This reduces unnecessary overhead and minimizes the size of the Docker image.
**2. WORKDIR /app:** This sets the working directory inside the container to /app. All subsequent commands (like copying files and running commands) will be executed within this directory.
Think of WORKDIR as setting the current working directory inside the container, just like running the cd command on your local system.
**3. COPY backend/ /app:** This command copies the contents of the backend/ directory from your host machine (where your project code resides) into the /app directory inside the container.
This means that all your Flask application files (like main.py, requirements.txt, etc.) will be available in the /app folder within the container.
**4. RUN pip install --no-cache-dir -r requirements.txt:** This command installs the Python dependencies listed in the requirements.txt file.
pip install: Installs the required Python packages.
```--no-cache-dir:``` This option prevents pip from caching the downloaded packages, which helps keep the image size small.
requirements.txt: This file typically contains a list of dependencies that the Flask app needs (like Flask, pymongo, etc.). When Docker runs this command, it ensures all the necessary libraries are installed inside the container.
**5. EXPOSE 5000:** This tells Docker that the container will listen for incoming HTTP requests on port 5000, which is the default port that Flask uses for development servers.
When the container runs, Flask will be accessible on port 5000 inside the container, and you can map it to any port on the host machine (e.g., docker run -p 5000:5000).
**6. CMD ["python", "main.py"]:** This specifies the command to run when the container starts. Here, it’s telling Docker to run the Python interpreter and execute the main.py file.
**CMD:** This defines the default command that should be executed when a container starts. In this case, it starts the Flask application by running main.py.
**main.py:** This file is your Flask app's entry point. It contains the code that starts the Flask web server, which handles incoming API requests and interacts with the MongoDB database.
What happens:
When this Dockerfile is built and the container is run, the Flask web server will start, listening for HTTP requests on port 5000. The Flask app will be ready to process requests from the frontend (for example, incrementing the page views or sending the current count).

### Why Dockerize?
- Consistency Across Environments: Docker ensures that the application runs exactly the same way across development, testing, and production environments. By containerizing the app, you eliminate the "it works on my machine" problem.
- Easy Deployment: Once the application is containerized, it can be easily deployed to any environment that supports Docker (e.g., cloud servers like AWS EC2).
- Dependency Management: Since all dependencies are packaged inside the Docker image, there’s no need to install dependencies separately on the host machine. Docker containers are self-contained environments.

These steps ensure that both the frontend and backend are isolated and packaged into containers, making them easier to deploy and manage. Each component of the application has its own environment, and by using Docker, we ensure consistency across all stages of development and deployment.






