FROM telegraf:1.28

# Install Python and pyudev
RUN apt-get update && apt-get install -y python3 python3-pip \
    && pip3 install --break-system-packages pyudev \
    && rm -rf /var/lib/apt/lists/*

# Copy the script into the image
COPY usb-watcher.sh /etc/telegraf/usb-watcher.sh

# Make it executable
RUN chmod +x /etc/telegraf/usb-watcher.sh

