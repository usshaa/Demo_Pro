#!/bin/bash

# This script helps set up SSL certificates using Let's Encrypt
# Make sure to run this script after setting up your domain to point to your EC2 instance

# Check if domain name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 yourdomain.com"
    exit 1
fi

DOMAIN=$1

# Install Certbot
sudo apt-get update
sudo apt-get install -y certbot

# Stop Nginx if it's running
docker-compose down

# Get SSL certificate
sudo certbot certonly --standalone -d $DOMAIN --agree-tos --email your-email@example.com --non-interactive

# Create SSL directory if it doesn't exist
mkdir -p nginx/ssl

# Copy certificates to Nginx SSL directory
sudo cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem nginx/ssl/

# Set proper permissions
sudo chown -R $USER:$USER nginx/ssl/
chmod -R 755 nginx/ssl/

# Update Nginx configuration for SSL
cat > nginx/conf.d/app.conf << EOF
server {
    listen 80;
    server_name $DOMAIN;
    
    # Redirect all HTTP requests to HTTPS
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name $DOMAIN;
    
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384;
    ssl_session_timeout 10m;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    location / {
        proxy_pass http://web:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Optional: Configure for static files if needed
    location /static/ {
        alias /app/static/;
        expires 30d;
    }
}
EOF

# Start the services again
docker-compose up -d

# Set up auto-renewal
echo "0 3 * * * certbot renew --quiet && docker-compose restart nginx" | sudo tee -a /etc/crontab

echo "SSL setup complete for $DOMAIN!"
echo "Your application should now be accessible via https://$DOMAIN"
