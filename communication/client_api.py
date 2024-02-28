import socket
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from communication_exception import communication_exception
from communication_config import communication_config
from server_client_manager import server_client_manager
from transmission_manager import transmission_manager

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

        transmission_manager.send_message(client, server_client_manager.get_ressources_list)

        # récupération de la liste des chemins de fichiers
        while True:
            data = transmission_manager.receive_message_from(client)["message"]

            if data == communication_config.message_ending:
                break

            file_list.append({"path": data})

        # fermeture de la connexion
        transmission_manager.send_message(client, server_client_manager.close_connection)

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

        # files = []
        # messages = []

        client = get_client_conn()

        # envoi du type de l'action
        transmission_manager.send_message(client, server_client_manager.get_files_to_download)

        # transmission des chemins de fichier à récupérer
        for path in files_path_list:
            transmission_manager.send_message(client, path)

        # envoi de l'action marquant la fin de réception des fichiers
        transmission_manager.send_message(client, server_client_manager.end_filepath_sending)

        match = {
            communication_config.new_file: lambda client_con: print("nouveau fichier : " + transmission_manager.receive_message_from(client_con)["message"]),
            # à faire
            # récupération du nom du fichier à venir
            # switch pour que toutes les nouvelles entrées soient dans le nouveau fichier
            communication_config.receive_file_part: lambda client_con: print("\t>> partie du fichier : " + transmission_manager.receive_message_from(client_con)["message"]),
            # à faire
            # écrire dans le fichier ouvert les données,
            communication_config.compression_error: lambda client_con: print("\t>> Erreur de connexion : " + transmission_manager.receive_message_from(client_con)["message"])
        }

        # récupération des fichiers demandés compressés
        while True:
            data = transmission_manager.receive_message_from(client)["message"]

            if data == communication_config.message_ending:
                break

            if data in match:
                match[data](client)

        # fin de l'échange
        transmission_manager.send_message(client, server_client_manager.close_connection)

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
