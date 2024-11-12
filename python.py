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
data = pd.read_excel(file_path, sheet_name='Orders')

# Fill NaN values with appropriate defaults
data.fillna({
    'Customer ID': 'Unknown',
    'Order ID': '00000',
    'Order Date': pd.Timestamp('2024-01-01'),
    'Quantity': 0,
    'Sales': 0.0,
    'Discount': 0.0,
    'Delivery Cost': 0.0
}, inplace=True)

# Insert data into Bookings table if not already inserted
for _, row in data.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Bookings (CustomerID, BookingDate, BookingTime, TableNumber, NumberOfGuests, SpecialRequests, BookingStatus, StaffID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['Customer ID'], '2024-11-15', '19:00:00', 5, 4, 'No requests', 'Confirmed', 1))

    # Fetch the BookingID for the last inserted or existing booking
    cursor.execute("SELECT BookingID FROM Bookings WHERE CustomerID = %s AND BookingDate = %s;", 
                   (row['Customer ID'], '2024-11-15'))
    result = cursor.fetchone()

    if result:
        booking_id = result[0]  # Extract the BookingID if found
    else:
        print(f"No BookingID found for CustomerID: {row['Customer ID']} on BookingDate: '2024-11-15'. Skipping this row.")
        continue  # Skip this iteration if no valid BookingID is found

    # Insert data into Orders table with the fetched BookingID
    cursor.execute("""
        INSERT INTO Orders (OrderID, OrderDate, Quantity, TotalCost, Discount, DeliveryCost, BookingID)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (row['Order ID'], row['Order Date'], row['Quantity'], row['Sales'], row['Discount'], row['Delivery Cost'], booking_id))

# Commit the transaction and close the connection
con.commit()
cursor.close()
con.close()

print("Data insertion completed successfully.")




