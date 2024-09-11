mig:
	python manage.py makemigrations
	python manage.py migrate

super:
	python manage.py createsuperuser

loaddata:
	python manage.py loaddata regions
	python manage.py loaddata districts