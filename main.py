from functions import verify_user, calculate_tax, save_to_csv, read_from_csv, calculate_tax_relief


def main():
    print("=== Malaysian Tax Input Program ===")

    while True:
        registered = input("Are you registered? (Y/N): ").upper()
        if registered in ['Y', 'N']:
            break
        print("Please enter Y or N.")

    # IC number validation added here
    while True:
        ic_number = input("Enter your IC number (12 digits): ").strip()
        if len(ic_number) == 12 and ic_number.isdigit():
            break
        print("Invalid IC number. It must be exactly 12 digits and contain only numbers.")

    if registered == 'N':
        print("Registering new user...")
        password = input("Set password (last 4 digits of IC): ")
        if not verify_user(ic_number, password):
            print("Password must match last 4 digits of IC. Exiting.")
            return
        print("Registration successful!")

    # Login
    attempts = 3
    while attempts > 0:
        password = input("Enter password (last 4 digits of IC): ")
        if verify_user(ic_number, password):
            print("Login successful!")
            break
        else:
            attempts -= 1
            print(f"Incorrect password. Attempts remaining: {attempts}")
    else:
        print("Too many failed attempts. Exiting.")
        return

    # Input income
    while True:
        try:
            income = float(input("Enter annual income (RM): "))
            if income < 0:
                raise ValueError
            break
        except ValueError:
            print("Enter a positive number.")

    # Calculate tax relief automatically
    tax_relief = calculate_tax_relief()

    # Calculate tax
    tax_payable = calculate_tax(income, tax_relief)
    print(f"Your tax payable is: RM {tax_payable:,.2f}")

    # Save data
    record = {
        "IC Number": ic_number,
        "Income": income,
        "Tax Relief": tax_relief,
        "Tax Payable": tax_payable
    }
    save_to_csv(record)
    print("Data saved successfully!")

    # Display all records
    df = read_from_csv()
    if df is not None:
        print("\n=== Tax Records ===")
        print(df)


if __name__ == "__main__":
    main()
