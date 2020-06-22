"""
This module is responsible for the monitoring and scheduling of batches of beer within the brewery.
It can create new batches, move them between the different stages of the brew process and check the
status of all batches and tanks. It is also responsible for importing the CSV file for predictions.
"""
# Imports
import csv
from datetime import datetime
import csv_prediction as predict

# Global lists
available_tanks: list = []
running_tanks: list = []
batches_s1: list = []
batches_s2: list = []
batches_s3: list = []
batches_s4: list = []

# Constants
VALID_RECIPE: set = {"Organic Pilsner", "Organic Red Helles", "Organic Dunkel"}
FERMENTER: str = "Fermenter"
CONDITIONER: str = "Conditioner"
FERMENTER_CONDITIONER: str = "Fermenter/conditioner"
CSV_FILE: list = ["Barnabys_sales_fabriacted_data.csv"]


# Classes
class Tank:
    """
    This class is used to define Tanks. A tank can hold one batch and has various attributes that
    dictate what kind of batch it can hold.

    attributes:
    name: str - the name of the tank
    max_volume: int - the maximum volume (in Litres) that a tank can hold
    capability: str - which stages of the process the tank can do
    current_state: str = "Idle" - the current state of the tank, (it is idle, fermenting or
    conditioning)
    """
    # Attribute volume is measured in litres (L) and capability describes what the tank can do.
    def __init__(self, name: str, max_volume: int, capability: str, current_state: str = "Idle"):
        self.name = name
        self.max_volume = max_volume

        if capability in ["Fermenter/conditioner", "Fermenter", "Conditioner"]:
            self.capability = capability
        else:
            raise ValueError("Invalid capability")

        if current_state in ["Idle", "Fermenting", "Conditioning"]:
            self.current_state = current_state
        else:
            raise ValueError("Invalid current state.")

    def change_current_state(self, new_state: str):
        """
        A class method which changes the current state of the tank.

        :param new_state: str
        :return: None
        """
        self.current_state = new_state


class Batch:
    """
    This class is used to define batches of beer and has various attributes which helps the user do
    that.

    class attributes:
    bottle_vol: float = 0.5 - the volume of any bottle that is in the batch
    time_started: datetime - the time at which the batch instance was created

    attributes:
    name: str - the name of the batch
    recipe: str - the recipe of the batch
    quantity: int - the number of bottles in the batch
    stage: str - the stage at which the batch is at. Stage 1 = Hot Brew, Stage 2 = Fermenting,
                    Stage 3 = Conditioning and Carbonation, Stage 4 = Bottling and Labelling.
    volume: float - the total volume of the batch. A product of bottle_vol and quantity.
    """
    # Class attribute bottle_vol is volume of single bottle, measured in litres (L).
    bottle_vol: float = 0.5
    time_started: datetime = datetime.now()

    def __init__(self, name: str, recipe: str, quantity: int, stage: str = "1"):
        if recipe in ["Organic Dunkel", "Organic Pilsner", "Organic Red Helles"]:
            self.recipe = recipe
        else:
            raise ValueError("Invalid recipe.")

        self.name = name
        self.quantity = quantity
        self.volume: float = quantity * self.bottle_vol

        if stage in ["1", "2", "3", "4"]:
            self.stage = stage
        else:
            raise ValueError("Invalid Stage")

    def change_stage(self, new_stage: str):
        """
        A class method which changes the current stage of the brewing process that the batch is on.

        :param new_stage: str
        :return: None
        """
        if new_stage in ["1", "2", "3", "4"]:
            self.stage = new_stage
        else:
            raise ValueError("Invalid stage")

    def update_time(self):
        """
        A class method which changes the time_started to the current time.

        :return: None
        """
        self.time_started = datetime.now()


# Functions
def create_new_tank(name: str, max_volume: int, capability: str):
    """
    A function which creates a new Tank object.

    This function creates a new Tank instance using the given name, max_volume and capability.
    If a ValueError is raised, it prints the error message to the terminal.

    :param name: str
    :param max_volume: int
    :param capability: str
    :return: None
    """
    try:
        tank = Tank(name, max_volume, capability, "Idle")
        available_tanks.append(tank)
    except ValueError as e:
        print(e)


