#!/bin/bash
# pip install --user virtualenv	# permet d'installer l'environnement virtuel a 42 sans VM
# python3 -m virtualenv env # a la place de 'python3 -m venv env'
# source env/bin/activate
# pip install django	# installe django (no? seriously?)
# pip freeze > requirements.txt 	# documente les dependances

pip install virtualenv	# permet d'installer l'environnement virtuel a 42 sans VM
python3 -m venv env
source env/bin/activate 
pip install django
pip freeze > requirements.txt
