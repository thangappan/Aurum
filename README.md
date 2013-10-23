Aurum
=====

This is my internal application development using Django framework and Tastypie application


Installation Steps ( Ubuntu and Debian )
==================

1. Application Installation 
----------------------------

1.1 Django Installation
-------------------------

sudo apt-get install python-setuptools
easy-install-2.7 django

1.2 Tastypie Installation
--------------------------

easy-install-2.7 python-mimeparse
easy-install-2.7 dateutil
easy-install-2.7 django-tastypie

1.3 Application Installation
----------------------------

mkdir /usr/local/api
git clone http://thangappanm@stash.nithini.com/scm/aur/aurum.git
password:

2. Deployment with apache server
---------------------------------

2.1. apache installation
------------------------

sudo apt-get install apache2


2.2 Django installation with mod-wsgi
-------------------------------------

sudo apt-get install libapache2-mod-wsgi

2.3 Adding our site to apache
-----------------------------

create the following file in /etc/apache2/sites-available directory

api.nithini.com

	ServerName api.nithini.com
    ServerAlias www.api.nithini.com
    WSGIScriptAlias / /usr/local/api/aurum/server/aurum/aurum/wsgi.py
    WSGIDaemonProcess api.nithini.com python-path=/usr/local/api/aurum/server/aurum:/usr/local/lib/python2.7/dist-packages/
    WSGIProcessGroup api.nithini.com
    <Directory /usr/local/api/aurum/server/aurum/aurum>
    <Files wsgi.py>
    Order deny,allow
    Allow from all
    </Files>
    </Directory>


# Enabling the above created site
a2ensite api.nithini.com

# reload the apache2 configuration 
service apache2 reload 

# Now HIT the following API to know the working condition of our deployment process
http://api.nithini.com/api/v1/count/1



	





