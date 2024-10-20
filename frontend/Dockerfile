# Use a base image for serving static HTML files (nginx is common)
FROM nginx:alpine

# Copy your frontend files to the nginx web directory
COPY . /usr/share/nginx/html

# Expose port 80 to serve the frontend
EXPOSE 80
