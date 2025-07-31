import pandas
from tabulate import tabulate
from datetime import date

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
- Weight (mg) / Volume of Item (ml) / Quantity (q)
- Cost

The program will record the item information and calculate the 
unit cost per amount (kg/L/quantity).

Once you have entered all information products (minimum 2 items to compare) and enter the exit code ('xxx'), 
the program will display the items information. This  data will be  written to a text file.

It will also recommend the user on which item to purchase that is the best in value and inform whether
or not it is within their budget and by how much.

*DISCLAIMER* : Please be reasonable with the items you are comparing. 


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
converted_amounts = []




print("Price Comparison Tool")

print()
# Ask if user wants instructions
want_instructions = string_check("Do you want to see the instructions? ")
if want_instructions == "yes":
    instructions()

# Get user budget
budget = num_check("Enter Budget $: ", "float")

# Ask measurement type
item_type = string_check("Are your items measured in weight, volume, or quantity? ",
                         valid_answers=measurement_ans,
                         num_letters=1)


# Start item entry loop
while True:
    # Add space before each new item entry
    print()

    item = not_blank("Item Name: ")


    if item.lower() == "xxx":
        if len(all_items) < MIN_ITEMS:
            print("Oops, you need at least two items before exiting.\n")
            continue
        else:
            break

    # Determine unit names
    if item_type in ['w', 'weight']:
        unit_name = "g"
        converted_unit = "kg"
        amount_label = "Amount (g)"
    elif item_type in ['v', 'volume']:
        unit_name = "ml"
        converted_unit = "L"
        amount_label = "Amount (ml)"
    else:
        unit_name = "qty"
        converted_unit = "qty"
        amount_label = "Quantity"

    # Get user amount when quantity
    if item_type in ['q', 'quantity']:
        amount = num_check("Enter how many items (e.g. eggs): ", "integer")
    else:
        amount = num_check(f"Enter the item amount (in {unit_name}): ")

    # Convert amount to standard unit
    if item_type in ['w', 'weight', 'v', 'volume']:
        converted_amount = amount / 1000
    else:
        converted_amount = amount

    # Get the item cost
    cost = num_check("Enter the item cost $:", "float")

    # Append the data
    all_items.append(item)
    all_amounts.append(amount)
    all_costs.append(cost)
    converted_amounts.append(converted_amount)


# Create DataFrame without converted column yet
price_tool_dict = {
    "Item": all_items,
    amount_label: all_amounts,
    "Cost": all_costs
}
# create dataframe / table from dictionary
price_tool_frame = pandas.DataFrame(price_tool_dict)

# Automatically convert to kg/L/qty based on user unit
price_tool_frame[f"Amount ({converted_unit})"] = converted_amounts


# Calculate Unit Price
price_tool_frame["Unit Price"] = (price_tool_frame["Cost"] / price_tool_frame[f"Amount ({converted_unit})"]).round(2)


# Currency formatting (using my currency function)
for var_item in ['Cost', 'Unit Price']:
    price_tool_frame[var_item] = price_tool_frame[var_item].apply(currency)



# Convert costs back to numbers for comparison
costs_as_numbers = []
unit_prices_as_numbers = []

for cost in price_tool_frame['Cost']:
    costs_as_numbers.append(float(cost.replace('$', '')))

for unit_price in price_tool_frame['Unit Price']:
    unit_prices_as_numbers.append(float(unit_price.replace('$', '')))

# Find best value (lowest unit price)
# If multiple items have the same unit price, the first one is chosen
unit_price = min(unit_prices_as_numbers)
best_index = unit_prices_as_numbers.index(unit_price)
best_item = all_items[best_index]
best_cost = costs_as_numbers[best_index]


#Prepare Strings for File Output

# Recommendation section header
recommendation_heading = make_statement("Best  Value Recommendation", "-")

# Individual recommendation lines
budge_heading = f"Budget: ${budget}"
recommended_item = f"Item: {best_item}"
recommended_cost = f"Cost: {currency(best_cost)}"
recommended_unit_price = f"Unit Price: {currency(unit_price)} per {converted_unit}"

# Budget summary
if best_cost > budget:
    budget_summary = f"This item is over your budget by {currency(best_cost - budget)}"
else:
    budget_summary = f"This item is within your budget by {currency(budget - best_cost)}"

# Table Output
if item_type in ['q', 'quantity']:
    table_string = tabulate(price_tool_frame[['Item', amount_label, 'Cost', 'Unit Price']],
                            headers='keys', tablefmt='psql', showindex=False)
else:
    table_string = tabulate(price_tool_frame[['Item', amount_label, f"Amount ({converted_unit})", 'Cost', 'Unit Price']],
                            headers='keys', tablefmt='psql', showindex=False)

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
    main_heading_string, budge_heading,
    table_heading,
    table_string,  "\n",
    recommendation_heading,
    recommended_item,
    recommended_cost,
    recommended_unit_price,
    budget_summary,
]

# Print Area
print()
for item in to_write:
    print(item)

# Write to File
file_name =f"{best_item}_{year}_{month}_{day}"
write_to =  "{}.txt".format(file_name)

text_file = open(write_to, "w+")

# write the item to file
for item in to_write:
    text_file.write(item)
    text_file.write("\n")
