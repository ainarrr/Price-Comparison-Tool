# Functions go here
def make_statement(statement, decoration):
    """" Emphasises headings by adding decoration
    at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}"


def string_check(question, valid_answers=('yes', 'no'), num_letters=1):
    """Checks that users enter the full word or the first letter of a word from the list of valid responses"""

    while True:
        response = input(question).lower()

        for item in valid_answers:
            # check if the response is the entire word
            if response == item:
                return item

            # check if it's the 'n' letters (abbreviation)
            elif response == item[:num_letters]:
                return item

        print(f"Please choose an option from {valid_answers}")



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
unit cost per kg.

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
# initialise variables / non-default option
measurement_ans = ('weight', 'w', 'volume', 'v')
# lists to hold item details
get_budget = []
all_items = []
all_items_weights = []
all_items_volume = []
all_cost = []
get_weight_or_volume = []

price_tool_dict = {
    'Budget': get_budget,
    'Item': all_items,
    'Weight': all_items_weights,
    'Volume': all_items_volume,
    'Cost': all_cost
}


print(make_statement("Price Comparison Tool", "💲"))
print()
want_instructions = string_check("Do you want to see the instructions? ")
print()

if want_instructions == "yes":
    instructions()

print()

# Get user budget
budget = num_check("Enter Budget $:", "integer")
get_budget.append(budget)


while True:
    # Get item name and check it is not blank
    item = not_blank("Item Name: ")

    # Check for exit code
    if item.lower() == "xxx":
        if len(all_items) < MIN_ITEMS:
            print("Oops, you need at least two items before exiting.\n")
            continue
        else:
            break

    # Ask for item's weight or volume
    # initialise weight as 0
    weight_kg = 0
    # initialise weight as 0
    volume_l = 0

    # Ask for item's weight or volume
    while True:
        item_type = string_check("Is your item measured in weight or volume? ", valid_answers=measurement_ans, num_letters=1)
        if item_type == "weight":
            weight_grams = num_check("Enter the item weight (in grams): ")
            weight_kg = weight_grams / 1000
            all_items_weights.append(weight_kg)
            all_items_volume.append(0)
            break
        elif item_type == "volume":
            volume_ml = num_check("Enter the item volume (in millilitres): ")
            volume_l = volume_ml / 1000
            all_items_volume.append(volume_l)
            all_items_weights.append(0)
            break
        else:
            print("Please enter either 'weight' or 'volume'.")


    # Add the current item to the list of all items
    all_items.append(item)

    # Ask the user to enter the cost of the item, ensuring the input is a valid float
    cost = num_check("Enter the item cost $", "float")

    # Append the validated cost to the list of all costs
    all_cost.append(cost)

