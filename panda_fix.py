import pandas
def make_statement(statement, decoration):
    """" Emphasises headings by adding decoration
    at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}"


def calculate_unit_cost(cost, weight=0, volume=0, quantity=0):
    """Calculates unit price in dollars per kg, litre, or unit"""
    if weight > 0:
        unit_cost = cost / weight
        unit = "kg"
    elif volume > 0:
        unit_cost = cost / volume
        unit = "litre"
    else:
        quantity > 0
        unit_cost = cost / quantity
        unit = "item"

    return unit_cost, unit



def string_check(question, valid_answers=('yes', 'no'), num_letters=1):
    """Checks that users enter the full word or the first letter of a word from the list of valid responses"""
    while True:
        response = input(question).lower()
        for item in valid_answers:
            if response == item:
                return item
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


def num_check(question, num_type="float", exit_code=None):
    """Checks users enter integer / float that is more than zero (or the optional exit code)"""
    if num_type == "float":
        error = "Please enter a number more than zero"
    else:
        error = "Oops - please enter a number more than zero"

    while True:
        response = input(question)
        if response == exit_code:
            return response

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

*DISCLAIMER* : Please ensure that the items you are comparing with use the same unit. 


    ''')

# Main Routine goes here

# Initialise Items
MIN_ITEMS = 2
# Initialise variables / non-default options
measurement_ans = ('weight', 'w', 'volume', 'v', 'quantity', 'q')

# Lists to hold item details ( amount in g/ml/qty)
all_items = []
all_amounts = []  # grams or millilitres or quantity
all_costs = []

# Create DataFrame without converted column yet
price_tool_dict = {
    "Item": all_items,
    "Amount (g/ml)": all_amounts,
    "Cost": all_costs
}

print("Price Comparison Tool")

print()
# Ask if user wants instructions
want_instructions = string_check("Do you want to see the instructions? ")
if want_instructions == "yes":
    instructions()

# Get user budget
budget = num_check("Enter Budget $:", "float")

# Ask measurement type
item_type = string_check("Are your items measured in weight, volume, or quantity? ",
                         valid_answers=measurement_ans,
                         num_letters=1)

# Start item entry loop
while True:
    item = not_blank("Item Name: ")

# Obligates user to enter minimum of 2 items/entries
    if item.lower() == "xxx":
        if len(all_items) < MIN_ITEMS:
            print("Oops, you need at least two items before exiting.\n")
            continue
        else:
            break

    # Unit details
    if item_type in ['w', 'weight']:
        unit_name = "g"
        converted_unit = "kg"
    elif item_type in ['v', 'volume']:
        unit_name = "ml"
        converted_unit = "L"
    else:

        unit_name = "qty"
        converted_unit = "qty"

    # Allows users input to be converted so it can be calculated later on as $/kg or $/litre or $/quantity
    if item_type == "quantity":
        amount = num_check("Enter how many items (e.g. eggs): ", "integer")
    else:
        amount = num_check(f"Enter the item amount (in {unit_name}): ")


    # Asking user for the item's cost
    cost = num_check("Enter the item cost $", "float")

    # Append values to lists
    all_items.append(item)
    all_amounts.append(amount)
    all_costs.append(cost)

go_over_budget = string_check("Do you want to see recommendation even if they're over your budget? ", ('yes', 'no'))


# create dataframe / table from dictionary
price_tool_frame = pandas.DataFrame(price_tool_dict)

# Automatically convert to kg/L/qty based on user unit
price_tool_frame[f"Amount ({converted_unit})"] = price_tool_frame[f"Amount ({unit_name})"] / 1000

# Calculate Unit Price
price_tool_frame["Unit Price"] = (price_tool_frame["Cost"] / price_tool_frame[f"Amount ({converted_unit})"]).round(2)


# Currency formatting (using my currency function)
add_dollars = ['Cost', 'Unit Price']
for var_item in add_dollars:

    price_tool_frame[var_item] = price_tool_frame[var_item].apply(currency)
# Rename the 'Age' and 'Department' columns


# Print result with no index
print(price_tool_frame.to_string(index=False))
print()




