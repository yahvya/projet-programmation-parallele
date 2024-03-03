from io import BytesIO, StringIO

from huffman_compression.compressor_exception import compressor_exception


##
# @brief gestion de décompression huffman
class huffman_decompressor:
    ##
    # @brief décompresse un fichier compressé dans un stream
    # @param readable_stream stream
    # @throws compressor_exception en cas d'erreur
    # @return le stream résultat de décompression
    @staticmethod
    def decompress_from(readable_stream: BytesIO):
        try:
            readable_stream = StringIO(readable_stream.read().decode())
            result_stream = BytesIO()

            # récupération du nombre de 0 ajoutés à la fin
            count_of_added_zeros = int(huffman_decompressor.__read_until_separator(readable_stream))

            # récupération de l'arbre
            tree = huffman_decompressor.__get_tree_from(readable_stream)

            # décompression du fichier
            bin_buff = ""

            while True:
                char = readable_stream.read(1)

                if not char:
                    break

                # ajout du binaire récupéré à partir de l'octet au buffer et tentative de récupération des caractères associés
                bin_buff += huffman_decompressor.__get_binary_from(char, 0)
                bin_buff = huffman_decompressor.__fill_from(bin_buff, tree, result_stream)

            if len(bin_buff) > 0:
                huffman_decompressor.__fill_from(bin_buff[:-count_of_added_zeros], tree, result_stream)

            return result_stream
        except compressor_exception as e:
            raise e
        except:
            raise compressor_exception("Une erreur s'est produite lors de la décompression")

    ##
    # @brief consume et récupère l'arbre d'association huffman à partir du stream
    # @param readable_stream stream
    # @return l'arbre récupéré inversé (clés binaires avec valeurs caractères)
    @staticmethod
    def __get_tree_from(readable_stream: StringIO) -> [str, str]:
        tree_len = int(huffman_decompressor.__read_until_separator(readable_stream))
        tree = {}

        for i in range(0, tree_len):
            char = readable_stream.read(1)
            count_of_added_zeros = int(huffman_decompressor.__read_until_separator(readable_stream))
            text_len = int(huffman_decompressor.__read_until_separator(readable_stream))
            tree[huffman_decompressor.__get_binary_from(readable_stream.read(text_len), count_of_added_zeros)] = char

        return tree

    ##
    # @brief consume et récupère le contenu du stream jusqu'à rencontrer le séparateur
    # @param readable_stream stream
    # @param separator le séparateur attendu
    # @return le contenu récupéré avant le séparateur
    @staticmethod
    def __read_until_separator(readable_stream: StringIO, separator: str = ":") -> str:
        buff = ""

        while True:
            el = readable_stream.read(1)

            if not el or el == separator:
                break

            buff += el

        return buff

    ##
    # @brief converti le caractère en chaine binaire en ignorant les 0 ajoutés à la fin
    # @param compressed_binary le binaire compressé
    # @param count_of_added_zeros nombre de 0 ajoutés à la fin
    # @return le binaire
    @staticmethod
    def __get_binary_from(compressed_binary: str, count_of_added_zeros: int) -> str:
        bin_buff = ""

        for char in compressed_binary:
            bin_buff += bin(ord(char))[2:].rjust(8, "0")

        return bin_buff[:-count_of_added_zeros] if count_of_added_zeros > 0 else bin_buff

    ##
    # tente de trouver un caractère et rempli le stream à partir du buffer
    # @param bin_buff buffer binaire
    # @param tree arbre inversé
    # @param result_stream résultat
    # @return le binaire restant
    @staticmethod
    def __fill_from(bin_buff: str, tree: [str, str], result_stream: BytesIO) -> str:
        end = 1

        while end <= len(bin_buff):
            searched_bin = bin_buff[:end]

            if searched_bin in tree:
                # si binaire est trouvé dans l'arbre, on réduit la chaine et on tente sur la suite
                result_stream.write(tree[searched_bin].encode())
                bin_buff = bin_buff[end:]
                end = 0

            end += 1

        return bin_buff
