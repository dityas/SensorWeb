chmod 755 ansi_corr/ansi_corr.py
echo "Changed permissions on ansi_corr" >> ansi_corr/install.log
mv ansi_corr/ansi_corr.service /etc/systemd/system/ansi_corr.service
echo "Loaded bsend ansi_corr" >> ansi_corr/install.log
systemctl start ansi_corr.service
