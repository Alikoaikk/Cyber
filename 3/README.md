# Docker - Complete Beginner's Guide

## What is Docker? (The Simple Explanation)

Imagine you're moving to a new house. You could:
1. Pack each item separately (nightmare!)
2. Put everything in a shipping container (easy to move!)

**Docker is like a shipping container for software.**

---

## The Problem Docker Solves

### Before Docker:
```
Your Computer:
- Works perfectly ✓

Friend's Computer:
- "It doesn't work!" ✗
- Different OS version
- Missing dependencies
- Wrong Python version
- Different library versions
```

### With Docker:
```
Your Computer:
- Package app + dependencies in container ✓

Friend's Computer:
- Run the SAME container ✓
- Works identically!
```

**Docker guarantees**: "If it works on your machine, it works everywhere."

---

## Core Concepts (Building Blocks)

### 1. Image (The Blueprint)
**What it is**: A template/snapshot containing:
- Operating system
- Your application code
- All dependencies
- Configuration files

**Think of it as**:
- A recipe for a cake
- A blueprint for a house
- A class in programming (if you know OOP)

**Example**:
```
ubuntu:22.04 = Ubuntu Linux image
nginx:latest = Nginx web server image
node:18 = Node.js runtime image
```

---

### 2. Container (The Running Instance)
**What it is**: A running image

**Think of it as**:
- The actual cake baked from the recipe
- The house built from the blueprint
- An object created from a class

**Key difference**:
- 1 Image → Can create MANY containers
- Each container is isolated from others

**Example**:
```
Image: nginx
Container 1: Your blog (running on port 8080)
Container 2: Your store (running on port 8081)
Container 3: Your portfolio (running on port 8082)
```

---

### 3. Dockerfile (The Recipe)
**What it is**: A text file with instructions to build an image

**Think of it as**: Step-by-step cooking instructions

**Example**:
```dockerfile
FROM ubuntu:22.04          # Start with Ubuntu
RUN apt-get update         # Update packages
RUN apt-get install nginx  # Install Nginx
COPY index.html /var/www/  # Copy your HTML
CMD ["nginx"]              # Run Nginx
```

---

### 4. Docker Hub (The App Store)
**What it is**: Online repository of pre-made images

**Think of it as**: GitHub for Docker images

**Popular images**:
- ubuntu, debian, alpine (Linux distributions)
- nginx, apache (web servers)
- mysql, postgres (databases)
- node, python, java (programming languages)

---

## Visual: Image vs Container

```
┌─────────────────────────────────────────┐
│  DOCKER IMAGE (Blueprint)               │
│  - Read-only                            │
│  - Stored on disk                       │
│  - Can't be modified (create new one)   │
│  - Like a .exe installer                │
└─────────────────────────────────────────┘
                  │
                  │ docker run
                  ↓
┌─────────────────────────────────────────┐
│  CONTAINER 1 (Running Instance)         │
│  - Read/write                           │
│  - Running in memory                    │
│  - Can be modified                      │
│  - Like a running program               │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  CONTAINER 2 (Another Instance)         │
│  - Completely separate from Container 1 │
│  - Different data, different state      │
└─────────────────────────────────────────┘
```

---

## Docker Architecture

```
┌──────────────────────────────────────────────────────┐
│  YOUR COMPUTER                                        │
│                                                       │
│  ┌────────────────────────────────────────────┐     │
│  │  Docker Client (What you use)              │     │
│  │  Commands: docker run, docker build, etc.  │     │
│  └────────────────────────────────────────────┘     │
│                      │                               │
│                      │ talks to                      │
│                      ↓                               │
│  ┌────────────────────────────────────────────┐     │
│  │  Docker Daemon (The Engine)                │     │
│  │  - Builds images                           │     │
│  │  - Runs containers                         │     │
│  │  - Manages everything                      │     │
│  └────────────────────────────────────────────┘     │
│                      │                               │
│                      │ manages                       │
│                      ↓                               │
│  ┌─────────────────────────────────────────────┐    │
│  │  Containers (Running)                       │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐ │    │
│  │  │Container1│  │Container2│  │Container3│ │    │
│  │  │  Nginx   │  │  MySQL   │  │  Node.js │ │    │
│  │  └──────────┘  └──────────┘  └──────────┘ │    │
│  └─────────────────────────────────────────────┘    │
│                                                       │
└──────────────────────────────────────────────────────┘
```

