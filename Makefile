mig:
	python manage.py makemigrations
	python manage.py migrate

super:
	python manage.py createsuperuser

loaddata:
	python manage.py loaddata regions
	python manage.py loaddata districts

uzbek:
	python manage.py makemessages -l uz -l oz -l ru

compile:
	python manage.py compilemessages --ignore=.venv