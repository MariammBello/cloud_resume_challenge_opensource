# Limitations and Best Practices: Navigating Open Source vs. Enterprise tools 
While the project successfully demonstrates the use of Free and Open Source Software (FOSS) and minimal-cost cloud services to deploy a cloud-based resume website, there are important limitations to consider and areas where improvements can be made. These considerations revolve around security, scalability, performance, and management.

**1. Lack of SSL/TLS (HTTPS)**
**Issue:** The current setup serves the site over HTTP, which exposes it to potential security threats, such as data interception and man-in-the-middle attacks.

**Best Practice Solution:** Implementing SSL/TLS certificates for HTTPS is critical for securing web traffic. Using Let's Encrypt, a free, automated, and open certificate authority, would allow you to easily obtain and renew SSL certificates, ensuring that your website is secure with HTTPS.

**2. Scalability Concerns**
**Issue:** The project uses a small, free-tier EC2 instance, which is sufficient for low-traffic personal projects but inadequate for handling high-traffic or production-level applications. This setup may also become a bottleneck as the number of visitors or service demands increases.

**Best Practice Solution:** As traffic grows or requirements change, it's important to plan for scaling. You could upgrade the EC2 instance to a more powerful type, or even better, implement an auto-scaling group that can dynamically add or remove instances based on traffic demand. Pairing this with AWS Elastic Load Balancer (ELB) can distribute traffic more efficiently, improving both scalability and fault tolerance.

**3. Database Management & Persistence**
**Issue:** Currently, MongoDB is running in a Docker container on the EC2 instance. This setup works for development but may have limitations regarding data persistence and availability. If the instance goes down, data stored in the container could be lost unless specific volume persistence strategies are implemented.

**Best Practice Solution:** For better availability and data security, moving to a managed database service like MongoDB Atlas is recommended. Managed services provide automated backups, replication, and enhanced security out of the box, eliminating concerns about losing data or managing database infrastructure manually. Another option would be to configure persistent volumes and backups within the current Docker setup.

**4. Monitoring and Logging**
**Issue:** Currently, there is no system in place for structured monitoring and logging of the app, containers, or underlying infrastructure. This means you might not detect potential performance issues, downtime, or errors in a timely manner.

**Best Practice Solution:** Implementing monitoring and observability tools is essential for maintaining the health and performance of the application. Using Prometheus for metrics collection and Grafana for visualizing those metrics can help track container performance, request times, resource utilization, and more. For logging, ELK Stack (Elasticsearch, Logstash, and Kibana) or AWS CloudWatch Logs can help centralize and analyze logs to troubleshoot issues effectively.

**5. Performance Optimization**
**Issue:** While the current setup works for a small-scale project, it’s not optimized for high performance. Page load times and overall responsiveness could be improved with optimizations to both frontend delivery and backend query performance.

**Best Practice Solution:**
- Frontend Optimization: Utilize a CDN (Content Delivery Network) to cache and deliver static assets (CSS, JavaScript, images) closer to users, reducing load times.
- Backend Optimization: Implement caching mechanisms, such as Redis, to minimize database queries and reduce API response times.
- Database Performance: Indexing the MongoDB collections can improve query performance, especially as the data grows.

**6. Security Considerations**
**Issue:** Security for a cloud-based web app goes beyond just using HTTPS. Running services directly on EC2 without additional security measures like firewalls, encryption, or secure access controls can expose your application to various vulnerabilities.

**Best Practice Solution:**
- Security Groups: Tighten EC2 security groups to only allow necessary traffic (e.g., restricting access to ports for SSH, HTTP, HTTPS, and MongoDB as needed).
- IAM Roles: Implement least-privilege AWS IAM roles for access control, ensuring that only the necessary permissions are granted for actions such as deploying containers or accessing data.
- Secrets Management: Use AWS Secrets Manager or environment variables in conjunction with Docker to securely store sensitive information (like database credentials or API keys).

### **Conclusion: FOSS & Open Source vs. Proprietary Solutions**
This project exemplifies how Free and Open Source Software (FOSS) and low-cost cloud services can be used to build a scalable cloud-based resume application. While it's highly functional and offers significant cost savings, it also has its limitations in areas such as scalability, security, and monitoring, especially when compared to fully managed, proprietary solutions offered by major cloud providers.

By following best practices—such as securing your site with SSL, implementing auto-scaling, using managed database services, and adding robust monitoring and logging solutions—you can mitigate these limitations while maintaining the benefits of an open-source, cost-effective tech stack.

Addressing these aspects will not only help your application remain secure and performant but also ensure that it scales efficiently as it grows, all while leveraging the flexibility of open-source tools.