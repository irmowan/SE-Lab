.PHONY: run clean

MODELS = user/models.py course/models.py homework/models.py
MIGRATIONS = user/migrations/*_initial.py user/migrations/*_auto_*.py \
	course/migrations/*_initial.py course/migrations/*_auto_*.py \
	homework/migrations/*_initial.py homework/migrations/*_auto_*.py \

run: db.sqlite3
	python3 manage.py runserver

db.sqlite3: $(MODELS) insertData.py
	rm -f db.sqlite3
	rm -f $(MIGRATIONS)
	python3 manage.py makemigrations
	python3 manage.py migrate
	env DJANGO_SETTINGS_MODULE=SELab.settings python3 insertData.py

clean:
	rm -f db.sqlite3
	rm -f $(MIGRATIONS)

