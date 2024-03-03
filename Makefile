# commandes d'initialisation de l'application

init-app:
	tsc -p interface/visual/includes/tsconfig.json
	python -m venv venv || python3 -m venv venv

install-requirements:
	python -m pip install --upgrade pip || python3 -m pip install --upgrade pip
	pip install -r requirements.txt || pip3 install -r requirements.txt

# commandes de lancement de l'application

# lance l'api client
launch-api:
	uvicorn interface.api:app --port 6060 --reload

# lance le serveur pour délivrer les fichiers html,css,js
launch-interface-server:
	@echo "Lancement du serveur d'interface client"
	python3 -m http.server -d interface/visual 8080 || python -m http.server -d interface/visual

# lance les outils utile à l'interface
launch-interface:
	@make -s -j 2 launch-interface-server launch-api

# lance le serveur
launch-server:
	cd communication && (python server.py || python3 server.py)

# lance tout les éléments utiles à l'application
launch-app:
	@make -s -j 2 launch-server launch-interface