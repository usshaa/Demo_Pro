#!/bin/bash

# Update the system
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common git

# Install Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add the current user to the docker group to run docker without sudo
sudo usermod -aG docker $USER

# Create directory for SSL certificates (if you plan to use HTTPS)
mkdir -p nginx/ssl

echo "Setup complete! You may need to log out and log back in for the docker group changes to take effect."
echo "Next steps:"
echo "1. Clone your repository or upload your application files"
echo "2. Run 'docker-compose up -d' to start your application"
