"""
This module is responsible for handling the data found within the provided CSV, to make predictions
about sales in any given month in the future. It can also sort the data by month, by recipe and
calculate figures such as percentage growth between months and the Average Annual Growth Rate.
"""
# Imports
import csv
from datetime import datetime
import brewery_monitoring as b_m

# Constants
VALID_RECIPE: set = {"Organic Pilsner", "Organic Red Helles", "Organic Dunkel"}
VALID_MONTH: list = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]


def import_to_dicts(file_name: str = "Barnabys_sales_fabriacted_data.csv") -> list:
    """
    A function which imports the chosen CSV file into a list of dictionaries.

    :param file_name: str

    :return: orders: list
    """
    with open(file_name, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        orders: list = []

        for row in csv_reader:
            order: dict = {"date": row[2], "quantity": row[5], "recipe": row[3]}
            orders.append(order)

        return orders


def sort_by_month(orders: list) -> tuple:
    """
    A function which sorts the contents of the CSV file into months.

    :param orders: List

    :return: tuple
    """
    jan: list = []
    feb: list = []
    mar: list = []
    apr: list = []
    may: list = []
    jun: list = []
    jul: list = []
    aug: list = []
    sep: list = []
    _oct: list = []
    nov: list = []
    dec: list = []
    for order in orders:
        if "Jan" in order["date"]:
            jan.append(order)
        elif "Feb" in order["date"]:
            feb.append(order)
        elif "Mar" in order["date"]:
            mar.append(order)
        elif "Apr" in order["date"]:
            apr.append(order)
        elif "May" in order["date"]:
            may.append(order)
        elif "Jun" in order["date"]:
            jun.append(order)
        elif "Jul" in order["date"]:
            jul.append(order)
        elif "Aug" in order["date"]:
            aug.append(order)
        elif "Sep" in order["date"]:
            sep.append(order)
        elif "Oct" in order["date"]:
            _oct.append(order)
        elif "Nov" in order["date"]:
            nov.append(order)
        elif "Dec" in order["date"]:
            dec.append(order)

    return jan, feb, mar, apr, may, jun, jul, aug, sep, _oct, nov, dec


def get_month_data(month: str, file_name: str) -> list:
    """
    A month which gets the data for a specified month.

    :param month: str
    :param file_name: str
    :return: list
    """
    jan, feb, mar, apr, may, jun, jul, aug, sep, _oct, nov, dec = \
        sort_by_month(import_to_dicts(file_name))
    if month == "Jan":
        return jan
    elif month == "Feb":
        return feb
    elif month == "Mar":
        return mar
    elif month == "Apr":
        return apr
    elif month == "May":
        return may
    elif month == "Jun":
        return jun
    elif month == "Jul":
        return jul
    elif month == "Aug":
        return aug
    elif month == "Sep":
        return sep
    elif month == "Oct":
        return _oct
    elif month == "Nov":
        return nov
    elif month == "Dec":
        return dec


def calc_month_quantity_by_recipe(month: str, recipe: str, file_name: str) -> int:
    """
    A function which calculates the quantity of a specific recipe for a specific month.

    :param month: str
    :param recipe: str
    :param file_name: str
    :return: int
    """
    if month not in VALID_MONTH:
        raise ValueError("Date must be one of %s." % VALID_MONTH)
    elif recipe not in VALID_RECIPE:
        raise ValueError("Recipe must be one of %s." % VALID_RECIPE)
    else:
        month_data: list = get_month_data(month, file_name)
        total_quantity: int = 0
        for order in month_data:
            if order.get("recipe") == recipe:
                total_quantity: float = total_quantity + int(order.get("quantity"))

        return total_quantity


def calc_recipe_quantity_ratio(
        first_month: str,
        first_recipe: str,
        second_recipe: str,
        file_name: str,
        second_month: str = None) -> float:
    """
    A function which calculates the ratio of quantity between two months.

    :param first_month: str
    :param first_recipe: str
    :param second_recipe: str
    :param file_name: str
    :param second_month: str
    :return: ratio: float
    """

    if first_month not in VALID_MONTH:
        raise ValueError("Date must be one of %s." % VALID_MONTH)
    elif first_recipe not in VALID_RECIPE or second_recipe not in VALID_RECIPE:
        raise ValueError("Recipe must be on of %s." % VALID_RECIPE)
    else:
        if second_month is None:
            second_month: str = first_month

        first_quantity: int = calc_month_quantity_by_recipe(first_month, first_recipe, file_name)
        second_quantity: int = calc_month_quantity_by_recipe(second_month, second_recipe, file_name)

        ratio = round(first_quantity / second_quantity, 2)

        return ratio


def calc_percent_growth_rate(
        last_month: str, this_month: str, recipe: str, file_name: str) -> float:
    """
    A function which calculates the percentage growth between two months.

    :param last_month: str
    :param this_month: str
    :param recipe: str
    :param file_name: str
    :return: percent_growth_rate: float
    """
    if last_month not in VALID_MONTH or this_month not in VALID_MONTH:
        raise ValueError("Date must be one of %s." % VALID_MONTH)
    elif recipe not in VALID_RECIPE:
        raise ValueError("Recipe must be one of %s." % VALID_RECIPE)
    else:
        last_month_quantity: int = calc_month_quantity_by_recipe(last_month, recipe, file_name)
        this_month_quantity: int = calc_month_quantity_by_recipe(this_month, recipe, file_name)

        percent_growth_rate: float = round(((this_month_quantity / last_month_quantity) - 1), 2)

        return percent_growth_rate


def calc_annual_growth_rate(recipe: str, file_name: str) -> float:
    """
    A function which calculates the Average Annual Growth Rate.

    :param recipe: str
    :param file_name: str
    :return: annual_growth_rate: float
    """
    if recipe not in VALID_RECIPE:
        raise ValueError("Recipe must be one of %s." % VALID_RECIPE)
    else:
        total_growth: float = (
                    calc_percent_growth_rate("Nov", "Dec", recipe, file_name)
                    + calc_percent_growth_rate("Dec", "Jan", recipe, file_name)
                    + calc_percent_growth_rate("Jan", "Feb", recipe, file_name)
                    + calc_percent_growth_rate("Feb", "Mar", recipe, file_name)
                    + calc_percent_growth_rate("Mar", "Apr", recipe, file_name)
                    + calc_percent_growth_rate("Apr", "May", recipe, file_name)
                    + calc_percent_growth_rate("May", "Jun", recipe, file_name)
                    + calc_percent_growth_rate("Jun", "Jul", recipe, file_name)
                    + calc_percent_growth_rate("Jul", "Aug", recipe, file_name)
                    + calc_percent_growth_rate("Aug", "Sep", recipe, file_name)
                    + calc_percent_growth_rate("Sep", "Oct", recipe, file_name)
        )

        annual_growth_rate: float = round((total_growth / 11), 2)
        return annual_growth_rate


def predict_for_given_month(recipe: str, month: str, file_name: str) -> float:
    """
    A function which predicts a quantity for a specific recipe for a specific month in the next
    year.

    :param recipe: str
    :param month: str
    :param file_name: str
    :return: predict_quantity: float
    """
    if recipe not in VALID_RECIPE:
        raise ValueError("Recipe must be one of %s." % VALID_RECIPE)
    elif month not in VALID_MONTH:
        raise ValueError("Month must be one of %s." % VALID_MONTH)
    else:
        annual_growth_rate: float = calc_annual_growth_rate(recipe, file_name)
        month_quantity: int = calc_month_quantity_by_recipe(month, recipe, file_name)

        predict_quantity: float = round(month_quantity + (month_quantity * annual_growth_rate))

        return predict_quantity


def predict_on_current_stock() -> tuple:
    """
    A function which can predict which beer should be made next based on sales figures and current
    batches of beer.

    :return: tuple
    """
    dunkel = 0
    helles = 0
    pilsner = 0

    current_month = datetime.now().strftime("%b")
    current_month_index = VALID_MONTH.index(current_month)
    if current_month_index == 10:
        in_two_month_index = 0
    elif current_month_index == 11:
        in_two_month_index = 1
    else:
        in_two_month_index = current_month_index + 2

    in_two_month = VALID_MONTH[in_two_month_index]

    helles_predict = predict_for_given_month("Organic Red Helles", in_two_month, b_m.CSV_FILE[0])
    dunkel_predict = predict_for_given_month("Organic Dunkel", in_two_month, b_m.CSV_FILE[0])
    pilsner_predict = predict_for_given_month("Organic Pilsner", in_two_month, b_m.CSV_FILE[0])

    predict_stock = [helles_predict, dunkel_predict, pilsner_predict]
    print(predict_stock[0])

    for batch in b_m.view_all_batches_as_list():
        if batch.recipe == "Organic Pilsner":
            pilsner = pilsner + batch.quantity
        elif batch.recipe == "Organic Dunkel":
            dunkel = dunkel + batch.quantity
        elif batch.recipe == "Organic Red Helles":
            helles = helles + batch.quantity

    stock = [dunkel, helles, pilsner]
    current_max = max(stock)
    current_min = min(stock)
    predict_max = max(predict_stock)
    predict_min = min(predict_stock)

    if current_max != 0:
        if stock.index(current_max) != 0 and predict_stock.index(predict_max) == 0:
            return "Dunkel", stock[0], predict_max
        elif stock.index(current_max) != 1 and predict_stock.index(predict_max) == 1:
            return "Red Helles", stock[1], predict_max
        elif stock.index(current_max) != 2 and predict_stock.index(predict_max) == 2:
            return "Pilsner", stock[2], predict_max
        elif current_min < predict_min:
            if stock.index(current_min) == 0:
                return "Dunkel", stock[0], predict_min
            elif stock.index(current_min) == 1:
                return "Red Helles", stock[1], predict_min
            elif stock.index(current_min) == 2:
                return "Pilsner", stock[2], predict_min
        else:
            return True, False, False
    else:
        if predict_stock.index(predict_max) == 0:
            return "Dunkel", stock[0], predict_max
        elif predict_stock.index(predict_max) == 1:
            return "Red Helles", stock[1], predict_max
        elif predict_stock.index(predict_max) == 2:
            return "Pilsner", stock[2], predict_max

    print(current_max, current_min, predict_max, predict_min)


if __name__ == "__main__":
    b_m.create_new_batch("Batch 1", "Organic Dunkel", 100)
    b_m.create_new_batch("Batch 2", "Organic Dunkel", 100)
    b_m.create_new_batch("Batch 3", "Organic Dunkel", 100)
    b_m.create_new_batch("Batch 4", "Organic Dunkel", 100)
    b_m.create_new_batch("Batch 5", "Organic Dunkel", 100)
    b_m.create_new_batch("Batch 6", "Organic Dunkel", 100)
    b_m.create_required_tanks()

    predict_on_current_stock()
