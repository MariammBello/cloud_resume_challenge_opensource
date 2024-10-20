## Main.yml file breakdown
Let's break down each part of the GitHub Actions workflow file (main.yml) step by step. This guide will explain each line and how it contributes to automating the CI/CD pipeline for deploying the frontend and backend of your application to an AWS EC2 instance. The goal is to make this a beginner-friendly explanation, so you can understand what’s happening at each step.

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
branches: This limits the trigger to pushes made on the main branch only.
paths: This defines which directories or files should trigger the workflow when changes are made. It watches changes in the frontend/, backend/, and .github/workflows/main.yml paths.

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