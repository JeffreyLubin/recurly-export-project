import csv
import recurly
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import messagebox

# api_key intentionally left blank
api_key = ''
client = recurly.Client(api_key)

def subscriptions_csv_create(csv_name):
    """Create's a CSV file using the get_subscription Recurly endpoint"""  
    try:
        params = {"limit": 200}
        subscriptions = client.list_subscriptions(params=params).items()

        with open(csv_name, 'w', newline='') as file:
            writer_subscriptions = csv.writer(file)

            writer_subscriptions.writerow([
                "id", "state", "plan_code", "currency", 
                "account_code"
                ])

            for subscription in subscriptions:
                subscription_id = subscription.id
                state = subscription.state
                plan_code = subscription.plan.code
                currency = subscription.currency
                account_code = subscription.account.code

                writer_subscriptions.writerow([subscription_id, state, plan_code, currency, account_code])

        print("Csv Created!")

    except recurly.errors.ValidationError as e:
        # If the request was invalid, you may want to tell your user
        # why. You can find the invalid params and reasons in e.error.params
        print("ValidationError: %s" % e.error.message)
        print(e.error.params)
    except recurly.errors.NotFoundError as e:
        print("Some id was not found, probably the subscription.id. The error message will explain:")
        print(e)
    except recurly.NetworkError as e:
        print("Something happened with the network connection.")
        print(e)

def accounts_csv_create(csv_name):
    """Create's a CSV file using the get_accounts Recurly endpoint"""
    try:
        params = {"limit": 200}
        accounts = client.list_accounts(params=params).items()
        
        with open(csv_name, 'w', newline='') as file:
            writer_accounts = csv.writer(file)

            writer_accounts.writerow([
                'account_id', 'account_code', 'state', 'has_live_subscription',
                'created_at'
            ])
        
            for account in accounts:
                account_id = account.id
                account_code = account.code
                state = account.state
                has_live_subscription = account.has_live_subscription
                created_at = account.created_at

                writer_accounts.writerow([
                    account_id, account_code, state,
                    has_live_subscription, created_at,
                    ])
    
    except recurly.errors.ValidationError as e:
        print("ValidationError: %s" % e.error.message)
        print(e.error.params)
    except recurly.errors.NotFoundError as e:
        print("Some id was not found, probably the subscription.id. The error message will explain:")
        print(e)
    except recurly.NetworkError as e:
        print("Something happened with the network connection.")
        print(e)

def handle_user_selection():
    """The main program built to handle user selection in terminal"""
    while True:

        print("Please select an option from below: ")
        print("1.) Download Accounts Export")
        print("2.) Download Subscriptions Export")
        print("3.) Exit Program")

        user_selection = input("")

        if user_selection == '1':
            csv_name = input("What would you like your CSV to be named?").strip()
            if not csv_name.endswith('.csv'):
                csv_name += '.csv'
            accounts_csv_create(csv_name)

        elif user_selection == '2':
            csv_name = input("What would you like your CSV to be named?").strip()
            if not csv_name.endswith('.csv'):
                csv_name += '.csv'
            subscriptions_csv_create(csv_name)

        elif user_selection == '3':
            break

        else:
            print("Would you like to make another selection? Y / N")
            restart = input(user_selection).lower()
            if user_selection != 'y':
                break

def handle_user_selection_gui(export_type):
    csv_name = entry.get().strip()
    if not csv_name:
        messagebox.showerror("Error", "Please enter a filename!")
    
    if csv_name.endswith(".csv"):
        csv_name = csv_name[:-4]
    csv_name += ".csv"

    if export_type == "accounts":
        accounts_csv_create(csv_name)
        messagebox.showinfo("Confirmation!", f"The accounts export has been created as {csv_name}")
    elif export_type == "subscriptions":
        subscriptions_csv_create(csv_name)
        messagebox.showinfo("Confirmation!", f"The subscriptions export has been created as {csv_name}")


# Set Up Main Window
root = tk.Tk()
root.title("Csv Exporter")

# Asking for CSV file name:
tk.Label(root, text="Enter the CSV file name:")

# Entry field to input the CSV file name
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Buttons to select the export type
tk.Button(root, text = "Download Accounts Export", command = lambda: handle_user_selection_gui("accounts")).pack(pady=5)
tk.Button(root, text = "Download Subscriptions Export", command = lambda: handle_user_selection_gui("subscriptions")).pack(pady=5)

# Exit button
tk.Button(root, text = "Exit", command=root.quit).pack(pady=10)

# Start the GUI event loop

root.mainloop()

