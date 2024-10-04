mig:
	python manage.py makemigrations
	python manage.py migrate

super:
	python manage.py createsuperuser

loaddata:
	python manage.py loaddata regions
	python manage.py loaddata districts

uzbek:
	python manage.py makemessages -l uz

russia:
	python manage.py makemessages -l ru

uzbek_kiril:
	python manage.py makemessages -l oz

compile:
	python manage.py compilemessages --ignore=.venv