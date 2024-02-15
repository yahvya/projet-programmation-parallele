init-app:
	python3 -m venv venv || python -m venv venv

install-requirements:
	pip install -r requirements.txt

launch-server:
	echo "lancement du serveur"

launch-client:
	echo "lancement du client"