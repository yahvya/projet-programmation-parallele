import json
from typing import TextIO
from collections import Counter

from CompressionException import CompressionException


##
# @brief compresseur de huffman
class HuffmanCompressor:

    ##
    # @brief compresse le fichier fourni
    # @param file_path chemin absolu du fichier à compresser
    # @return le contenu compressé du fichier
    # @throws CompressionException en cas d'erreur
    @staticmethod
    def compress_file(file_path: str) -> str:
        try:
            with open(file_path, 'r') as file_to_compress:
                return HuffmanCompressor.compress_tree(HuffmanCompressor.get_tree_from_file(file_to_compress),
                                                       file_to_compress)

        except CompressionException as e:
            raise e
        except Exception as _:
            raise CompressionException("Une erreur s'est produite")

    ##
    # @brief compresse l'arbre passée
    # @param tree l'arbre de huffman
    # @param file le fichier originaire de l'arbre
    # @return le contenu compressé
    # @throws CompressionException en cas d'erreur
    @staticmethod
    def compress_tree(tree: [str, ], file: TextIO) -> str:
        pass

    ##
    # @brief construit l'arbre de huffman à partir le fichier passé
    # @param file le fichier à compresser
    # @return l'arbre crée
    # @throws CompressionException en cas d'erreur
    @staticmethod
    def get_tree_from_file(file: TextIO) -> [str, ]:
        arr = [1,2,3,4]

        tmp_tree = Counter([*file.read()])

        if len(tmp_tree) == 0:
            raise CompressionException("Le fichier est vide")

        node_arr = [{"count": tmp_tree[el], "val": el, "binary": ""} for el in tmp_tree]

        while len(node_arr) > 1:

            # on défini les deux noeuds les plus petits par défaut (smaller one doit être plus petit que smaller two)
            smaller_one = 0 if node_arr[0]["count"] < node_arr[1]["count"] else 1
            smaller_two = 1 if smaller_one == 0 else 0

            for index in range(0, len(node_arr) - 1):
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

        return node_arr[0]
    ##
    # @brief associe les binaires dans l'arbre
    # @param tree l'arbre
    # @param binary le binaire à associer
    @staticmethod
    def create_binary_for_tree(tree: [str, ], binary: str = ""):
        pass


HuffmanCompressor.compress_file(
    "C:/Users/devel/Desktop/fac/master/master-1-dev-web-mobile-fullstack/semestre-2/programmation-parrallele-et-distribue/projet/resources/a-faire-morpheus.txt")
