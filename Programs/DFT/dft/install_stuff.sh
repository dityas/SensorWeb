chmod 755 dft/dft.py
echo "Changed permissions on dft" >> dft/install.log
mv dft/dft.service /etc/systemd/system/dft.service
echo "Loaded bsend service" >> dft/install.log
systemctl start dft.service
