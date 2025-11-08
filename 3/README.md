# Tor Hidden Service Docker Project

A complete Tor Hidden Service running in a Docker container with Nginx, Tor, and SSH.

## 📁 Project Files

```
.
├── Dockerfile          # Docker build instructions
├── nginx.conf          # Web server configuration
├── torrc              # Tor hidden service configuration
├── sshd_config        # SSH server configuration
├── start.sh           # Startup script for all services
├── index.html         # Your website (already exists)
└── README.md          # This file
```

## 🎯 What This Does

1. **Nginx** - Serves your website on port 80
2. **Tor** - Creates a .onion address and routes traffic anonymously
3. **SSH** - Allows you to remotely manage the container on port 4242

## 🚀 Quick Start

### Step 1: Build the Docker Image

```bash
docker build -t tor-hidden-service .
```

**What this does:**
- Reads the Dockerfile
- Downloads Debian Linux
- Installs Nginx, Tor, and SSH
- Copies all configuration files
- Creates an image called "tor-hidden-service"

### Step 2: Run the Container

```bash
docker run -d \
  -p 8080:80 \
  -p 4242:4242 \
  --name my-tor-service \
  tor-hidden-service
```

**What this does:**
- Creates a container from the image
- Maps port 8080 on your computer → port 80 in container
- Maps port 4242 on your computer → port 4242 in container
- Names it "my-tor-service"
- Runs in background (-d)

### Step 3: Get Your .onion Address

```bash
docker exec my-tor-service cat /var/lib/tor/hidden_service/hostname
```

**Example output:**
```
abc123xyz456.onion
```

### Step 4: Test It!

**Local access (no Tor):**
```
http://localhost:8080
```

**Tor access:**
1. Open Tor Browser
2. Visit: `http://your-onion-address.onion`

## 📊 Useful Commands

### View Container Logs
```bash
docker logs -f my-tor-service
```

### Access Container via SSH
```bash
ssh root@localhost -p 4242
```
Password: `torproject123` (⚠️ Change this in Dockerfile!)

### Access Container Shell Directly
```bash
docker exec -it my-tor-service /bin/bash
```

### Check Running Containers
```bash
docker ps
```

### Stop the Container
```bash
docker stop my-tor-service
```

### Start the Container Again
```bash
docker start my-tor-service
```

### Remove the Container
```bash
docker rm my-tor-service
```

### Rebuild After Changes
```bash
docker stop my-tor-service
docker rm my-tor-service
docker build -t tor-hidden-service .
docker run -d -p 8080:80 -p 4242:4242 --name my-tor-service tor-hidden-service
```

## 🔍 Understanding the Build Process

When you run `docker build`, here's what happens:

```
1. FROM debian:bookworm-slim
   ↓ Downloads Debian Linux (base image)

2. RUN apt-get update && apt-get install...
   ↓ Installs Nginx, Tor, SSH, and utilities

3. COPY nginx.conf /etc/nginx/nginx.conf
   ↓ Copies your config files into container

4. COPY start.sh /app/start.sh
   ↓ Copies the startup script

5. RUN chmod +x /app/start.sh
   ↓ Makes startup script executable

6. EXPOSE 80 4242
   ↓ Documents which ports are used

7. CMD ["/app/start.sh"]
   ↓ Sets the command to run when container starts
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│  Docker Container                           │
│                                             │
│  ┌─────────────────────────────────┐       │
│  │  start.sh (runs on startup)     │       │
│  └─────────────────────────────────┘       │
│              │                               │
│              ↓                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  Nginx   │  │   Tor    │  │   SSH    │ │
│  │ Port 80  │  │ .onion   │  │ Port 4242│ │
│  └──────────┘  └──────────┘  └──────────┘ │
│       ↑              ↑              ↑       │
└───────│──────────────│──────────────│───────┘
        │              │              │
    Port 8080     Tor Network    Port 4242
   (your computer)               (your computer)
```

## 🔐 Security Notes

### ⚠️ IMPORTANT - Before Production

1. **Change the SSH password** in Dockerfile:
   ```dockerfile
   RUN echo 'root:YOUR_STRONG_PASSWORD' | chpasswd
   ```

2. **Use SSH keys instead of password**:
   - Generate key: `ssh-keygen -t ed25519`
   - Add to Dockerfile or mount as volume

3. **Disable password auth** in sshd_config:
   ```
   PasswordAuthentication no
   ```

4. **Keep your private key secret**:
   - Located at: `/var/lib/tor/hidden_service/hs_ed25519_secret_key`
   - If someone gets this, they can impersonate your site!

5. **Use volumes for persistence**:
   ```bash
   docker run -v /path/to/tor-data:/var/lib/tor/hidden_service ...
   ```

## 🐛 Troubleshooting

### Container exits immediately
```bash
# View logs to see what happened
docker logs my-tor-service
```

### Can't access on localhost:8080
```bash
# Check if Nginx is running inside container
docker exec my-tor-service curl localhost

# Check if port is mapped correctly
docker port my-tor-service
```

### .onion address not showing
```bash
# Wait a moment, then check again
docker exec my-tor-service cat /var/lib/tor/hidden_service/hostname

# Check Tor logs
docker exec my-tor-service tail /var/log/tor/notices.log
```

### SSH connection refused
```bash
# Check if SSH is running
docker exec my-tor-service ps aux | grep sshd

# Make sure port 4242 is not used by another program
lsof -i :4242
```

## 📚 Next Steps

1. **Customize your website** - Edit index.html
2. **Add more pages** - Create more HTML files
3. **Enable HTTPS** - Set up SSL certificates
4. **Add a database** - Run MySQL in another container
5. **Use Docker Compose** - Manage multiple containers easily

## 🎓 Learning Resources

- [Docker Documentation](https://docs.docker.com/)
- [Tor Hidden Services](https://community.torproject.org/onion-services/)
- [Nginx Documentation](https://nginx.org/en/docs/)

## 📝 Notes

- The .onion address is randomly generated by Tor
- It takes ~30 seconds for Tor to create circuits
- Your site is only accessible via Tor Browser (not regular browsers)
- Local access (localhost:8080) bypasses Tor
