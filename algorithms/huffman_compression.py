from typing import BinaryIO

from algorithms.huffman_exception import HuffmmanException


##
# @brief compresseur de fichier basé sur l'algorithme de huffman
#
class HuffmanCompressor:
    ##
    # arbre interne
    tree: any = None

    ##
    # liaison caractère binaire
    assign_map: dict[str, str] = None

    ##
    # la donnée d'où provient l'arbre
    data: str = None

    ##
    # @brief construit l'arbre de huffman
    # @param str_data la donnée
    # @return si la construction de l'arbre s'est bien produite
    # @throws HuffmanException en cas d'erreur
    #
    def generate_tree_from_str(self, str_data: str) -> bool:
        assert str_data is not str

        # récupération du nombre occurrences de chaque caractère
        chars_map = {}

        for char in str_data:
            if char in chars_map:
                chars_map[char] += 1
            else:
                chars_map[char] = 1

        self.build_tree_from_char_map(chars_map)

        self.data = str_data

        return True

    ##
    # @brief construit l'arbre de huffman à partir d'un fichier
    # @param file_path le chemin complet du fichier
    # @return si la construction de l'arbre s'est bien produite
    # @throws HuffmanException en cas d'erreur
    #
    def generate_tree_from_file(self, file_path: str) -> bool:
        assert file_path is not str

        try:
            return self.generate_tree_from_str(HuffmanCompressor.convert_file_binary_to_string(open(file_path, "rb")))
        except OSError as _:
            raise HuffmmanException("Echec de lecture du fichier", True)
        except HuffmmanException as error:
            raise error
        except Exception as _:
            raise HuffmmanException("Une erreur s'est produite durant le traitement du fichier", True)

    ##
    # @brief construi l'arbre à partir de la map occurrences des caractères
    # @param chars_map map occurrences des caractères
    #
    def build_tree_from_char_map(self, chars_map: dict[str, int]) -> None:
        assert chars_map is not map

        # conversion de la map des caractères en point de l'arbre
        tree = [{"value": char, "sum": chars_map[char], "binary": None} for char in chars_map]

        while len(tree) > 1:
            # recherche des deux élements les plus petits de l'arbre
            smallest_one = 0 if tree[0]["sum"] < tree[1]["sum"] else 1
            smallest_two = 1 if smallest_one == 0 else 0

            for key in range(len(tree)):
                if tree[key]["sum"] < tree[smallest_one]["sum"]:
                    smallest_one = key
                elif tree[key]["sum"] < tree[smallest_two]["sum"]:
                    smallest_two = key

            # fusion des deux nœuds les plus petits
            new_node = {
                "sum": tree[smallest_one]["sum"] + tree[smallest_two]["sum"],
                "value": {
                    "left": tree.pop(smallest_one),
                    "right": tree.pop(smallest_two if smallest_two < smallest_one else smallest_two - 1)
                }
            }

            tree.append(new_node)

        self.tree = tree[0] if len(tree) == 1 else {"sum": 0, "value": "", "binary": None}

        self.assign_binary_in_tree(self.tree)

    ##
    # @return l'arbre ou None si non définis
    def get_tree(self) -> any:
        return self.tree

    ##
    # @brief affecte le binaire à chaque élement de l'arbre
    # @param tree l'arbre
    # @param start_binary code binaire actuel de l'élément
    def assign_binary_in_tree(self, tree: {dict[str,]}, start_binary: str = "") -> None:
        if "binary" in tree:
            tree["binary"] = start_binary
            # sauvegarde du lien charactère binaire
            self.assign_map[tree["value"]] = start_binary
        else:
            HuffmanCompressor.assign_binary_in_tree(tree["value"]["left"], start_binary + "0")
            HuffmanCompressor.assign_binary_in_tree(tree["value"]["right"], start_binary + "1")

    ##
    # @brief lis le contenu du fichier en mode binaire et le change en une suite de caractère à partir des octets
    # @param file fichier ouvert en mode lecture binaire (rb)
    # @return la chaine générée
    # @throws HuffmanException en cas d'erreur
    @staticmethod
    def convert_file_binary_to_string(file: BinaryIO) -> str:
        try:
            # conversion des octets du fichier en caractère
            result = "".join([chr(byte) for byte in file.read()])

            return result
        except Exception as _:
            raise HuffmmanException("Echec de conversion du contenu du fichier en chaine", False)


try:
    compressor = HuffmanCompressor()

    compressor.generate_tree_from_file("C:/Users/devel/Desktop/fichiers-temporaires/test.txt")
    print(compressor.get_tree())
except HuffmmanException as e:
    print(e.get_error_message())
