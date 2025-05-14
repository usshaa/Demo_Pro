# IT Course Recommender System

A Flask-based web application that recommends IT courses based on user preferences and collaborative filtering.

## Local Development

### Setup and Installation

1. Create a virtual environment and activate it:
   ```
   python -m venv newenv
   newenv\Scripts\activate  # On Windows
   source newenv/bin/activate  # On Linux/Mac
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Generate synthetic data (if needed):
   ```
   python synthetic_data.py
   ```

4. Train the recommendation model:
   ```
   python Recommendation_Model.py
   ```

5. Run the application locally:
   ```
   python app.py
   ```

## Docker Deployment (Local)

1. Build the Docker image:
   ```
   docker build -t flask-app .
   ```

2. Run the container:
   ```
   docker run -p 5000:5000 flask-app
   ```

## AWS EC2 Deployment with Nginx and Docker Compose

### Prerequisites

- An AWS account
- An EC2 instance running Ubuntu (recommended: t2.micro for testing, t2.small or larger for production)
- Basic knowledge of AWS EC2 and SSH

### Deployment Steps

1. **Launch an EC2 instance**
   - Use Ubuntu Server (20.04 or later)
   - Configure security group to allow HTTP (80), HTTPS (443), and SSH (22) traffic
   - Create or use an existing key pair for SSH access

2. **Connect to your EC2 instance**
   ```
   ssh -i /path/to/your-key.pem ubuntu@your-ec2-public-ip
   ```

3. **Clone your repository or upload your application files**
   ```
   git clone https://your-repository-url.git
   # OR upload files using SCP or SFTP
   ```

4. **Run the setup script**
   ```
   chmod +x ec2_setup.sh
   ./ec2_setup.sh
   ```

5. **Start the application with Docker Compose**
   ```
   docker-compose up -d
   ```

6. **Access your application**
   Open your browser and navigate to your EC2 instance's public IP address or domain name.

### SSL Configuration (Optional)

To enable HTTPS:

1. Obtain SSL certificates (Let's Encrypt or your preferred provider)
2. Place the certificate files in the `nginx/ssl` directory
3. Update the Nginx configuration in `nginx/conf.d/app.conf` to include SSL settings
4. Restart the containers:
   ```
   docker-compose down
   docker-compose up -d
   ```

## Maintenance

- **View logs**:
  ```
  docker-compose logs
  ```

- **Update the application**:
  ```
  git pull  # If using git
  docker-compose down
  docker-compose up -d --build
  ```

- **Backup data**:
  ```
  # Backup your data files
  tar -czvf backup.tar.gz users.csv courses.csv ratings.csv course_recommender_model.pkl
  ```