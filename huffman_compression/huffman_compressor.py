import typing
from collections import Counter
from io import BytesIO

from huffman_compression.compressor_exception import compressor_exception


##
# @brief gestion de compression de huffman
class huffman_compressor:
    ##
    # @brief taille de la chaine binaire avant compression et envoi du block
    # @attention >= 8 et multiple de 8
    len_before_submit = 8

    ##
    # @param filepath chemin absolu du fichier à compresser
    # @param to_do_on_compression_error fonction à appeler en cas d'erreur dans la compression, reçoit compressor_exception
    # @param to_do_on_tree_build fonction à appeler à la fin de la création de l'arbre, reçoit l'arbre formaté pour pouvoir être écrit dans un fichier au format nombre_el:(caractèrenombre_de_zeros_sur_le_binaire_compresse:taille_de_la_chaine:binaire_formaté....)
    # @param to_do_on_block_build fonction à appeler à la compression d'un block, reçoit le block compressé au format chars
    # @param to_do_on_compression_end fonction à appeler à la fin de la compression, reçoit le nombre de 0 ajouté à la fin (à mettre en seek 0)
    def __init__(
            self,
            filepath: str,
            to_do_on_compression_error: typing.Callable,
            to_do_on_tree_build: typing.Callable,
            to_do_on_block_build: typing.Callable,
            to_do_on_compression_end: typing.Callable
    ):
        self.filepath = filepath
        self.to_do_on_compression_error = to_do_on_compression_error
        self.to_do_on_tree_build = to_do_on_tree_build
        self.to_do_on_block_build = to_do_on_block_build
        self.to_do_on_compression_end = to_do_on_compression_end

    ##
    # @brief compresse le fichier
    # @return si la compression a réussi
    def compress(self) -> bool:
        try:
            with open(self.filepath, "r") as file:
                self.__build_tree(file)
                # formatage de l'arbre pour un format compressé
                formatted_tree = f"{len(self.tree)}:"

                for char in self.tree:
                    _, formatted_bin, count_of_added_zeros = huffman_compressor.compress_bin(self.tree[char], True)
                    formatted_tree += f"{char}{count_of_added_zeros}:{len(formatted_bin)}:{formatted_bin}"

                self.to_do_on_tree_build(formatted_tree)

                # compression de l'arbre
                file.seek(0)
                self.__compress_file_from_tree(file)

                return True
        except compressor_exception as e:
            self.to_do_on_compression_error(e)
        except:
            self.to_do_on_compression_error(compressor_exception("Une erreur s'est produite lors de la compression du fichier"))

        return False

    ##
    # @brief construit l'arbre
    # @param file le fichier à traiter
    # @throws compression_exception en cas d'erreur
    def __build_tree(self, file: typing.TextIO) -> None:
        self.tree = {}
        occurrences_map = Counter([*file.read()])

        # construction du tableau de nœuds
        node_arr: [[str, ]] = [{"count": occurrences_map[el], "val": el, "binary": ""} for el in occurrences_map]

        while len(node_arr) > 1:
            # définition des deux nœuds les plus petits par défaut (smaller one doit être plus petit que smaller two)
            smaller_one = 0 if node_arr[0]["count"] < node_arr[1]["count"] else 1
            smaller_two = 1 if smaller_one == 0 else 0

            for index in range(0, len(node_arr)):
                if index == smaller_one:
                    continue

                node = node_arr[index]

                # récupération de l'élément le plus petit
                if node["count"] < node_arr[smaller_one]["count"]:
                    smaller_one = index
                elif node["count"] < node_arr[smaller_two]["count"]:
                    smaller_two = index

            new_node = {
                "count": node_arr[smaller_one]["count"] + node_arr[smaller_two]["count"],
                "val": {
                    "left": node_arr[smaller_one],
                    "right": node_arr[smaller_two]
                }
            }

            # suppression des deux plus petits éléments
            del node_arr[smaller_one]
            del node_arr[smaller_two if smaller_two < smaller_one else smaller_two - 1]

            node_arr.append(new_node)

        if len(node_arr) > 0:
            self.__associate_binary_in_tree(node_arr[0])

    ##
    # @brief associe les binaires dans l'arbre
    # @param node nœud de l'arbre
    # @param binary le binaire actuel
    # @param left_code code associé en descendant du côté gauche de l'arbre
    def __associate_binary_in_tree(self, node: [str,], binary: str = "", left_code: str = "0") -> None:
        if not ("binary" in node):
            right_code = "1" if left_code == "0" else "0"
            self.__associate_binary_in_tree(node["val"]["left"], f"{binary}{left_code}")
            self.__associate_binary_in_tree(node["val"]["right"], f"{binary}{right_code}")
        else:
            self.tree[node["val"]] = binary

    # @brief compresse le fichier
    # @param file le fichier à traiter
    # @throws compression_exception en cas d'erreur
    def __compress_file_from_tree(self, file: typing.TextIO) -> None:
        binary_buffer = ""
        added_zeros = 0

        while True:
            char = file.read(1)

            if not char:
                break

            # association du caractère courant à son binaire
            binary_buffer += self.tree[char]

            if len(binary_buffer) >= huffman_compressor.len_before_submit:
                # compression du buffer des binaires pour la version compressé
                binary_buffer, result, _ = huffman_compressor.compress_bin(binary_buffer, False)
                self.to_do_on_block_build(result)

        if len(binary_buffer) > 0:
            # compression de la fin du fichier
            _, result, added_zeros = huffman_compressor.compress_bin(binary_buffer, True)
            self.to_do_on_block_build(result)

        self.to_do_on_compression_end(added_zeros)

    ##
    # compresse une chaine qui contient du binaire en un caractère
    # @param le buffer contenant le binaire
    # @param complete_end si des 0 doivent être complété à la fin
    # @return [reste du buffer si ne doit pas être complété, chaine de résultat, si complete_end true alors 0 ajoutées]
    @staticmethod
    def compress_bin(buffer: str, complete_end: bool):
        result = [buffer, "", 0]

        if complete_end:
            # on rajoute le nombre de 0 nécessaire pour avoir un multiple de 8
            buff_len = len(buffer)
            count_of_added_zeros = 8 - (buff_len % 8)
            result[2] = count_of_added_zeros
            buffer = buffer.ljust(buff_len + count_of_added_zeros, "0")

        while len(buffer) >= 8:
            # compression
            result[1] += chr(int(buffer[:8], 2))

            buffer = buffer[8:]

            if len(buffer) < 8:
                result[0] = buffer
                break

        return result

    ##
    # @brief crée un stream contenant les données compressés
    # @param filepath chemin absolu du fichier à compresser
    # @param to_do_on_compression_error fonction à appeler en cas d'erreur dans la compression, reçoit compressor_exception
    # @return le stream crée avec le curseur à 0 ou None si la fonction de gestion d'erreur a été appellé
    @staticmethod
    def create_compression_stream(filepath: str, to_do_on_compression_error: typing.Callable) -> BytesIO:
        stream = BytesIO()
        final_stream = BytesIO()

        return final_stream if huffman_compressor(
            filepath=filepath,
            to_do_on_compression_error=lambda e: to_do_on_compression_error(e),
            to_do_on_compression_end=lambda count_of_added_zeros: (
                final_stream.write(f"{count_of_added_zeros}:".encode()),
                final_stream.write(stream.getvalue()),
                final_stream.seek(0),
                stream.close()
            ),
            to_do_on_tree_build=lambda tree: stream.write(tree.encode()),
            to_do_on_block_build=lambda block: stream.write(block.encode())
        ).compress() else None