---

## Key Docker Commands (The Essential Toolkit)

### Working with Images

```bash
# 1. Download an image from Docker Hub
docker pull ubuntu:22.04

# 2. List all images on your computer
docker images

# 3. Build an image from Dockerfile
docker build -t my-app:1.0 .

# 4. Remove an image
docker rmi ubuntu:22.04

# 5. Search for images on Docker Hub
docker search nginx
```

### Working with Containers

```bash
# 1. Create and start a container
docker run ubuntu:22.04

# 2. Create and start (interactive mode with terminal)
docker run -it ubuntu:22.04 /bin/bash

# 3. Create and start (detached/background mode)
docker run -d nginx

# 4. List running containers
docker ps

# 5. List all containers (including stopped)
docker ps -a

# 6. Stop a running container
docker stop container_name

# 7. Start a stopped container
docker start container_name

# 8. Remove a container
docker rm container_name

# 9. View container logs
docker logs container_name

# 10. Execute command in running container
docker exec -it container_name /bin/bash
```

---

## Important Flags Explained

### `docker run` Flags

```bash
-d              # Detached (run in background)
-it             # Interactive + Terminal
-p 8080:80      # Port mapping (host:container)
--name my-app   # Give container a name
-v /host:/cont  # Volume (share folder)
--rm            # Auto-remove when stopped
-e VAR=value    # Environment variable
```

**Examples**:

```bash
# Run Nginx, expose port 80 as 8080, name it "webserver"
docker run -d -p 8080:80 --name webserver nginx

# Run Ubuntu interactively, remove when exit
docker run -it --rm ubuntu:22.04 /bin/bash

# Run with volume (share folder between host and container)
docker run -v /my/html:/usr/share/nginx/html nginx
```

---

## Understanding Ports (-p flag)

```
Your Computer                Docker Container
─────────────                ────────────────

Port 8080        ←─────→     Port 80
(you visit)                  (Nginx listens)

localhost:8080               nginx:80
```

**Example**:
```bash
docker run -p 8080:80 nginx
```

**What happens**:
1. Nginx inside container listens on port 80
2. Docker maps your computer's port 8080 to container's port 80
3. You visit `localhost:8080` in browser
4. Request goes to container's port 80
5. Nginx serves the page

---

## Understanding Volumes (-v flag)

**Problem**: Container data disappears when container is removed!

**Solution**: Volumes (persistent storage)

```
Your Computer                Docker Container
─────────────                ────────────────

/home/user/html  ←─────→     /usr/share/nginx/html
(permanent)                  (inside container)
```

**Example**:
```bash
docker run -v /home/user/html:/usr/share/nginx/html nginx
```

**What happens**:
1. Your HTML files stay on your computer
2. Container can read/write them
3. Changes persist even if container is deleted
4. You can edit files normally, container sees changes

---

## Container Lifecycle

```
┌──────────┐
│  Image   │
└──────────┘
     │
     │ docker run
     ↓
┌──────────┐     docker stop      ┌──────────┐
│ Running  │ ───────────────────→ │ Stopped  │
└──────────┘                      └──────────┘
     ↑                                  │
     │                                  │
     │ docker start                     │ docker rm
     │                                  ↓
     └──────────────────────────  ┌──────────┐
                                  │ Removed  │
                                  └──────────┘
```

---

## Isolation: How Containers Stay Separate

