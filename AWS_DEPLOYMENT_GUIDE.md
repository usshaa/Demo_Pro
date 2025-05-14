# AWS EC2 Deployment Guide

This guide provides detailed instructions for deploying the IT Course Recommender application to AWS EC2 using Docker, Docker Compose, Nginx, and Gunicorn.

## Prerequisites

1. An AWS account
2. Basic knowledge of AWS EC2, SSH, and the command line

## Step 1: Launch an EC2 Instance

1. Log in to the AWS Management Console
2. Navigate to EC2 and click "Launch Instance"
3. Choose an Amazon Machine Image (AMI)
   - Recommended: Ubuntu Server 20.04 LTS or newer
4. Choose an Instance Type
   - For testing: t2.micro (free tier eligible)
   - For production: t2.small or larger
5. Configure Instance Details
   - Use default settings or customize as needed
6. Add Storage
   - Recommended: At least 20GB for production
7. Add Tags (optional)
   - Key: Name, Value: course-recommender-app
8. Configure Security Group
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80) from anywhere
   - Allow HTTPS (port 443) from anywhere
9. Review and Launch
10. Create or select an existing key pair
    - Download the key pair (.pem file) and keep it secure

## Step 2: Connect to Your EC2 Instance

1. Open a terminal on your local machine
2. Change permissions for your key file:
   ```
   chmod 400 /path/to/your-key.pem
   ```
3. Connect to your instance:
   ```
   ssh -i /path/to/your-key.pem ubuntu@your-ec2-public-ip
   ```

## Step 3: Set Up the EC2 Instance

1. Clone your repository or upload your application files:
   ```
   git clone https://your-repository-url.git
   # OR upload files using SCP
   ```

2. If you uploaded files via SCP, navigate to your project directory:
   ```
   cd your-project-directory
   ```

3. Make the setup script executable and run it:
   ```
   chmod +x ec2_setup.sh
   ./ec2_setup.sh
   ```

4. Log out and log back in to apply the Docker group changes:
   ```
   exit
   # Then reconnect using SSH
   ssh -i /path/to/your-key.pem ubuntu@your-ec2-public-ip
   ```

## Step 4: Configure Your Application

1. Create necessary directories if they don't exist:
   ```
   mkdir -p data static nginx/ssl
   ```

2. Update the Nginx configuration with your domain name or EC2 public IP:
   ```
   nano nginx/conf.d/app.conf
   ```
   Replace `server_name _;` with `server_name your-domain.com;` or your EC2 public IP

3. If you have a domain name and want to set up SSL:
   ```
   chmod +x setup_ssl.sh
   ./setup_ssl.sh your-domain.com
   ```

## Step 5: Start the Application

1. Build and start the containers:
   ```
   docker-compose up -d --build
   ```

2. Check if the containers are running:
   ```
   docker-compose ps
   ```

3. View the logs:
   ```
   docker-compose logs
   ```

## Step 6: Test Your Deployment

1. Open a web browser and navigate to your EC2 public IP or domain name
2. Verify that your application is working correctly

## Troubleshooting

### Container Not Starting

Check the logs:
```
docker-compose logs web
```

### Nginx Configuration Issues

Test the Nginx configuration:
```
docker exec -it $(docker ps -q -f name=nginx) nginx -t
```

### Permission Issues

Check file permissions:
```
ls -la
sudo chown -R $USER:$USER .
```

## Maintenance

### Updating Your Application

1. Pull the latest changes:
   ```
   git pull
   ```

2. Rebuild and restart the containers:
   ```
   docker-compose down
   docker-compose up -d --build
   ```

### Backing Up Data

1. Create a backup of your data:
   ```
   tar -czvf backup.tar.gz data/
   ```

2. Copy the backup to your local machine:
   ```
   scp -i /path/to/your-key.pem ubuntu@your-ec2-public-ip:~/backup.tar.gz .
   ```

### Monitoring

1. Check container resource usage:
   ```
   docker stats
   ```

2. Monitor system resources:
   ```
   sudo apt-get install -y htop
   htop
   ```

## Security Best Practices

1. Keep your system updated:
   ```
   sudo apt-get update && sudo apt-get upgrade -y
   ```

2. Use a firewall:
   ```
   sudo apt-get install -y ufw
   sudo ufw allow ssh
   sudo ufw allow http
   sudo ufw allow https
   sudo ufw enable
   ```

3. Set up automatic security updates:
   ```
   sudo apt-get install -y unattended-upgrades
   sudo dpkg-reconfigure -plow unattended-upgrades
   ```

4. Consider using AWS CloudWatch for monitoring

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Gunicorn Documentation](https://docs.gunicorn.org/en/stable/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
