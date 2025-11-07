# Tor Hidden Service Project - Learning Notes

## Project Goal
Build a web server accessible via Tor network (.onion address) using Docker, Nginx, and SSH.

---

## The Big Picture: How Everything Works

### The Flow (User Visiting Your Site)
```
1. User opens Tor Browser
   ↓
2. Types your .onion address
   ↓
3. Request goes through Tor network (encrypted, anonymous)
   ↓
4. Reaches YOUR Docker container
   ↓
5. Tor service (inside container) receives it
   ↓
6. Tor forwards to Nginx on port 80
   ↓
7. Nginx serves your index.html
   ↓
8. Response goes back through Tor network
   ↓
9. User sees your webpage!
```

---

## Components Explained

### 1. Docker Container (The House)
**What it is**: A mini-computer inside your computer

**Why use it**:
- Isolated environment (won't mess up your actual system)
- Portable (runs the same everywhere)
- Contains all services (Nginx, Tor, SSH) in one package

**Think of it as**: A sealed box with everything needed to run your application

---

### 2. Nginx (The Waiter)
**Job**: Serve web pages to visitors

**How it works**:
- Listens on port 80 (HTTP)
- When request comes in, finds the file (index.html)
- Sends the file back to visitor

**Configuration**: nginx.conf tells it:
- Where to find HTML files
- What port to listen on
- What file to serve by default

---

### 3. Tor (The Anonymous Mailman)
**Job**: Hide your location and create a .onion address

**How Tor works**:
1. Creates a special .onion address (like abc123xyz.onion)
2. Visitor's request bounces through 3 random Tor servers
3. Each hop encrypts the data (like layers of an onion)
4. Finally reaches your server
5. Neither you nor visitor know each other's real location

**Hidden Service**:
- Tor listens for requests to your .onion address
- Forwards them to Nginx (localhost:80)
- Sends responses back through Tor network

**Configuration**: torrc tells it:
- Where to store service keys
- What port to forward to Nginx

---

### 4. SSH (The Maintenance Door)
**Job**: Let you access the container remotely

**Why you need it**:
- Check logs
- Restart services
- Debug issues
- Manage the container

**Configuration**: sshd_config tells it:
- Listen on port 4242 (not default 22)
- Security settings (authentication methods)

---

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│  Docker Container (Your Mini-Computer)  │
│                                         │
│  ┌─────────┐    ┌────────┐            │
│  │   Tor   │───→│ Nginx  │            │
│  │ Service │    │Port 80 │            │
│  │         │    │        │            │
│  │ Creates │    │ Serves │            │
│  │ .onion  │    │ HTML   │            │
│  └─────────┘    └────────┘            │
│       ↑              ↑                  │
│       │              │                  │
│  Tor Network    Port 80                │
│                                         │
│  ┌─────────┐                           │
│  │   SSH   │                           │
│  │Port 4242│ (for you to access)       │
│  └─────────┘                           │
│                                         │
└─────────────────────────────────────────┘
        ↑                    ↑
        │                    │
   Tor Network          SSH Client
   (visitors)             (you)
```

---

## Files You Need to Create

### 1. **nginx.conf** (Web Server Configuration)
**Purpose**: Tell Nginx how to serve your website

**What it needs**:
- Listen on port 80
- Point to HTML files location
- Serve index.html by default

---

### 2. **torrc** (Tor Configuration)
**Purpose**: Configure Tor to create hidden service

**What it needs**:
- HiddenServiceDir (where to store keys and hostname)
- HiddenServicePort (forward .onion:80 to localhost:80)

---

### 3. **sshd_config** (SSH Configuration)
**Purpose**: Configure SSH server

**What it needs**:
- Listen on port 4242
- Security settings
- Authentication methods

---

### 4. **Dockerfile** (Build Instructions)
**Purpose**: Instructions to build the Docker container

**What it needs**:
- Base image (Debian/Ubuntu)
- Install Nginx, Tor, SSH
- Copy configuration files
- Expose ports 80 and 4242
- Start all services

---

### 5. **index.html** ✓
**Purpose**: Your webpage

**Status**: Already created!

---

## Order of Implementation

1. **nginx.conf** (simplest - web server config)
2. **torrc** (Tor configuration)
3. **sshd_config** (SSH server config)
4. **Dockerfile** (brings everything together)
5. **Start script** (to run all services)
6. **Build & Test** (see it work!)

---

## Key Concepts to Remember

### Docker
- Container = isolated mini-computer
- Dockerfile = blueprint to build container
- Image = built container (snapshot)
- Running container = your services actually running

### Nginx
- Web server that serves static files
- Very simple for just HTML
- Configuration defines behavior

### Tor Hidden Service
- Gives you .onion address
- Provides anonymity for both server and visitors
- Routes traffic through encrypted network

### SSH
- Secure remote access
- Like a backdoor to manage your container
- On custom port 4242

---

## Questions to Explore Later

1. How does Tor generate the .onion address?
2. What's inside the HiddenServiceDir?
3. How to make SSH more secure?
4. What if you want HTTPS instead of HTTP?
5. How to persist data in Docker containers?

---

## Next Session

Continue with creating configuration files one by one, with detailed explanations of each line.
