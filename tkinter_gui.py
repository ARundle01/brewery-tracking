"""
This module is responsible for the Graphical User Interface of the program as a whole. It uses
Tkinter to construct a simple GUI that lets the user input new batches, as well as monitor current
batches; aspects such as current stage, tank, recipe, time at stage etc. can be viewed.
The user can also choose when to move a batch from one stage to the next, as the only person that
knows when the batch is ready is the user.
"""
# Imports
import tkinter as tk
from tkinter import ttk
import brewery_monitoring as b_m
import csv_prediction as predict

# Tkinter Frame init
MASTER = tk.Tk()
MASTER.title("Data Dashboard")
MASTER.resizable(True, True)

# Global Lists
LIST_OF_BATCHES = []


# Functions
def make_a_label(frame, text: str, column: int = 0, row: int = 0):
    """
    A function which makes a new label using arguments.

    This function makes a new Label widget inside the specified ttk frame, using the specified text,
    column and row arguments. Anything else about this Label cannot be changed, so new Labels that
    need to have textwrap or other features must be stated independently.

    :param frame: A ttk GUI frame
    :param text: str
    :param column: int = 0
    :param row: int = 0
    :return: None
    """
    ttk.Label(frame, text=text).grid(column=column, row=row)


def show_all_batches():
    """
    A function which shows all batches on the GUI.

    This function creates a list of all current batches, making new Label widgets for each batch.
    Any previous versions of the list are removed and then shown again, to act as a list refresh.

    :return: None
    """
    SHOW_ALL_BUTTON.configure(text="Update batch list")
    ttk.Label(MASTER, text="Name:").grid(column=0, row=2)
    ttk.Label(MASTER, text="Stage:").grid(column=1, row=2)
    ttk.Label(MASTER, text="Time:").grid(column=2, row=2)
    ttk.Label(MASTER, text="Quantity:").grid(column=3, row=2)
    ttk.Label(MASTER, text="Recipe:").grid(column=4, row=2)

    all_batches = b_m.view_all_batches_as_list()
    all_batch_names = []

    for b in all_batches:
        all_batch_names.append(b.name)

    iterator = 3

    for label in MASTER.grid_slaves():
        if int(label.grid_info()["row"]) > 2 and int(label.grid_info()["column"]) in \
                [0, 1, 2, 3, 4]:
            label.grid_forget()
    for batch in all_batches:
        if batch.name not in LIST_OF_BATCHES:
            LIST_OF_BATCHES.append(batch.name)

        weeks, hours = b_m.time_at_stage(batch.name)
        time = ("Weeks: " + str(weeks) + " Hours: " + str(hours))
        make_a_label(MASTER, batch.name, 0, iterator)
        make_a_label(MASTER, batch.stage, 1, iterator)
        make_a_label(MASTER, time, 2, iterator)
        make_a_label(MASTER, batch.quantity, 3, iterator)
        ttk.Label(MASTER, text=str(batch.recipe), wraplength=100, justify=tk.CENTER).grid(
            column=4, row=iterator
        )
        iterator += 1

    BATCH_STAGE_NAME_ENTERED["values"] = LIST_OF_BATCHES


def show_all_tanks():
    """
    A function which shows all empty tanks on the GUI.

    This function shows all tanks available to the user for batches. Any batches that reach stage 2
    or 3 must go into a tank (that has the capability to do stage 2, 3 or both), so this list tells
    the user which tanks are currently not being used.

    :return: None
    """
    for label in MASTER.grid_slaves():
        if int(label.grid_info()["row"]) > 2 and int(label.grid_info()["column"]) in [8, 9, 10]:
            label.grid_forget()
    SHOW_TANKS_BUTTON.configure(text="Update tank list")
    ttk.Label(MASTER, text="Name:").grid(column=8, row=2)
    ttk.Label(MASTER, text="Capability:").grid(column=9, row=2)
    ttk.Label(MASTER, text="Volume:").grid(column=10, row=2)
    iterator = 3
    for tank in b_m.available_tanks:
        make_a_label(MASTER, tank.name, 8, iterator)
        make_a_label(MASTER, tank.capability, 9, iterator)
        make_a_label(MASTER, str(tank.max_volume) + "L", 10, iterator)
        iterator += 1


