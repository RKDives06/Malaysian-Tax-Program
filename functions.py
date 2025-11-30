import pandas as pd


def verify_user(ic_number, password):
    ic_number = ic_number.strip()
    password = password.strip()

    # Ensure IC is exactly 12 digits and numeric
    if len(ic_number) != 12 or not ic_number.isdigit():
        return False

    return ic_number[-4:] == password


def calculate_tax(income, tax_relief):
    chargeable = income - tax_relief
    if chargeable <= 0:
        return 0.0

    brackets = [
        (5000, 0.00),
        (20000, 0.01),
        (35000, 0.03),
        (50000, 0.06),
        (70000, 0.11),
        (100000, 0.19),
        (400000, 0.25),
        (600000, 0.26),
        (2000000, 0.28),
        (float("inf"), 0.30)
    ]

    tax = 0.0
    lower = 0.0
    for upper, rate in brackets:
        if chargeable > lower:
            taxable_amount = min(chargeable, upper) - lower
            tax += taxable_amount * rate
            lower = upper
        else:
            break
    return tax


def calculate_tax_relief():
    """
    Compute total tax relief based on user input for various categories.
    Returns total relief amount.
    """
    total_relief = 9000  # Individual relief
    print(f"Individual relief: RM {total_relief}")

    spouse = input(
        "Do you have a spouse with no income or ≤ RM4,000? (Y/N): ").upper()
    if spouse == 'Y':
        total_relief += 4000
        print("Added spouse relief: RM 4,000")

    while True:
        try:
            children = int(input("Number of children (0–12): "))
            if 0 <= children <= 12:
                total_relief += children * 8000
                print(f"Added child relief: RM {children * 8000}")
                break
            else:
                print("Enter a number between 0 and 12.")
        except ValueError:
            print("Invalid input. Enter a number.")

    while True:
        try:
            medical = float(input("Medical expenses (max RM 8,000): RM "))
            total_relief += min(medical, 8000)
            break
        except ValueError:
            print("Enter a valid number.")

    while True:
        try:
            lifestyle = float(input("Lifestyle expenses (max RM 2,500): RM "))
            total_relief += min(lifestyle, 2500)
            break
        except ValueError:
            print("Enter a valid number.")

    while True:
        try:
            education = float(input("Education fees (max RM 7,000): RM "))
            total_relief += min(education, 7000)
            break
        except ValueError:
            print("Enter a valid number.")

    while True:
        try:
            parental = float(input("Parental care (max RM 5,000): RM "))
            total_relief += min(parental, 5000)
            break
        except ValueError:
            print("Enter a valid number.")

    print(f"Total tax relief: RM {total_relief}")
    return total_relief


def save_to_csv(data, filename="tax_data.csv"):
    df = pd.DataFrame([data])
    try:
        old_df = pd.read_csv(filename)
        df = pd.concat([old_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv(filename, index=False)


def read_from_csv(filename="tax_data.csv"):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        print("No tax records found.")
        return None
