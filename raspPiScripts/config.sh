#################### INSTALACJA FLASKA I VIRTUALENV #############################

# as root
$ apt-get install sudo
$ apt-get install raspi-config
$ raspi-config # expand to the filesystem and reboot
$ apt-get nano
$ adduser user
$ adduser user sudo
$ su user # switch to added user
$ sudo apt-get update
$ sudo apt-get install -y python python-pip python-virtualenv nginx gunicorn
$ sudo mkdir /home//user/www && cd /home/user/www
$ virtualenv -p /usr/bin/python3.4 env
$ source env/bin/activate
$ sudo mkdir server && cd server
$ sudo nano app.py #paste basic app to app.py
$ sudo mkdir static

##################### KONFIGURACJA NGINX ###################################

$ sudo /etc/init.d/nginx start
$ sudo rm /etc/nginx/sites-enabled/default
$ sudo touch /etc/nginx/sites-available/flask_project
$ sudo ln -s /etc/nginx/sites-available/flask_project /etc/nginx/sites-enabled/flask_project
$ sudo nano /etc/nginx/sites-enabled/flask_project
# Add following lines
# server {
#     location / {
#         proxy_pass http://localhost:8000;
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#     }
#     location /static {
#         alias  /home/www/flask_project/static/;
#     }
# }
$ sudo /etc/init.d/nginx restart
$ sudo pip install -r requirements.txt
#create error-logfile for gunicorn and add permission
$ sudo touch gunicorn-error.log
$ sudo chown user:user gunicorn-error.log
$ sudo chmod u+rw  gunicorn-error.log
$ sudo mkdir logs
$ sudo chown user:user logs
$ touch logs/gunicorn-access.log logs/gunicorn-error.log
$ gunicorn --access-logfile logs/gunicorn-access.log --error-logfile logs/gunicorn-error.log server:app -b localhost:8000

##################### KONFIGURACJA SUPERVISOR ##############################

$ sudo apt-get install -y supervisor
$ sudo nano /etc/supervisor/conf.d/broker.conf
# [program:broker]
# command = sudo mosquitto -d -p 1884
# user = user
#[program:server]
#command = /home/user/raspPiScripts/env/bin/gunicorn --access-logfile /home/user/raspPiScripts/logs/gunicorn-access.log --error-logfile /home/user/raspPiScripts/logs/gunicorn-err
#directory = /home/user/raspPiScripts/
#user = user

$ sudo supervisord -c /etc/supervisor/supervisord.conf
$ sudo supervisorctl reread
$ sudo supervisorctl update
$ sudo supervisorctl start server

#################### INSTALACJA MQTT ######################################
$ sudo apt-get insall mosquitto
$ sudo apt-get insall mosquitto-clients
