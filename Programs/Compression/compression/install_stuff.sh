chmod 755 compression/compression.py
echo "Changed permissions on compression" >> compression/install.log
mv compression/compression.service /etc/systemd/system/compression.service
echo "Loaded bsend compression" >> compression/install.log
systemctl start compression.service
