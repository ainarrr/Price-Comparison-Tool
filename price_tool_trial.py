def calculate_unit_cost(cost, weight, volume, quantity):
    """Calculates the unit price in dollars per kg or dollars per liter"""
    if weight > 0:  # If weight is available, calculate unit price per kg
        unit_price = cost / weight
        unit = "kg"
    elif volume > 0:  # If volume is available, calculate unit price per liter
        unit_price = cost / volume
        unit = "liter"
    else:
        quantity = 0  # In case neither weight nor volume is available
        unit = "unknown"
    return unit_price, unit


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


# Main Routine
MIN_ITEMS = 2
measurement_ans = ('weight', 'w', 'volume', 'v')
get_budget = []
all_items = []
all_items_weights = []
all_items_volume = []
all_cost = []
all_items_quantity = []

price_tool_dict = {
    'Budget': get_budget,
    'Item': all_items,
    'Weight': all_items_weights,
    'Volume': all_items_volume,
    'Cost': all_cost,
    'Quantity': all_items_quantity
}

print("Price Comparison Tool")
print()

want_instructions = string_check("Do you want to see the instructions? ")

if want_instructions == "yes":
    print('''
    For each user, enter your budget/money you have on hand...
    Then enter the following information:
    - Item Name
    - Weight / Volume of Item
    - Cost

    The program will record the item information and calculate the 
    unit price per kg.

    Once you have entered all information products (minimum 2 items to compare) and enter the exit code ('xxx'), 
    the program will display the items' information. This data will be written to a text file.

    It will also recommend the user on which item is best to purchase within their budget.
    ''')

# Get user budget
budget = num_check("Enter Budget $:", "float")
get_budget.append(budget)

while True:
    item = not_blank("Item Name: ")

    if item.lower() == "xxx":
        if len(all_items) < MIN_ITEMS:
            print("Oops, you need at least two items before exiting.\n")
            continue
        else:
            break

    # Ask for item's weight or volume
    weight_kg = 0  # Initialise weight as 0
    volume_l = 0  # Initialise volume as 0

    while True:
        item_type = string_check("Is your item measured in weight or volume? ", valid_answers=measurement_ans,
                                 num_letters=1)
        if item_type == "weight":
            weight_grams = num_check("Enter the item weight (in grams): ")
            weight_kg = weight_grams / 1000  # Convert grams to kilograms
            all_items_weights.append(weight_kg)
            all_items_volume.append(0)
            break
        elif item_type == "volume":
            volume_ml = num_check("Enter the item volume (in milliliters): ")
            volume_l = volume_ml / 1000  # Convert milliliters to liters
            all_items_volume.append(volume_l)
            all_items_weights.append(0)
            break
        elif item_type == "quantity":
            quantity = num_check("Enter amount")
            all_items_quantity.append(quantity)
            all_items_volume.append(0)
            all_items_weights.append(0)
        else:
            print("Please enter either 'weight' or 'volume'.")

    all_items.append(item)

    cost = num_check("Enter the item cost $", "float")
    all_cost.append(cost)

    # Calculate the unit price (dollars per kg or dollars per liter)
    unit_cost, unit = calculate_unit_cost(cost, weight_kg, volume_l, quantity)

    print(f"Unit Price: {currency(unit_cost)} per {unit}\n")