def create_required_tanks():
    """
    A function which creates Tank instances using details about the current tanks which the client
    possesses.

    :return: None
    """
    create_new_tank("Albert", 1000, "Fermenter/conditioner")
    create_new_tank("Brigadier", 800, "Fermenter/conditioner")
    create_new_tank("Camilla", 1000, "Fermenter/conditioner")
    create_new_tank("Dylon", 800, "Fermenter/conditioner")
    create_new_tank("Emily", 1000, "Fermenter/conditioner")
    create_new_tank("Florence", 800, "Fermenter/conditioner")
    create_new_tank("Gertrude", 680, "Conditioner")
    create_new_tank("Harry", 680, "Conditioner")
    create_new_tank("R2D2", 800, "Fermenter")


def create_new_batch_manual_entry():
    """
    A function which allows for manual, command line entry of data. Used in development only.

    :return: None
    """
    name = input("Please input the name of the new batch.\n>> ")
    quantity: int = int(input("Please input the amount of bottles you would like to make.\n>> "))
    recipe = input("Please input the type of beer you would like to make.\n>> ")

    create_new_batch(name, recipe, quantity)


def create_new_batch(name: str, recipe: str, quantity: int):
    """
    A function which creates a new Batch instance.

    This function creates a new Batch instance using user input for name, quantity
    (number of bottles) and recipe. The recipe can only be one of three set recipes
    (Organic Pilsner, Organic Dunkel and Organic Red Helles). Client has not specified the need to
     be able to make batches of other recipes.

    :return: None
    """
    try:
        quantity = int(quantity)

        if quantity <= 2000 and recipe in VALID_RECIPE:
            batch = Batch(name, recipe, quantity)
            batches_s1.append(batch)
        elif quantity > 2000:
            print("You cannot make that many bottles in one batch.")
            create_new_batch()
        elif recipe not in VALID_RECIPE:
            print("That is not a valid type of beer. Must be one of %s" % VALID_RECIPE)
    except ValueError as e:
        print(e)


def show_relevant_tanks(stage: str, batch_volume: int):
    """
    A function which shows all available tanks which can be used for a batch at stage 2 or 3.
    Does not show tanks which can ferment and condition and have batches already.

    :param stage: str
    :param batch_volume: int
    :return: None
    """
    for tank in available_tanks:
        if stage == "2":
            if tank.capability in [FERMENTER, FERMENTER_CONDITIONER] and tank.max_volume >= \
                    batch_volume:
                print(tank.name)
        if stage == "3":
            if tank.capability in [CONDITIONER, FERMENTER_CONDITIONER] and tank.max_volume >= \
                    batch_volume:
                print(tank.name)


def choose_tank(stage: str, batch_volume: int) -> str:
    """
    A function which shows all relevant tanks for a specified stage, asks the user to choose one of
    those tanks and returns said tank.

    :param stage: str
    :param batch_volume: int
    :return: chosen_tank: str
    """
    show_relevant_tanks(stage, batch_volume)

    chosen_tank = input("Please input the tank that you would like to use for this batch.\n>> ")
    return chosen_tank


def view_all_batches():
    """
    A function which shows all batches at all stages.

    :return: None
    """
    view_by_stage("1")
    view_by_stage("2")
    view_by_stage("3")
    view_by_stage("4")


def view_by_stage(stage: str) -> None:
    """
    A function which shows all batches at a specified stage.

    :param stage: str
    :return: batch.name: str
    """
    if stage == "1":
        for batch in batches_s1:
            print(batch.name, "is at stage 1, waiting to move onto stage 2.")
    elif stage == "2":
        for batch in batches_s2:
            print(batch["batch"].name, "is at stage 2 in tank", batch["tank"].name,
                  ", waiting to move onto stage 3.")
    elif stage == "3":
        for batch in batches_s3:
            print(batch["batch"].name, "is at stage 3 in tank", batch["tank"].name,
                  ", waiting to move onto stage 4.")
    elif stage == "4":
        for batch in batches_s4:
            print(batch.name, "is at stage 4, waiting to be delivered.")


