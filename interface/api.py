import socket
from io import BytesIO

from fastapi import FastAPI,Request
from starlette.middleware.cors import CORSMiddleware
from termcolor import colored
from communication.server import server
from communication.client import client
from communication.transmission_manager import transmission_manager
from huffman_compression.huffman_decompressor import huffman_decompressor

print(colored("--- Lancement de l'api ---", "green"))

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/get-files")
def get_files():
    con = get_client_con()

    files = []

    # envoi de l'action de demande des fichiers
    transmission_manager.send_string_message(con, client.get_files)

    # réception des chemins
    while True:
        data = transmission_manager.receive_string_message(con)

        if data == client.transmission_end:
            break

        files.append({"path": data})

    transmission_manager.send_string_message(con, client.close_con)

    return {"files": files}


@app.post("/files-to-download")
async def get_files_to_download(request: Request):
    form = await request.form()

    files_path_list = form.getlist("files[]")

    client_con = get_client_con()

    # transmission des fichiers à télécharger
    transmission_manager.send_string_message(client_con, client.receive_files_to_download_action)

    for path in files_path_list:
        transmission_manager.send_string_message(client_con, path)

    transmission_manager.send_string_message(client_con, client.transmission_end)

    # récupération des fichiers
    stream_map = {}
    last_key = None

    while True:
        data = transmission_manager.receive_string_message(client_con)

        if data == client.transmission_end:
            break
        elif data == client.new_file:
            # récupération du nom du fichier
            last_key = transmission_manager.receive_string_message(client_con)
            stream_map[last_key] = BytesIO()
        elif data == client.receive_tree or data == client.receive_content:
            # réception de l'arbre ou du contenu
            stream_map[last_key].write(transmission_manager.receive_string_message(client_con).encode())
        elif data == client.compression_end:
            # réception du nombre de 0 ajoutés à la fin et construction du stream final
            final_stream = BytesIO()
            final_stream.write(f"{transmission_manager.receive_string_message(client_con)}:".encode())
            final_stream.write(stream_map[last_key].getvalue())
            stream_map[last_key].close()
            final_stream.seek(0)

            stream_map[last_key] = huffman_decompressor.decompress_from(final_stream)

    # fin de la connexion
    transmission_manager.send_string_message(client_con, client.close_con)

    # envoi des streams

    return {
        "files": {key: value.getvalue() for key, value in stream_map.items()}
    }


##
# @return une connexion client
def get_client_con() -> socket.SocketType:
    client_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_con.connect((server.address, server.port))

    return client_con
