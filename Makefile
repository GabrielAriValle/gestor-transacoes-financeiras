PROJECT_NAME := gestor-transacoes
PYTHON_VERSION := 3.11.2

VENV_NAME := $(PROJECT_NAME)-$(PYTHON_VERSION)

create-venv:
	pyenv install $(PYTHON_VERSION) -v
	pyenv virtualenv $(PYTHON_VERSION) $(VENV_NAME)
	pyenv local $(VENV_NAME)
	pip install --upgrade pip
	pip install -r requirements.txt

migrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate