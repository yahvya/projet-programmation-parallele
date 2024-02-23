# initialise l'environnement python
init-env:
	python -m venv venv || python3 -m venv venv

install-requirements:
	pip install -r requirements.txt || pip3 install -r requirements

launch-client:
	 uvicorn communication.client:app --reload