**Each container has its own**:
- File system
- Network
- Processes
- Memory
- CPU resources

```
┌─────────────────────────────────────────┐
│  Your Computer (Host OS)                │
│                                         │
│  ┌──────────┐  ┌──────────┐           │
│  │Container1│  │Container2│           │
│  │          │  │          │           │
│  │ Ubuntu   │  │ Debian   │           │
│  │ Nginx    │  │ Apache   │           │
│  │ Port 80  │  │ Port 80  │  ← Same port, no conflict!
│  │ /var/www │  │ /var/www │  ← Same path, different files!
│  └──────────┘  └──────────┘           │
│                                         │
└─────────────────────────────────────────┘
```

**Why this matters**:
- No conflicts between containers
- Can run multiple versions of same software
- Easy to delete without affecting others

---

## Dockerfile: Building Your Own Image

### Basic Dockerfile Structure

```dockerfile
# 1. Start from a base image
FROM ubuntu:22.04

# 2. Set working directory
WORKDIR /app

# 3. Copy files from your computer to container
COPY index.html /app/

# 4. Run commands (install software, etc.)
RUN apt-get update && apt-get install -y nginx

# 5. Expose port (documentation, doesn't actually open it)
EXPOSE 80

# 6. Command to run when container starts
CMD ["nginx", "-g", "daemon off;"]
```

### Dockerfile Instructions Explained

| Instruction | Purpose | Example |
|------------|---------|---------|
| `FROM` | Base image to start from | `FROM ubuntu:22.04` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `COPY` | Copy files from host to container | `COPY . /app` |
| `ADD` | Like COPY but can extract archives | `ADD file.tar.gz /app` |
| `RUN` | Execute command during build | `RUN apt-get install nginx` |
| `CMD` | Default command when container starts | `CMD ["nginx"]` |
| `ENTRYPOINT` | Command that always runs | `ENTRYPOINT ["/start.sh"]` |
| `EXPOSE` | Document which ports are used | `EXPOSE 80 443` |
| `ENV` | Set environment variable | `ENV DEBUG=true` |
| `USER` | Set user for commands | `USER nginx` |

---

## Docker Build Process

```bash
# Build an image from Dockerfile
docker build -t my-image:1.0 .
```

**What the command means**:
- `docker build` = build an image
- `-t my-image:1.0` = tag/name it "my-image" version "1.0"
- `.` = look for Dockerfile in current directory

**What happens**:
1. Docker reads Dockerfile
2. Executes each instruction in order
3. Each instruction creates a layer
4. Layers are cached (faster rebuilds!)
5. Final image is created

---

## Layers: How Docker Images Work

```
┌────────────────────────────────────┐
│  Layer 4: CMD ["nginx"]            │  ← Your command
├────────────────────────────────────┤
│  Layer 3: COPY index.html          │  ← Your files
├────────────────────────────────────┤
│  Layer 2: RUN apt-get install      │  ← Installed software
├────────────────────────────────────┤
│  Layer 1: FROM ubuntu:22.04        │  ← Base OS
└────────────────────────────────────┘
```

**Why layers matter**:
- Each layer is cached
- If you change Layer 4, only Layer 4 rebuilds
- Faster builds!
- Shared layers between images save space

**Best practice**: Put things that change least at the top

---

## Common Use Cases

### 1. Web Server (Nginx)
```bash
# Quick Nginx server with your HTML
docker run -d -p 8080:80 -v $(pwd):/usr/share/nginx/html nginx
```

### 2. Database (MySQL)
```bash
# MySQL database with password
docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=secret mysql
```

### 3. Development Environment
```bash
# Node.js development
docker run -it -v $(pwd):/app -w /app node:18 /bin/bash
```

### 4. Testing
```bash
# Test your app in clean environment
docker run --rm -v $(pwd):/app python:3.9 python /app/test.py
```

---

## Docker vs Virtual Machines

