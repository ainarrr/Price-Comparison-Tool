import pandas
from tabulate import tabulate
from datetime import date


def make_statement(statement, decoration):
    """" Emphasises headings by adding decoration
    at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}"


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
- Weight (mg/kg) / Volume of Item (ml/L) / Quantity (q)
- price

The program will record the item information and calculate the 
unit price per amount (kg/L/quantity).

Once you have entered all information products (minimum 2 items to compare) and enter the exit code ('xxx'), 
the program will display the items information. This  data will be  written to a text file.

It will also inform if the best item is 
the user on which item to purchase that is the best in value and inform whether
or not it is within their budget and by how much.

*DISCLAIMER* : Please be reasonable with the items you are comparing. 


    ''')


# Main Routine goes here

# Initialise variables / non-default options
measurement_ans = ('g', 'kg', 'ml', 'l', 'quantity')

# Lists to hold item details (names, amounts and prices)
all_items = []
all_amounts = []
all_prices = []
stand_amounts = []
all_unit_price = []
all_comparison = []

# printing title
print("Price Comparison Tool")
print()

# Ask if user wants instructions
want_instructions = string_check("Do you want to see the instructions? ")
if want_instructions == "yes":
    instructions()

# Get user budget
budget = num_check("Enter Budget $: ", "float")

# Ask measurement type
unit_type = string_check("Are your items measured in g, kg, ml, L or quantity? ",
                         valid_answers=measurement_ans,
                         num_letters=1)

# Get standard unit
if unit_type in ('g', 'kg'):
    stand_unit = "kg"
elif unit_type in ('ml', 'L'):
    stand_unit = "L"
else:
    stand_unit = "piece"

# Start item entry loop
while True:
    # Add space before each new item entry
    print()

    item = not_blank("Item Name: ")

    if item.lower() == "xxx":
        if len(all_items) < 2:
            print("Oops, you need at least two items before exiting.\n")
            continue
        else:
            break

    amount = num_check("Amount : ")

    # Convert amount to standard unit (kg for weight, L for volume, quantity unchanged)
    if unit_type in ('g', 'ml'):
        stand_amount = round(amount / 1000, 4)
    elif unit_type in ('kg', 'L'):
        stand_amount = amount
    else:
        stand_amount = amount


    # Get the item price
    price = num_check("Enter the item price $:", "float")

    # Calculate unit price per STANDARD unit (per kg, per L, or per item)
    unit_price = round(price / stand_amount, 2)

    # if price is greater than budget, make comparison infinite to bypass min system later
    if price > budget:
        comparison = float('inf')
    else:
        comparison = unit_price

    # append all items
    all_items.append(item)
    all_amounts.append(amount)
    all_prices.append(price)
    stand_amounts.append(stand_amount)
    all_unit_price.append(unit_price)
    all_comparison.append(comparison)

# Create DataFrame
price_tool_dict = {
    "Item": all_items,
    "Amount": all_amounts,
    "Amount (standard)": stand_amounts,
    "Price": all_prices,
    "Unit Price": all_unit_price
}
# create dataframe / table from dictionary
price_tool_frame = pandas.DataFrame(price_tool_dict)

# Currency formatting (using my currency function)
for var_item in ['Price']:
    price_tool_frame[var_item] = price_tool_frame[var_item].apply(currency)

    # make panda
    frame = pandas.DataFrame(price_tool_dict)

    tabulate_string = tabulate(frame, headers=["Item", f"Amount ({unit_type})", f"Amount ({stand_unit})", "Price ($)", "Unit Price ($)"],
                               tablefmt="psql", showindex=False)

# Prepare Strings for File Output
budget_heading = f"Budget: ${budget}"

# Getting values for the item with the best unit price
best_unit_price = min(all_unit_price)
best_index = all_unit_price.index(best_unit_price)
best_price = all_prices[best_index]
best_item = all_items[best_index]
best_stand_amount = stand_amounts[best_index]

# Recommendation section header
recommendation_heading = make_statement("Best  Value Recommendation", "-")
# Individual recommendation lines
recommended_item = f"Item: {best_item}"
recommended_price = f"Price: {currency(best_price)}"
recommended_unit_price = f"Unit Price: {currency(best_unit_price)} per {stand_unit}"
budget_summary = f"This item is over your budget by {currency(best_price - budget)}"

# if price is over budget, ask user if they want item with the best unit price under budget
if best_price > budget:
    want_budget = string_check(f"{best_item} is over your budget, would you like to see the best item under budget? ")
    if want_budget == "yes":
        best_unit_price = min(all_comparison)
        best_index = all_comparison.index(best_unit_price)
        best_price = all_prices[best_index]
        best_item = all_items[best_index]
        best_stand_amount = stand_amounts[best_index]

        # Individual recommendation lines
        recommended_item = f"Item: {best_item}"
        recommended_price = f"Price: {currency(best_price)}"
        recommended_unit_price = f"Unit Price: {currency(best_unit_price)} per {stand_unit}"
        budget_summary = f"This item is within your budget by {currency(budget - best_price)}"

# Headings
# strings / output area
# **** Get current date for heading and filename ****
today = date.today()

# Get day, month and year as individual strings
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")
# Headings / Strings...
main_heading_string = make_statement(f"Price Comparison Tool "
                                     f"({day}/{month}/{year})", "=")
table_heading = make_statement("Item Details", "-")

# Combine all output lines into one list
to_write = [
    main_heading_string,
    table_heading,
    budget_heading,
    tabulate_string, "\n",
    recommendation_heading,
    recommended_item,
    recommended_price,
    recommended_unit_price,
    budget_summary
]

# Print Area
print()
for item in to_write:
    print(item)

# Write to File
file_name = f"{year}_{month}_{day}"
write_to = "{}.txt".format(file_name)

text_file = open(write_to, "w+")

# write the item to file
for item in to_write:
    text_file.write(item)
    text_file.write("\n")