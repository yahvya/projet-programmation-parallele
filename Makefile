# initialise l'environnement python
init-env:
	python -m venv venv || python3 -m venv venv

# installe les librairies utiles au projet
install-requirements:
	pip install -r requirements.txt || pip3 install -r requirements

# lance le serveur local pour accéder à l'interface
launch-client-local-server:
	 python3 -m http.server -d communication/interface 8080 || python -m http.server -d communication/interface 8080

# lance l'utilitaire d'api du client
launch-client-api:
	uvicorn communication.client:app --reload

# lance les utilitaires du client
launch-client:
	make -j 2 launch-client-local-server launch-client-api

