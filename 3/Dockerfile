# Dockerfile for Tor Hidden Service
# This file contains instructions to build the Docker image

## Step 1: Choose Base Image ##
# We're using Debian 12 (Bookworm) - stable and well-supported
FROM debian:bookworm-slim

## Step 2: Set Metadata ##
LABEL maintainer="your-email@example.com"
LABEL description="Tor Hidden Service with Nginx and SSH"
LABEL version="1.0"

## Step 3: Install Required Software ##
# Update package list and install everything we need
RUN apt-get update && apt-get install -y \
    # Web server
    nginx \
    # Tor for hidden service
    tor \
    # SSH server for remote access
    openssh-server \
    # Useful utilities
    curl \
    nano \
    procps \
    # Clean up to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

## Step 4: Create Application Directory ##
# This is where we'll put our files
WORKDIR /app

## Step 5: Copy Configuration Files ##
# Copy all our config files into the container

# Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Tor configuration
COPY torrc /etc/tor/torrc

# SSH configuration
COPY sshd_config /etc/ssh/sshd_config

# Website files
COPY index.html /app/index.html

# Startup script
COPY start.sh /app/start.sh

## Step 6: Set Permissions ##
# Make the startup script executable
RUN chmod +x /app/start.sh

## Step 7: Create Necessary Directories ##
# Create directories that services will need
RUN mkdir -p /var/www/html \
    && mkdir -p /var/lib/tor/hidden_service \
    && mkdir -p /var/log/tor \
    && mkdir -p /var/log/nginx \
    && mkdir -p /run/sshd

## Step 8: Set Root Password (CHANGE THIS!) ##
# Set a password for SSH access
# In production, you should use SSH keys instead!
RUN echo 'root:torproject123' | chpasswd

## Step 9: Expose Ports ##
# Tell Docker which ports this container will use

# Port 80 - HTTP (Nginx web server)
EXPOSE 80

# Port 4242 - SSH (for remote access)
EXPOSE 4242

# Note: Tor doesn't need an exposed port (it works internally)

## Step 10: Health Check ##
# Docker will run this to check if container is healthy
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

## Step 11: Set the Startup Command ##
# This command runs when the container starts
CMD ["/app/start.sh"]


###############################################
## DOCKER BUILD & RUN INSTRUCTIONS ##
###############################################

# To build this image:
#   docker build -t tor-hidden-service .

# To run the container:
#   docker run -d \
#     -p 8080:80 \
#     -p 4242:4242 \
#     --name my-tor-service \
#     tor-hidden-service

# To view logs:
#   docker logs -f my-tor-service

# To get your .onion address:
#   docker exec my-tor-service cat /var/lib/tor/hidden_service/hostname

# To access container via SSH:
#   ssh root@localhost -p 4242
#   (password: torproject123)

# To stop the container:
#   docker stop my-tor-service

# To remove the container:
#   docker rm my-tor-service