def show_running_tanks():
    """
    A function which shows all tanks with batches in.

    This function creates a list of all tanks which currently contain batches. It contains
    information about the tank name, batch name and the stage the batch is on. If a batch needs to
    move from stage 2 to 3 and is already in a tank that can do stages 2 and 3, it will remain in
    the same tank.

    :return: None
    """
    SHOW_RUNNING_BUTTON.configure(text="Update running tank list")
    ttk.Label(MASTER, text="Name:").grid(column=12, row=2)
    ttk.Label(MASTER, text="Batch:").grid(column=13, row=2)
    ttk.Label(MASTER, text="Stage:").grid(column=14, row=2)
    iterator = 3
    for label in MASTER.grid_slaves():
        if int(label.grid_info()["row"]) > 2 and int(label.grid_info()["column"]) in [12, 13, 14]:
            label.grid_forget()

    for tank in b_m.running_tanks:
        make_a_label(MASTER, tank["tank"].name, 12, iterator)
        make_a_label(MASTER, tank["batch"].name, 13, iterator)
        make_a_label(MASTER, str(tank["batch"].stage), 14, iterator)
        iterator += 1


def add_new_batch_via_button():
    """
    A button event which creates a new batch on button press.

    This function creates a new batch when the corresponding button is pressed.

    :return: None
    """
    b_m.create_new_batch(BATCH_NAME.get(), BATCH_RECIPE.get(), BATCH_QUANTITY.get())


def choose_batch_via_button():
    """
    A button event which grabs the user input from the entry widgets and then allows the user to
    select a tank for
    their batch.

    :return: None
    """
    available_tanks = []
    for batch in b_m.view_all_batches_as_list():
        if batch.name == BATCH_STAGE_NAME_ENTERED.get():
            AVAILABLE_TANK_CHOSEN.configure(state="readonly")
            MOVE_BATCH_BUTTON.configure(state="normal")
            if batch.stage == "1" or batch.stage == "2":
                if batch.stage == "1":
                    for tank in b_m.available_tanks:
                        if tank.max_volume >= batch.volume and tank.capability in [
                            "Fermenter", "Fermenter/conditioner"
                        ]:
                            available_tanks.append(tank.name)
                    AVAILABLE_TANK_CHOSEN["values"] = available_tanks
                elif batch.stage == "2":
                    for tank in b_m.running_tanks:
                        if tank["batch"].name == batch.name and tank["tank"].capability in [
                            "Conditioner", "Fermenter/conditioner"
                        ]:
                            available_tanks.append(tank["tank"].name)
                    AVAILABLE_TANK_CHOSEN["values"] = available_tanks
            elif batch.stage == "3":
                AVAILABLE_TANK_CHOSEN.configure(state="disabled")


def move_batch_via_button():
    """
    A button event which moves a batch onto the next stage on button press.

    This function moves the specified batch on to the next stage in the process, with the tank that
    it must move into also being specified by the user.

    :return: None
    """
    chosen_tank = AVAILABLE_TANK_CHOSEN.get()
    chosen_batch = BATCH_STAGE_NAME_ENTERED.get()
    all_batches = b_m.view_all_batches_as_list()

    for batch in all_batches:
        if batch.name == chosen_batch:
            if batch.stage == "1":
                b_m.move_to_stage_2(chosen_batch, chosen_tank)
            elif batch.stage == "2":
                b_m.move_to_stage_3(chosen_batch, chosen_tank)
            elif batch.stage == "3":
                b_m.move_to_stage_4(chosen_batch)

    AVAILABLE_TANK_CHOSEN.configure(state="disabled")
    MOVE_BATCH_BUTTON.configure(state="disabled")


def disable_enable_button():
    """
    A function which disables a button if a checkbox has not been pressed and vice versa.

    If the checkbox is not checked, the button to create a new batch cannot be pressed. This is to
    prevent the user from creating batches with no name.

    :return: None
    """
    if NAME_CHECK.get() == "1":
        NEW_BATCH_BUTTON.configure(state="normal")
    elif NAME_CHECK.get() == "0":
        NEW_BATCH_BUTTON.configure(state="disabled")