```
VIRTUAL MACHINE                    DOCKER CONTAINER
───────────────                    ────────────────

┌─────────────────┐               ┌─────────────────┐
│   Application   │               │   Application   │
├─────────────────┤               ├─────────────────┤
│   Guest OS      │               │   (no full OS)  │
│   (Full Linux)  │               │   (shared)      │
├─────────────────┤               ├─────────────────┤
│   Hypervisor    │               │  Docker Engine  │
├─────────────────┤               ├─────────────────┤
│    Host OS      │               │    Host OS      │
└─────────────────┘               └─────────────────┘

Size: GBs                         Size: MBs
Boot: Minutes                     Boot: Seconds
Resource: Heavy                   Resource: Light
Isolation: Complete               Isolation: Process-level
```

---

## Practical Example: Your First Container

Let's run a simple web server:

### Step 1: Create HTML file
```bash
echo "<h1>Hello from Docker!</h1>" > index.html
```

### Step 2: Run Nginx with your HTML
```bash
docker run -d -p 8080:80 -v $(pwd):/usr/share/nginx/html --name my-web nginx
```

### Step 3: Visit in browser
```
http://localhost:8080
```

### Step 4: Check it's running
```bash
docker ps
```

### Step 5: View logs
```bash
docker logs my-web
```

### Step 6: Stop and remove
```bash
docker stop my-web
docker rm my-web
```

---

## Troubleshooting Common Issues

### Container exits immediately
```bash
# See what happened
docker logs container_name

# Run in foreground to see errors
docker run -it image_name
```

### Port already in use
```bash
# Use different port
docker run -p 8081:80 nginx  # Instead of 8080:80
```

### Can't find Dockerfile
```bash
# Make sure you're in right directory
ls Dockerfile

# Or specify path
docker build -f /path/to/Dockerfile .
```

### Permission denied
```bash
# On Linux, add user to docker group
sudo usermod -aG docker $USER
# Then logout and login
```

---

## Best Practices

### 1. Use Specific Tags
```dockerfile
# Bad
FROM ubuntu

# Good
FROM ubuntu:22.04
```

### 2. Minimize Layers
```dockerfile
# Bad
RUN apt-get update
RUN apt-get install -y nginx
RUN apt-get install -y curl

# Good
RUN apt-get update && apt-get install -y \
    nginx \
    curl
```

### 3. Use .dockerignore
```
# .dockerignore file
node_modules
.git
*.log
```

### 4. Don't Run as Root
```dockerfile
# Create non-root user
RUN useradd -m appuser
USER appuser
```

### 5. Clean Up in Same Layer
```dockerfile
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*
```

---

## Next Steps

Now that you understand Docker basics, you're ready to:

1. **Practice**: Run different containers (nginx, mysql, ubuntu)
2. **Build**: Create your own Dockerfile
3. **Apply**: Build your Tor hidden service project!

---

## Quick Reference Card

```bash
# IMAGES
docker pull <image>              # Download image
docker images                    # List images
docker build -t <name> .         # Build image
docker rmi <image>               # Remove image

# CONTAINERS
docker run <image>               # Create & start container
docker ps                        # List running containers
docker ps -a                     # List all containers
docker stop <container>          # Stop container
docker start <container>         # Start stopped container
docker rm <container>            # Remove container
docker logs <container>          # View logs
docker exec -it <container> bash # Enter container

# CLEANUP
docker system prune              # Remove unused data
docker container prune           # Remove stopped containers
docker image prune               # Remove unused images
```

---

## Key Takeaways

1. **Image** = Blueprint (static template)
2. **Container** = Running instance of image
3. **Dockerfile** = Instructions to build image
4. **Isolation** = Each container is separate
5. **Portability** = Works same everywhere
6. **Lightweight** = Faster and smaller than VMs

You're now ready to start using Docker! Practice with the commands, and we can build your Tor hidden service next.
