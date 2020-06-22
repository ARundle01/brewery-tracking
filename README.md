# brewery-tracking

This repository contains code used for tracking sales data and for modelling the
brewing process of a brewery.

## What is this Project?
This is one of my University projects for the Programming module. The specification was to create a piece of software that could track the brewing process of a local brewery. Other requirements included:
- the ability to start new batches of beer
- the ability to move batches between stages of the process
- the ability to predict or suggest the next batch

## Installation and Dependencies

This code requires Python 3.7+, as was used in development. To install Python 3.7+,
see: [Python](https://www.python.org/downloads/).
All packages used are native to Python and do not require extra installation.

## Getting Started and Usage

To start the Data Dashboard, open the file: tkinter_gui.py and, if Python 3.7+ has been
installed correctly, a window will open.
This window is your main point of access for the whole system, and closing it down will
remove any current batches.

To begin, click the "Show all tanks" button and "Show running tanks" button. These
buttons will display all currently empty and running tanks. To update the lists, click
the corresponding buttons. IMPORTANT: The system does not automatically refresh the lists
seen, this must be done manually by pressing the corresponding "Refresh" button.

### Adding a new Batch

To add a new batch, input the name into the "Batch Name" field, choose a recipe from the
three provided and input a number between 1 and 2000 (this is the number of bottles to
make) into the "Batch Quantity" field. Finally, confirm the name by ticking the
"Add with this name" checkbox and click "Add Batch". Well Done! A new batch has been
created and can be seen by clicking the "Show all batches" button. **IMPORTANT: This
must be done after every new batch is created or when a batch is updated, as the list
does not automatically refresh.**

### Moving a batch to the next Stage

To move a batch to the next stage of the brewing process, refresh the batch list and
select the batch name from the "Batch Name" drop down. Once selected, click the 
"Choose Batch" button to confirm your choice. If the batch needs to be moved into a tank,
the tanks available to it will be displayed under the "Tanks" dropdown seen below. Select
your tank and, finally, click the "Move to next stage" button. Now, refresh all lists and
watch as the stage of the batch increases and any tanks that have been filled are moved to
the list of running tanks.

### Getting a prediction

To get a prediction from the program, simply click the "Make prediction" button. This will
display a short sentence advising you on which beer should be brewed next based on the 
amount that is currently being brewed and the predicted sales figures in two months.

### Showing deliveries

When a batch reaches stage 4, it is moved from the "All batches" list to the "Delivery"
list. To show this list, click the "Show all deliveries" button.