def view_all_batches_as_list(stage_4: bool = False) -> list:
    """
    A function which appends the names of every batch into one list.

    :return: all_batches: list
    """
    all_batches = []
    for batch in batches_s1:
        all_batches.append(batch)
    for batch in batches_s2:
        all_batches.append(batch["batch"])
    for batch in batches_s3:
        all_batches.append(batch["batch"])
    if stage_4:
        for batch in batches_s4:
            all_batches.append(batch)
    return all_batches


def move_to_stage_2(chosen_batch: str, chosen_tank: str, manual: bool = False):
    """
    A function which moves a batch from stage 1 to stage 2.

    This function asks the user to choose a batch from stage 1 which they would like to move to
    stage 2. It then displays all available tanks which can be used for stage 2 and asks the user to
    choose one. A dictionary containing the batch and tank is then created and appended to
    batches_s2 (a list of all batches at stage 2) and running_tanks (a list of all tanks that are
    currently operating). The batch and tank are then removed from batches_s1 and available_tanks
    respectively.

    :return: None
    """
    if manual:
        chosen_batch = input(
            "Please input the name of the batch you would like to move to stage 2.\n>> "
        )
    fermenter_dict = {}
    for batch in batches_s1:
        if batch.name == chosen_batch:
            if manual:
                chosen_tank = choose_tank("2", batch.volume)

            for tank in available_tanks:
                if tank.name == chosen_tank:
                    batch.change_stage("2")
                    batch.update_time()
                    fermenter_dict.update({"batch": batch, "tank": tank})
                    batches_s2.append(fermenter_dict)
                    batches_s1.remove(batch)

                    running_tanks.append(fermenter_dict)
                    available_tanks.remove(tank)


def move_to_stage_3(chosen_batch: str, chosen_tank: str, manual: bool = False):
    """
    A function which moves a batch from stage 2 to stage 3.

    This function asks the user which batch from stage 2 they would like to move to stage 3. If said
    batch is in a tank with the ability to ferment and condition (stage 2 and stage 3), the batch is
    not moved out of the tank; it is instead updated to stage 3 and moved into batches_s3 (list of
    batches at stage 3). The tank it is in is not changed. If the tank it is in is not able to
    condition (stage 3), any available tanks are displayed and the user is asked to choose one. The
    original tank is moved back into available_tanks and a new dictionary containing the batch and
    new tank is created. This dictionary is appended to batches_s3 (list of all batches at stage 3)
    and added to the list of running_tanks.

    :return: None
    """
    if manual:
        chosen_batch = input(
            "Please input the name of the batch you would like to move to stage 3.\n>> "
        )
    conditioner_dict = {}
    for batch in batches_s2[:]:
        if batch["batch"].name == chosen_batch:
            if manual:
                chosen_tank = choose_tank("3", batch["batch"].volume)

            if batch["tank"].capability in [FERMENTER_CONDITIONER]:
                batch["batch"].change_stage("3")
                batch["batch"].update_time()
                conditioner_dict.update({"batch": batch["batch"], "tank": batch["tank"]})
                batches_s3.append(conditioner_dict)
                batches_s2.remove(batch)

            else:
                for tank in available_tanks:
                    if tank.name == chosen_tank:
                        batches_s2.remove(batch)
                        batch["batch"].change_stage("3")
                        batch["batch"].update_time()

                        conditioner_dict.update({"batch": batch["batch"], "tank": tank})

                        available_tanks.remove(tank)
                        running_tanks.append(conditioner_dict)

                        batches_s3.append(conditioner_dict)


