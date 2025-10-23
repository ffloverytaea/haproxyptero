FROM debian:11-bullseye

# Install HAProxy + Python3
RUN apt-get update && \
    apt-get install -y haproxy python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy files to /home/container/
COPY generate_haproxy.py /home/container/generate_haproxy.py
COPY haproxy.cfg /home/container/haproxy.cfg

# Make Python script executable
RUN chmod +x /home/container/generate_haproxy.py

# Set working directory
WORKDIR /home/container

# Default startup: generate haproxy.cfg then run HAProxy
CMD ["bash", "-c", "python3 /home/container/generate_haproxy.py && /usr/sbin/haproxy -f /home/container/haproxy.cfg"]
