#!/bin/bash
# Startup script for Tor Hidden Service Container
# This script starts all services in the correct order

set -e  # Exit on any error

echo "=========================================="
echo "Starting Tor Hidden Service Container"
echo "=========================================="

## 1. Create necessary directories ##
echo "[1/6] Creating directories..."

mkdir -p /var/www/html
mkdir -p /var/lib/tor/hidden_service
mkdir -p /var/log/tor
mkdir -p /var/log/nginx
mkdir -p /run/sshd

## 2. Set proper permissions ##
echo "[2/6] Setting permissions..."

# Tor directories (must be owned by tor user)
chown -R tor:tor /var/lib/tor
chmod 700 /var/lib/tor/hidden_service

# Nginx directories
chown -R www-data:www-data /var/www/html
chown -R www-data:www-data /var/log/nginx

# Tor log directory
chown -R tor:tor /var/log/tor

## 3. Copy HTML files to web root ##
echo "[3/6] Setting up website..."

# Copy index.html if it exists
if [ -f /app/index.html ]; then
    cp /app/index.html /var/www/html/
    chown www-data:www-data /var/www/html/index.html
    echo "   ✓ Copied index.html"
else
    # Create a default page if none exists
    echo "<h1>Tor Hidden Service is Running!</h1>" > /var/www/html/index.html
    chown www-data:www-data /var/www/html/index.html
    echo "   ✓ Created default index.html"
fi

## 4. Start Nginx ##
echo "[4/6] Starting Nginx..."

nginx -t  # Test configuration first
nginx     # Start Nginx

if pgrep nginx > /dev/null; then
    echo "   ✓ Nginx started successfully"
else
    echo "   ✗ Nginx failed to start"
    exit 1
fi

## 5. Start Tor ##
echo "[5/6] Starting Tor..."

# Start Tor in background
tor -f /etc/tor/torrc &

# Wait for Tor to create the hostname file
echo "   Waiting for Tor to generate .onion address..."
for i in {1..30}; do
    if [ -f /var/lib/tor/hidden_service/hostname ]; then
        break
    fi
    sleep 1
done

# Display the .onion address
if [ -f /var/lib/tor/hidden_service/hostname ]; then
    echo ""
    echo "=========================================="
    echo "🧅 YOUR TOR HIDDEN SERVICE ADDRESS:"
    echo "=========================================="
    cat /var/lib/tor/hidden_service/hostname
    echo "=========================================="
    echo ""
    echo "   ✓ Tor started successfully"
else
    echo "   ⚠ Warning: Tor started but .onion address not generated yet"
fi

## 6. Start SSH ##
echo "[6/6] Starting SSH..."

# Generate host keys if they don't exist
if [ ! -f /etc/ssh/ssh_host_rsa_key ]; then
    ssh-keygen -A
fi

# Start SSH daemon
/usr/sbin/sshd -f /etc/ssh/sshd_config

if pgrep sshd > /dev/null; then
    echo "   ✓ SSH started on port 4242"
else
    echo "   ✗ SSH failed to start"
fi

## 7. Display status ##
echo ""
echo "=========================================="
echo "✅ All services started!"
echo "=========================================="
echo ""
echo "Service Status:"
echo "  • Nginx:  Running on port 80"
echo "  • Tor:    Running (creating circuits...)"
echo "  • SSH:    Running on port 4242"
echo ""
echo "Access your site:"
echo "  • Local:  http://localhost"
echo "  • Tor:    http://$(cat /var/lib/tor/hidden_service/hostname 2>/dev/null || echo 'generating...')"
echo ""
echo "SSH access:"
echo "  ssh root@localhost -p 4242"
echo ""
echo "=========================================="

## 8. Keep container running and show logs ##
echo ""
echo "Monitoring logs (Ctrl+C to stop):"
echo "------------------------------------------"

# Tail logs from all services
tail -f /var/log/nginx/access.log \
        /var/log/nginx/error.log \
        /var/log/tor/notices.log 2>/dev/null
