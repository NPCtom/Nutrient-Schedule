from PyQt5 import QtWidgets, uic
import sys


class RecipeUi(QtWidgets.QMainWindow):
    """
    Dialog for allowing the user to calculate
    serving nutrients, sizes and recipe ingredients
    """
    def __init__(self, parent, nutrient_info):
        super(RecipeUi, self).__init__(parent)
        uic.loadUi("recipe.ui", self)
        self.nutrient_info = nutrient_info
        self.calculate_button.clicked.connect(self.on_calculate)

    def on_calculate(self):
        self.recipe.clear()

        serving_size = self.serving_size.text()
        if not serving_size.isdigit():
            return self.serving_size.setText("must be numeric")

        serving_size = int(serving_size)
        protein, total_fat, sat_fat, carb, sugar, sodium = [*map(float, self.nutrient_info[3:])]

        """
        Calculate proportionate nutrients according to the serving
        size
        """
        scale_factor = serving_size / (protein + total_fat + sat_fat + carb + sugar + sodium/1000)  # sodium in mg

        ingredients = self.nutrient_info[1].split(", ")
        self.recipe.addItem(f"For {serving_size} g of {ingredients[0]!r}")
        self.recipe.addItem("Primary serving nutrients: ")
        self.recipe.addItem(f"\tProtein: {protein * scale_factor:.2f} g")
        self.recipe.addItem(f"\tCarbohydrates: {carb * scale_factor:.2f} g")
        self.recipe.addItem(f"\tTotal fat: {total_fat * scale_factor:.2f} g")
        self.recipe.addItem("Serving ingredients: ")

        """
        Some recipes, e.g. `Vodka` have no further
        ingredients
        """
        if not ingredients[1:]:
            self.recipe.addItem(f"\tNo ingredients")
            return

        scale_factor = 1/len(ingredients[1:])
        for idx, ingredient in enumerate(ingredients[1:]):
            self.recipe.addItem(f"\t#{idx}: {ingredient!r} ({serving_size*scale_factor:.2f}g)")


class NutrientUi(QtWidgets.QMainWindow):
    def __init__(self, keys, nutrient_info):
        super(NutrientUi, self).__init__()
        uic.loadUi("nutrient-info.ui", self)
        self.nutrient_info = nutrient_info

        self.nutrient_table.setColumnCount(len(nutrient_info[0]))
        self.nutrient_table.setRowCount(len(nutrient_info)+1)
        self.search_results.setColumnCount(len(nutrient_info[0]))

        """
        Set the keys
        """
        for column, key in enumerate(keys):
            item = QtWidgets.QTableWidgetItem(key)
            self.nutrient_table.setItem(0, column, item)

        """
        Load all food into GUI
        table
        """
        for row, datum in enumerate(nutrient_info):
            for column, info in enumerate(datum):
                item = QtWidgets.QTableWidgetItem(info)
                self.nutrient_table.setItem(row+1, column, item)

        self.nutrient_table.cellDoubleClicked.connect(self.on_nutrient_selected)
        self.search_button.clicked.connect(self.on_search_invoked)

        self.show()

    def on_nutrient_selected(self, row, _):
        row -= 1
        if not row:
            return
        recipe_wnd = RecipeUi(self, self.nutrient_info[row])
        recipe_wnd.show()

    def on_search_invoked(self):
        search_term = self.search.text().lower()
        search_results = []

        self.search_results.clear()

        if not search_term:
            return self.search.setText("invalid search-term")

        for row, nutrient in enumerate(self.nutrient_info):
            if search_term in nutrient[1].lower():
                search_results.append(nutrient)

        if not search_results:
            return self.search.setText("couldn't find search-term")

        self.search_results.setRowCount(len(search_results))

        for row, nutrient in enumerate(search_results):
            for column, info in enumerate(nutrient):
                item = QtWidgets.QTableWidgetItem(info)
                self.search_results.setItem(row, column, item)
