# Functions go here
def make_statement(statement, decoration):
    """"Emphasises headings by adding decoration
    at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}"


def yes_no_check(question):
    """Checks that users enter yes / y or no / n to a question"""

    while True:
        response = input(question).lower()

        if response == "yes" or response == "y":
            return "yes"
        elif response == "no" or response == "n":
            return "no"
        else:
            print("please enter yes (y) or no (n).\n")


def not_blank(question):
    """Checks that a user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Sorry, this can't be blank. Please try again.\n")


def instructions():
    print(make_statement("Instructions", "ℹ️"))

    print('''

For each user, enter your budget/money you have on hand...
Then enter the following information
- Item Name
- Weight / Volume of Item
- Cost

The program will record the item information and calculate the 
unit price per kg.

Once you have entered all information products (minimum 2 items to compare) and enter the exit code ('xxx'), 
the program will display the items information. This  data will be  written to a text file.

It will also recommend the user on which item is purchase that's best suited within their budget.


    ''')


def num_check(question, num_type="float", exit_code=None):
    """Checks users enter integer / float that is more than
    zero (or the optional exit code)"""

    if num_type == "float":
        error = "Please enter an integer more than zero"

    else:
        error = "Oops - please enter a number more than zero"

    while True:

        response = input(question)

        # check for exit code and return it if entered
        if response == exit_code:
            return response

        # check datatype is correct and that number
        # is more than Zero
        try:

            if num_type == "float":
                response = float(response)
            else:
                response = int(response)

            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)


def currency(x):
    return "${:.2f}".format(x)


# Main Routine goes here

# Initialise Items
MIN_ITEMS = 2

# lists to hold item details
get_budget = []
all_items = []
all_items_weights = []
all_items_volume = []
all_cost = []

price_tool_dict = {
    'Budget': get_budget,
    'Item': all_items,
    'Weight': all_items_weights,
    'Volume': all_items_volume,
    'Cost': all_cost
}
print(make_statement("Price Comparison Tool", "💲"))

print()
want_instructions = yes_no_check("Do you want to see the instructions? ")
print()

if want_instructions == "yes":
    instructions()

print()

# Get user budget
get_budget = num_check("Enter Budget $:", "integer")

# loop to get items, weight/volume and cost
while MIN_ITEMS:

    # ask user for item  ( and check it's not blank)
    item = not_blank("Item: ")

    # if item is exit code, break out of loop
    if item == "xxx":
        break
    if item < 2:


    unit = num_check("Units: (eg 200g or 2l): ")
