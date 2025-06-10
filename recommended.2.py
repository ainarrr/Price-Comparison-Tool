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


    ''')

# Main Routine goes here

# Initialise Items
MIN_ITEMS = 2
# Initialise variables / non-default options
measurement_ans = ('weight', 'w', 'volume', 'v', 'quantity', 'q')

# Lists to hold item details
all_items = []
all_items_units = []
all_cost = []

# Dictionary
price_tool_dict = {
    'Item': all_items,
    'Unit': all_items_units,
    'Cost': all_cost,
}

print("Price Comparison Tool")

print()
# Ask if user wants instructions
want_instructions = string_check("Do you want to see the instructions? ")
if want_instructions == "yes":
    instructions()

# Get user budget
budget = num_check("Enter Budget $:", "float")

# Start item entry loop
while True:
    item = not_blank("Item Name: ")

    if item.lower() == "xxx":
        if len(all_items) < MIN_ITEMS:
            print("Oops, you need at least two items before exiting.\n")
            continue
        else:
            break

    # Initialize all measurement types
    weight_kg = 0
    volume_l = 0
    quantity = 0

    # Ask measurement type
    item_type = string_check("Is your item measured in weight, volume, or quantity? ",
                             valid_answers=measurement_ans,
                             num_letters=1)

    # Allows users input to be converted so it can be calculated later on as $/kg or $/litre or $/quantity
    if item_type == "weight":
        weight_grams = num_check("Enter the item weight (in grams): ")
        weight_kg = weight_grams / 1000
    elif item_type == "volume":
        volume_ml = num_check("Enter the item volume (in millilitres): ")
        volume_l = volume_ml / 1000
    elif item_type == "quantity":
        quantity = num_check("Enter how many items (e.g. eggs): ", "integer")

    # Asking user for the item's cost
    cost = num_check("Enter the item cost $", "float")

    # Calculate unit cost
    unit_cost, unit = calculate_unit_cost(cost, weight_kg, volume_l, quantity)

    # Append values to lists
    all_items.append(item)
    all_items_units.append(unit)
    all_cost.append(cost)


    # Display unit cost to user
    print(f"Unit Price: {currency(unit_cost)} per {unit}\n")


# Find the item with the lowest unit cost
lowest_unit_cost = min(unit_cost)
index_of_cheapest = unit_costs.index(lowest_unit_cost)

go_over_budget = string_check("Do you want to see recommendation even if they're over your budget? ", ('yes', 'no'))

# Determine which item to recommend
if go_over_budget == "no":
    within_budget_items = []
    for i in range(len(all_cost)):
        if all_cost[i] <= budget:
            within_budget_items.append(i)

    if within_budget_items:
        best_index = within_budget_items[0]
        for i in within_budget_items:
            if unit_cost[i] < unit_cost[best_index]:
                best_index = i
    else:
        print("No items are within your budget. Showing the overall cheapest item instead.\n")
        best_index = index_of_cheapest
else:
    best_index = index_of_cheapest

# Display the recommended item
recommended_item = all_items[best_index]
recommended_price = all_cost[best_index]
recommended_unit_cost = unit_cost[best_index]

print(make_statement("Recommended Item", "*"))
print(f"The item with the lowest unit cost is '{recommended_item}' "
      f"at {currency(recommended_unit_cost)} per unit.")

if recommended_price > budget:
    over_amount = recommended_price - budget
    print(f"The recommended item is over your budget by {currency(over_amount)}.")
else:
    print("The recommended item is within your budget.")


