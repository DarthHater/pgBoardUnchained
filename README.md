pgBoardUnchained
================

After years of mucking with the PHP flavor of pgBoard, I decided to rewrite it in Python for Django 1.6, and leverage node, redis and socket.io to make the board experience much neater. The text only approach is still in play with twitter bootstrap leading the styling charge. 

To setup pgBoardUnchained:

install and setup postgres 9.3

install node

install npm

install redis-server

setup database with vivalavinyl.settings.__init__.py values

install python

install virtualenv

cd ~

mkdir code

cd code

mkdir pgBoardUnchained

git clone https://github.com/DarthHater/pgBoardUnchained.git

createvenv pgboard

workon pgboard

npm install cookie

npm install socket.io

pip install redis

pip install -r requirements.txt

python manage.py migrate board

in a new terminal window cd to nodejs and node thread.js

in yet another terminal window sudo redis-server /usr/local/etc/redis.conf