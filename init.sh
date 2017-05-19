ln -s /var/www/md-resume/config/supervisor.conf /etc/supervisor/conf.d/md-resume.conf

ln -s /var/www/md-resume/config/nginx.conf /etc/nginx/sites-enabled/md-resume

pip3 install -r requirements.txt