def make_prediction():
    """
    A function which changes a label depending on the outcome of the sales prediction.

    :return: None
    """
    predict_name, predict_current, predict_prediction = predict.predict_on_current_stock()
    prediction1 = "You currently have a suitable amount of each recipe."
    prediction2 = "You should try brewing more Organic " + str(predict_name) + \
                  " as you currently have " + str(predict_current) + \
                  " bottles, with a prediction in two months of " + str(predict_prediction) + "."

    if predict_name is True and predict_current is False and predict_prediction is False:
        ttk.Label(MASTER, text=prediction1, wraplength=150, justify=tk.LEFT).grid(column=6, row=11)
    else:
        ttk.Label(MASTER, text=prediction2, wraplength=150, justify=tk.LEFT).grid(column=6, row=11)


def view_all_deliveries():
    """
    A function that views all batches that are at stage 4 and outputs them as a list to the user.
    """
    all_batches = b_m.view_all_batches_as_list(True)

    ttk.Label(MASTER, text="Name:").grid(column=15, row=2)
    ttk.Label(MASTER, text="Quantity:").grid(column=16, row=2)
    ttk.Label(MASTER, text="Recipe:").grid(column=17, row=2)

    for label in MASTER.grid_slaves():
        if int(label.grid_info()["row"]) > 2 and int(label.grid_info()["column"]) in [15, 16, 17]:
            label.grid_forget()

    iterator = 3
    for batch in all_batches:
        if batch.stage == "4":
            for _batch in LIST_OF_BATCHES:
                if _batch == batch.name:
                    LIST_OF_BATCHES.remove(_batch)

            make_a_label(MASTER, batch.name, 15, iterator)
            make_a_label(MASTER, batch.quantity, 16, iterator)
            ttk.Label(MASTER, text=str(batch.recipe), wraplength=100, justify=tk.CENTER).grid(
                column=17, row=iterator
            )
            iterator += 1

    BATCH_STAGE_NAME_ENTERED["values"] = LIST_OF_BATCHES


def main():
    """
    A function which starts the GUI.
    """
    b_m.create_required_tanks()
    MASTER.mainloop()

# GUI widgets for adding a new batch.
# Labels and Entry forms for Batch Name.
ADD_NEW_BATCH_LABEL = ttk.Label(MASTER, text="Add new batch:").grid(
    column=5, row=0, columnspan=2, sticky=tk.N
)
BATCH_NAME_LABEL = ttk.Label(MASTER, text="Batch Name:").grid(column=5, row=1)
BATCH_NAME = tk.StringVar()
BATCH_NAME_ENTERED = ttk.Entry(MASTER, width=18, textvariable=BATCH_NAME)
BATCH_NAME_ENTERED.grid(column=6, row=1)
# Checkbox to prevent empty name being submitted.
NAME_CHECK = tk.StringVar()
NAME_CHECK_BOX = tk.Checkbutton(
    MASTER, text="Add with this name", variable=NAME_CHECK, command=disable_enable_button
)
NAME_CHECK_BOX.deselect()
NAME_CHECK_BOX.grid(column=7, row=1)
# Labels and Entry forms for Batch Recipe.
BATCH_RECIPE_LABEL = ttk.Label(MASTER, text="Batch Recipe:").grid(column=5, row=2)
BATCH_RECIPE = tk.StringVar()
BATCH_RECIPE_ENTERED = ttk.Combobox(MASTER, width=15, textvariable=BATCH_RECIPE, state="readonly")
BATCH_RECIPE_ENTERED["values"] = ["Organic Red Helles", "Organic Pilsner", "Organic Dunkel"]
BATCH_RECIPE_ENTERED.current(0)
BATCH_RECIPE_ENTERED.grid(column=6, row=2)
# Labels and Entry forms for Batch Quantity.
BATCH_QUANTITY_LABEL = ttk.Label(MASTER, text="Batch Quantity").grid(column=5, row=3)
BATCH_QUANTITY = tk.IntVar()
BATCH_QUANTITY_ENTERED = ttk.Entry(MASTER, width=18, textvariable=BATCH_QUANTITY)
BATCH_QUANTITY_ENTERED.grid(column=6, row=3)
# Button for adding new batch
NEW_BATCH_BUTTON = ttk.Button(MASTER, text="Add Batch", command=add_new_batch_via_button)
NEW_BATCH_BUTTON.grid(column=6, row=4)
NEW_BATCH_BUTTON.configure(state="disabled")

