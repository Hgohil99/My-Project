def show_menu():
    print("\n--- Personal Expense Tracker ---")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Total Balance")
    print("5. Exit")

def main():
    while True:
        show_menu()
        choice = input("Choose an option from (1-5): ")
        if choice == "1":
            print("You chose: Add Income")
        elif choice == "2":
            print("You chose: Add Expense")
        elif choice == "3":
            print("You chose: View Transactions")
        elif choice == "4":
            print("You chose: View Total Balance")
        elif choice == "5":
            print("GoodBye!, See You Soon")
            break
        else:
            print("Invalid Choice")

        if __name__ == "__main__":
            main()