import socket
from typing import List

from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from communication_exception import communication_exception
from communication_config import communication_config
from server_client_manager import server_client_manager

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


##
# @brief crée une nouvelle connexion client
# @return la connexion
# @throws communication_exception en cas d'erreur
def get_client_conn():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((communication_config.address, communication_config.port))

        return client
    except Exception as _:
        raise communication_exception("Echec de récupération de connexion client")


@app.post("/get-files-list")
def get_files():
    try:
        client = get_client_conn()

        file_list = []

        client.send(server_client_manager.get_ressources_list.encode())

        # récupération de la liste des chemins de fichiers
        while True:
            filepath = client.recv(int(client.recv(4).decode())).decode()

            if filepath == communication_config.message_ending:
                break

            file_list.append({"path": filepath})

        # fermeture de la connexion
        client.send(server_client_manager.close_connection.encode())

        return {
            "success": True,
            "files": file_list
        }
    except communication_exception as e:
        return {
            "success": False,
            "error": e.get_error_message()
        }


@app.post("/download-files")
async def get_files_to_download(request: Request):
    try:
        # récupération de la liste des chemins attendue
        form = await request.form()

        files_path_list = form.getlist("files[]")

        files = []
        messages = []

        client = get_client_conn()

        # envoi du type de l'action
        client.send(server_client_manager.get_files_to_download.encode())

        # transmission des chemins de fichier à récupérer
        for path in files_path_list:
            path_message = path.encode()
            message_len = str(len(path_message)).encode()

            # transmission de la taille du futur message (chemin) à venir puis transmission du chemin
            client.send(message_len)
            client.send(path_message)

        # envoi de l'action marquant la fin de réception des fichiers
        end_sending_message = server_client_manager.end_filepath_sending.encode()

        client.send(str(len(end_sending_message)).encode())
        client.send(end_sending_message)

        # récupération des fichiers demandés compresses
        while True:
            data = client.recv(int(client.recv(4).decode())).decode()

            match data:
                case communication_config.message_ending:
                    break
                case communication_config.new_file:
                    # à faire
                    # récupération du nom du fichier à venir
                    # switch pour que toutes les nouvelles entrées soient dans le nouveau fichier
                    pass

                case communication_config.receive_file_part:
                    # à faire
                    # écrire dans le fichier ouvert les données
                    pass

        # fin de l'échange
        client.send(server_client_manager.close_connection.encode())

        return {
            "success": True,
            "files": {}
        }
    except communication_exception as e:
        return {
            "success": False,
            "error": e.get_error_message()
        }
    except Exception as _:
        return {
            "success": False,
            "error": "Une erreur s'est produite lors de la récupération des données"
        }
