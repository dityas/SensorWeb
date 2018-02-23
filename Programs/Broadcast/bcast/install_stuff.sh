chmod 755 bcast/bsend.py
echo "Changed permissions on bsend" >> bcast/install.log
chmod 755 bcast/brecv.py
echo "Changed permissions on brecv" >> bcast/install.log
mv bcast/bsend.service /etc/systemd/system/bsend.service
echo "Loaded bsend service" >> bcast/install.log
mv bcast/brecv.service /etc/systemd/system/brecv.service
echo "Loaded brecv service" >> bcast/install.log
systemctl start bsend.service
systemctl start brecv.service
