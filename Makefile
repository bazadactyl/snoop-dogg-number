SHELL := /bin/bash

prepare-venv: clean
	@echo "Preparing virtual environment..."
	virtualenv -p python3.7 --verbose --prompt='(sdn) ' env
	env/bin/pip install -r requirements.txt

update-requirements:
	@echo "Updating environment requirements..."
	cp requirements.txt requirements.txt.old
	env/bin/pip freeze > requirements.txt
	@echo "Applied the following changes to requirements.txt..."
	diff requirements.txt.old requirements.txt ; [ $$? -eq 1 ]  # diff returns non-zero codes
	rm -f requirements.txt.old

clean:
	@echo "Deleting old virtual environment..."
	rm -rf ./env
