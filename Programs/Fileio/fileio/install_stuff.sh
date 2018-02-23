chmod 755 fileio/fileio.py
echo "Changed permissions on fileio" >> fileio/install.log
mv fileio/fileio.service /etc/systemd/system/fileio.service
echo "Loaded bsend service" >> fileio/install.log
systemctl start fileio.service