# GUI widgets for the list of all batches.
ALL_BATCH_TITLE = ttk.Label(MASTER, text="All batches:").grid(
    column=0, row=0, columnspan=5, sticky=tk.N
)
SHOW_ALL_BUTTON = ttk.Button(MASTER, text="Show all batches", command=show_all_batches)
SHOW_ALL_BUTTON.grid(column=0, row=1, columnspan=5, sticky=tk.N)

# GUI widgets for the list of available tanks.
AVAILABLE_TANK_TITLE = ttk.Label(MASTER, text="Available Tanks:").grid(
    column=8, row=0, columnspan=3, sticky=tk.N
)
SHOW_TANKS_BUTTON = ttk.Button(MASTER, text="Show all tanks", command=show_all_tanks)
SHOW_TANKS_BUTTON.grid(column=8, row=1, columnspan=3, sticky=tk.N)

# GUI widgets for the list of running tanks.
RUNNING_TANK_TITLE = ttk.Label(MASTER, text="Running Tanks:").grid(
    column=12, row=0, columnspan=3, sticky=tk.N
)
SHOW_RUNNING_BUTTON = ttk.Button(MASTER, text="Show running tanks", command=show_running_tanks)
SHOW_RUNNING_BUTTON.grid(column=12, row=1, columnspan=3, sticky=tk.N)

# GUI widgets for moving batches between stages and selecting tanks for them.
MOVE_BATCH_STAGE_LABEL = ttk.Label(MASTER, text="Move batch stage:").grid(
    column=5, row=6, columnspan=2, sticky=tk.N
)
BATCH_STAGE_NAME_LABEL = ttk.Label(MASTER, text="Batch Name:").grid(column=5, row=7)
BATCH_STAGE_NAME = tk.StringVar()
BATCH_STAGE_NAME_ENTERED = ttk.Combobox(
    MASTER, width=18, textvariable=BATCH_STAGE_NAME, state="readonly"
)
BATCH_STAGE_NAME_ENTERED.grid(column=6, row=7)

AVAILABLE_TANK_LABEL = ttk.Label(MASTER, text="Tanks:")
AVAILABLE_TANK_LABEL.grid(column=5, row=8)
AVAILABLE_TANK = tk.StringVar()
AVAILABLE_TANK_CHOSEN = ttk.Combobox(
    MASTER, width=18, textvariable=AVAILABLE_TANK, state="disabled"
)
AVAILABLE_TANK_CHOSEN.grid(column=6, row=8)

CHOOSE_BATCH_BUTTON = ttk.Button(MASTER, text="Choose Batch", command=choose_batch_via_button)
CHOOSE_BATCH_BUTTON.grid(column=7, row=7)

MOVE_BATCH_BUTTON = ttk.Button(
    MASTER, text="Move to next stage", command=move_batch_via_button, state="disabled"
)
MOVE_BATCH_BUTTON.grid(column=6, row=9)

# GUI widgets for predictions.
PREDICTION_TITLE = ttk.Label(MASTER, text="Prediction:").grid(column=5, row=11)
PREDICT_BUTTON = ttk.Button(MASTER, text="Make prediction", command=make_prediction).grid(
    column=7, row=11
)

DELIVERY_TITLE = ttk.Label(MASTER, text="Delivery").grid(column=15, row=0, padx=25, columnspan=4)
DELIVERY_BUTTON = ttk.Button(MASTER, text="Show all deliveries", command=view_all_deliveries).grid(
    column=15, row=1, columnspan=4, padx=25
)

if __name__ == '__main__':
    main()
