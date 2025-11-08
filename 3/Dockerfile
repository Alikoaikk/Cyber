FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    nginx \
    tor \
    openssh-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY nginx.conf /etc/nginx/nginx.conf
COPY torrc /etc/tor/torrc
COPY sshd_config /etc/ssh/sshd_config
COPY index.html /var/www/html/index.html

RUN mkdir -p /var/www/html \
    && mkdir -p /var/lib/tor/hidden_service \
    && mkdir -p /var/log/tor \
    && mkdir -p /var/log/nginx \
    && mkdir -p /run/sshd \
    && chown -R debian-tor:debian-tor /var/lib/tor \
    && chmod 700 /var/lib/tor/hidden_service

RUN echo 'root:cyber.onion123' | chpasswd

EXPOSE 80
EXPOSE 4242

CMD service tor start && service ssh start && nginx -g 'daemon off;' 
