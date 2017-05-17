ln -s /var/www/md_resume/config/supervisor.conf /etc/supervisor/conf.d/md_resume.conf

ln -s /var/www/md_resume/config/nginx.conf /etc/nginx/sites-enabled/md_resume

pip3 install -r requirements.txt