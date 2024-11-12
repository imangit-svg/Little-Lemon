import pandas as pd
import mysql.connector

# Establish the connection
con = mysql.connector.connect(
    user='root',
    host='localhost',
    database='db_littlelemon',
    passwd='Xoominboox'
)
cursor = con.cursor()

# Path to the Excel file
file_path = r"C:\Users\XoominBoox\Downloads\LittleLemon_data.xlsx"

# Load data from the Excel file
data = pd.read_excel(file_path)

# Print the column names to verify them
print("Column names in the DataFrame:", data.columns)

# Add default values for missing columns if needed
if 'BookingDate' not in data.columns:
    data['BookingDate'] = pd.Timestamp('2024-01-01')  # Replace with your desired default date

if 'BookingTime' not in data.columns:
    data['BookingTime'] = '00:00:00'  # Replace with your desired default time

if 'TableNumber' not in data.columns:
    data['TableNumber'] = 1  # Default table number

if 'NumberOfGuests' not in data.columns:
    data['NumberOfGuests'] = 2  # Default number of guests

if 'SpecialRequests' not in data.columns:
    data['SpecialRequests'] = 'None'  # Default special request

if 'BookingStatus' not in data.columns:
    data['BookingStatus'] = 'Confirmed'  # Default booking status

# Fill NaN values with appropriate defaults
data.fillna({
    'Customer ID': 'Unknown',
    'Customer Name': 'Anonymous',
    'City': 'Unknown City',
    'Country': 'Unknown Country',
    'Postal Code': '00000',
    'Country Code': 'XX',
    'Order ID': '00000',
    'Order Date': pd.Timestamp('2024-01-01'),
    'Quantity': 0,
    ' Cost': 0.0,  # Reference column with leading space
    'Sales': 0.0,
    'Discount': 0.0,
    'Delivery Cost': 0.0
}, inplace=True)

# Insert data into CustomerDetails table
for _, row in data.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO CustomerDetails (CustomerID, CustomerName, City, Country, PostalCode, CountryCode)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (row['Customer ID'], row['Customer Name'], row['City'], row['Country'], row['Postal Code'], row['Country Code']))

# Insert data into StaffInformation table
for _, row in data.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO StaffInformation (StaffID, FirstName, LastName, Role, Salary)
        VALUES (%s, %s, %s, %s, %s)
    """, (row.get('Staff ID', 1), 'John', 'Doe', 'Default Role', 30000.00))  # Replace with real data if available

# Insert data into Bookings table
for _, row in data.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Bookings (CustomerID, BookingDate, BookingTime, TableNumber, NumberOfGuests, SpecialRequests, BookingStatus, StaffID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['Customer ID'], row['BookingDate'], row['BookingTime'], row['TableNumber'], row['NumberOfGuests'], row['SpecialRequests'], row['BookingStatus'], row.get('Staff ID', 1)))

# Insert data into Orders table using INSERT IGNORE to avoid duplicates
for _, row in data.iterrows():
    # Ensure a valid BookingID exists
    cursor.execute("SELECT BookingID FROM Bookings WHERE CustomerID = %s AND BookingDate = %s;", 
                   (row['Customer ID'], row['BookingDate']))
    result = cursor.fetchone()

    # Clear any remaining result set to prevent the "Unread result found" error
    cursor.fetchall()

    if result:
        booking_id = result[0]  # Extract the BookingID if found
        cursor.execute("""
            INSERT IGNORE INTO Orders (OrderID, OrderDate, Quantity, TotalCost, Discount, DeliveryCost, BookingID)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (row['Order ID'], row['Order Date'], row['Quantity'], row[' Cost'], row['Discount'], row['Delivery Cost'], booking_id))
    else:
        print(f"Skipping row for CustomerID: {row['Customer ID']} - no valid BookingID found.")

# Insert data into Menu table with corrected column names
for _, row in data.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Menu (CourseName, CuisineName, StarterName, DessertName, DrinkName, Sides)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (row['Course Name'], row['Cuisine Name'], row['Starter Name'], row['Desert Name'], row['Drink'], row['Sides']))

# Commit the transaction and close the connection
con.commit()
cursor.close()
con.close()

print("Data insertion completed successfully.")
