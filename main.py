import sqlite3
from enum import Enum
from CustomerOrder import *
from Categories import *
from Product import *
from ProductProperties import *

connection = sqlite3.connect("CoffeeShopDB.db")
cursor = connection.cursor()

# Variable Declarations
userChoice = 0
customerNumber = 1

print("Welcome to David's Project #1: Coffee Shop POS System. This current state (beta) does not have any UI element "
      "nor does it have any AI elements. All inputs are to be manually given by the user (employee) for another "
      "customer")


def PromptForItem():
    # Displays a list of categories for user's to choose from
    print("Please choose a category to select from")
    categories = cursor.execute("SELECT CategoriesID,CategoryName FROM Categories")
    for y in categories.fetchall():
        print(str(y[0]) + ": " + str(y[1]))

    # Gets the user input
    category = input()

    # Displays the list of available items
    print("Please choose from the list of available items")
    products_available = cursor.execute(
        'SELECT ProductCatalogueId, ENname FROM ProductCatalogues WHERE CategoriesId = ?', (category,))
    for y in products_available:
        print(str(y[0]) + ": " + str(y[1]))

    # Gets the user input
    chosen_product = input()

    # Query a size
    size_available = cursor.execute("SELECT ProductSize FROM ProductProperties WHERE ProductCatalogueId = ?",
                                    (chosen_product[0],)).fetchmany(3)

    if size_available[0][0] is None:
        return category, None
    else:
        print("Please select the size of the drink you would like to have")
        for y in size_available:
            if y[0] == 0:
                print(str(y[0]) + ": Small")
            elif y[0] == 1:
                print(str(y[0]) + ": Medium")
            elif y[0] == 2:
                print(str(y[0]) + ": Large")

    drink_size = input()

    return category, drink_size


def get_customer_order():
    print("The current item in order is")

    result = cursor.execute("""
    SELECT CustomerOrders.CustomerOrderId, ProductCatalogues.ENname
    FROM CustomerOrders
    INNER JOIN ProductCatalogues ON CustomerOrders.ProductCatalogueId = ProductCatalogues.ProductCatalogueId
    """)
    print()  # Prints an empty line

    return result



while userChoice != 5:
    print("\nOptions: " +
          "\n1: Add an item to Customer Order" +
          "\n2: Delete an item from Customer Order" +
          "\n3: View the customer order list" +
          "\n4: Proceed with the Order" +
          "\n5: End day and generate a report for the day")

    userInput = int(input())

    if userInput == 1:

        # Prompts for user input
        category_id, product_property_id = PromptForItem()

        # Updates CustomerOrder with new foreign keys
        cursor.execute(
            'INSERT INTO CustomerOrders (ProductCatalogueId, ProductPropertiesId) VALUES (?, ?)',
            (category_id, product_property_id))

        # Commits the connection
        connection.commit()

        # Prints out the current items inside the order list
        result = get_customer_order()
        for i in result:
            print(i[1])

    elif userInput == 2:
        result = get_customer_order().fetchall()
        if result[0][0] is not None:
            print("What item would you like to delete")

            for i in result:
                print(str(i[0]) + ": " + str(i[1]))

            userInput = input()

            # Deletes the corresponding line
            cursor.execute("DELETE FROM CustomerOrders WHERE CustomerOrderId = ?",userInput)

            # Commit connection
            connection.commit()

        else:
            print("That item is not available")

    elif userInput == 3:
        result = get_customer_order().fetchall()

        for i in result:
            print(str(i[0]) + ": " + str(i[1]))
    # elif userInput == 4:
    #     # Do something
    # elif userInput == 5:
    #     # Do something
    # else:
    #     print("That is not a valid option")

print(cursor.fetchall())
