import socket
from typing import List

from fastapi import FastAPI
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
def get_files_to_download(files: List[str]):
    print(files)

    return []