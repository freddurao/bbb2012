git clone https://github.com/freddurao/bbb2012.git
cd bbb2012
sudo easy_install python-memcached
./manage.py syncdb
python manage.py test
python manage.py runserver