def move_to_stage_4(chosen_batch: str, manual: bool = False):
    """
    A function which moves batches from stage 3 to stage 4.

    :return: None
    """
    if manual:
        chosen_batch = input(
            "Please input the name of the batch you would like to move to stage 3.\n>> "
        )

    for batch in batches_s3:
        if batch["batch"].name == chosen_batch:
            batch["batch"].change_stage("4")
            batch["batch"].update_time()
            available_tanks.append(batch["tank"])
            running_tanks.remove(batch)
            batches_s4.append(batch["batch"])
            batches_s3.remove(batch)


def suggest_next_beer(file_name: str):
    """
    A function which suggests which beer to make next, based on a prediction of the current months
    quantity.

    :param file_name: str
    :return: None
    """
    current_month = datetime.now().strftime("%b")
    pilsner_predict = predict.predict_for_given_month("Organic Pilsner", current_month, file_name)
    helles_predict = predict.predict_for_given_month("Organic Red Helles", current_month, file_name)
    dunkel_predict = predict.predict_for_given_month("Organic Dunkel", current_month, file_name)

    if pilsner_predict > helles_predict and pilsner_predict > dunkel_predict:
        print("Pilsner could be the most wanted beer this month.")
    elif helles_predict > pilsner_predict and helles_predict > dunkel_predict:
        print("Red Helles could be the most wanted beer this month.")
    elif dunkel_predict > pilsner_predict and dunkel_predict > helles_predict:
        print("Dunkel could be the most wanted beer this month.")


def time_at_stage(chosen_batch: str) -> tuple:
    """
    A function which returns the number of weeks and hours a batch has been at a stage for.

    :param chosen_batch: str
    :return: weeks, hours: tuple
    """
    for batch in view_all_batches_as_list():
        if batch.name == chosen_batch:
            time_now = datetime.now()

            time_difference = time_now - batch.time_started
            seconds = time_difference.seconds
            weeks = seconds / (86400 * 7)
            hours = seconds / 3600
            if weeks < 1:
                if hours < 1:
                    return 0, 0
                else:
                    return 0, hours
            else:
                return weeks, hours


def upload_csv():
    """
    A function which allows the ability to upload a new CSV file with sales data.

    This function asks the user to input the name of the CSV that they would like to use to make
    predictions. If a CSV file is not chosen, an error is raised. Similarly, if the user selected
    CSV file does not have the same column headings as the originally supplied CSV file, a Value
    Error is raised. This prevents the user from selecting either a file that isn't a CSV file, or a
    file that does not contain the relevant data needed to make a prediction.

    :return: None
    """
    file_name = input(
        "Please input the file name of the csv file you would like to use for predictions.\n>> "
    )
    if file_name[-4:] != ".csv":
        print("This file is not a .csv file.")
        upload_csv()
    else:
        try:
            headings_are_right = []
            valid_headings = [
                "Invoice Number",
                "Customer",
                "Date Required",
                "Recipe",
                "Gyle Number",
                "Quantity ordered"
            ]
            with open(file_name, mode="r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                headings = next(csv_reader)
                for heading in headings:
                    if heading in valid_headings:
                        headings_are_right.append(True)
                    else:
                        headings_are_right.append(False)

                if False in headings_are_right[0:6]:
                    csv_file.close()
                    raise ValueError("One or more of the required columns are missing.")
                else:
                    CSV_FILE[0] = file_name
        except ValueError as e:
            print(e)
        except FileNotFoundError:
            print(
                "The file you requested could not be found. "
                "Barnabys_sales_fabriacted_data.csv will be used instead."
            )


if __name__ == "__main__":
    upload_csv()

    suggest_next_beer(CSV_FILE[0])
    create_required_tanks()

    create_new_batch_manual_entry()
    create_new_batch_manual_entry()
    create_new_batch_manual_entry()

    view_all_batches_as_list()
    view_all_batches()
    move_to_stage_2("", "", manual=True)
    move_to_stage_2("", "", manual=True)
    move_to_stage_2("", "", manual=True)
    view_all_batches()
    move_to_stage_3("", "", manual=True)
    view_all_batches()
