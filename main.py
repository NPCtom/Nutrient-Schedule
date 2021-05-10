from PyQt5 import QtWidgets
import os
import sys
from gui import NutrientUi


KEYS = ("Food ID", "Food name", "Energy (kJ)", "Protein (g)", "Fat, total (g)", "Fat, saturated (g)",
        "Available carbohydrate (g)", "Total sugars (g)", "Sodium (mg)")
NUTRIENT_PATH = "nutrients.txt"


class Nutrients:
    """
    Primary class for handling loading and parsing nutrient information
    from a provided filepath
    """
    def __init__(self, path):
        if not os.path.isfile(path):
            raise OSError("file doesn't exist")
        with open(path, errors='ignore') as nutrient_info:
            self.nutrient_info = self.parse_nutrient_info(nutrient_info.read())

    @staticmethod
    def parse_nutrient_info(data):
        parsed_tokens = []
        is_parsing_string = False

        for line in data.splitlines()[1:]:
            tokens = [""]
            for char in line:
                if is_parsing_string:
                    """
                    If string is being parsed, accept all characters
                    except the quotation mark itself
                    """
                    if char == '"':
                        is_parsing_string = False
                        tokens.append("")
                        continue
                    tokens[-1] += char
                else:
                    if char == '"':
                        is_parsing_string = True
                    elif char in " \t":
                        tokens.append("")
                    else:
                        tokens[-1] += char

            """
            Due to the data's formatting, residue is left as empty
            tokens, which need to be cleaned out using `filter`
            """
            tokens = [*filter(lambda k: k, tokens)]
            try:
                """
                About 0.01% of the sample data tested is misformatted,
                i.e. missing quotation marks around the description, hence
                it's necessary to skip those out because they can pose
                further issues chur chur
                """
                float(tokens[2])
            except ValueError:
                print(f"skipping {tokens[1]!r}, misformatted data")
                continue
            parsed_tokens.append(tokens)
        return parsed_tokens


if __name__ == "__main__":
    nutrients = Nutrients(NUTRIENT_PATH)
    app = QtWidgets.QApplication(sys.argv)
    window = NutrientUi(KEYS, nutrients.nutrient_info)
    app.exec_()
