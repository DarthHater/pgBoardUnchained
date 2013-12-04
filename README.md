pgBoardUnchained
================

After years of mucking with the PHP flavor of pgBoard, I decided to rewrite it in Python for Django 1.6. Enjoi.

To setup pgBoardUnchained:

install and setup postgres 9.3

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

pip install -r requirements.txt

python manage.py migrate board