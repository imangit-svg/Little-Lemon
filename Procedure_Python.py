import mysql.connector
import pandas as pd

# Establish the connection
con = mysql.connector.connect(
    user='root',
    host='localhost',
    database='db_littlelemon',
    passwd='Xoominboox'
)
cursor = con.cursor()

# Procedure to ensure the CustomerID exists in CustomerDetails
def ensure_customer_exists(cursor, con, customer_id, customer_name, city, country, postal_code, country_code, contact_number='000-000-0000', email_address='unknown@example.com'):
    cursor.execute("SELECT CustomerID FROM CustomerDetails WHERE CustomerID = %s;", (customer_id,))
    customer_exists = cursor.fetchone()
    
    if not customer_exists:
        cursor.execute("""
            INSERT INTO CustomerDetails (CustomerID, CustomerName, City, Country, PostalCode, CountryCode, ContactNumber, EmailAddress)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (customer_id, customer_name, city, country, postal_code, country_code, contact_number, email_address))
        con.commit()
        print(f"Customer with ID {customer_id} was added to CustomerDetails.")

# Procedure to ensure the StaffID exists in StaffInformation
def ensure_staff_exists(cursor, con, staff_id, first_name='John', last_name='Doe', role='Default Role', salary=30000.00):
    cursor.execute("SELECT StaffID FROM StaffInformation WHERE StaffID = %s;", (staff_id,))
    staff_exists = cursor.fetchone()

    if not staff_exists:
        cursor.execute("""
            INSERT INTO StaffInformation (StaffID, FirstName, LastName, Role, Salary)
            VALUES (%s, %s, %s, %s, %s);
        """, (staff_id, first_name, last_name, role, salary))
        con.commit()
        print(f"Staff with ID {staff_id} was added to StaffInformation.")

# Procedure to get the maximum quantity from Orders
def get_max_quantity(cursor):
    query = "SELECT MAX(Quantity) FROM Orders;"
    cursor.execute(query)
    max_quantity = cursor.fetchone()[0]
    print("Maximum quantity ordered:", max_quantity)
    return max_quantity

# Procedure to add a new booking
def add_booking(cursor, con, customer_id, booking_date, booking_time, table_number, num_guests, special_requests, booking_status, staff_id):
    ensure_customer_exists(cursor, con, customer_id, 'Default Name', 'Default City', 'Default Country', '00000', 'XX')  # Replace with actual values if needed
    ensure_staff_exists(cursor, con, staff_id)  # Ensure the StaffID exists

    query = """
    INSERT INTO Bookings (CustomerID, BookingDate, BookingTime, TableNumber, NumberOfGuests, SpecialRequests, BookingStatus, StaffID)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, (customer_id, booking_date, booking_time, table_number, num_guests, special_requests, booking_status, staff_id))
    con.commit()
    print("New booking added successfully.")

# Procedure to update a booking
def update_booking(cursor, con, booking_id, new_num_guests):
    query = """
    UPDATE Bookings
    SET NumberOfGuests = %s
    WHERE BookingID = %s;
    """
    cursor.execute(query, (new_num_guests, booking_id))
    con.commit()
    print(f"Booking with ID {booking_id} updated successfully.")

# Procedure to cancel a booking
def cancel_booking(cursor, con, booking_id):
    query = "DELETE FROM Bookings WHERE BookingID = %s;"
    cursor.execute(query, (booking_id,))
    con.commit()
    print(f"Booking with ID {booking_id} canceled successfully.")

# Procedure to manage a booking by checking if it exists and updating or adding
def manage_booking(cursor, con, booking_id, customer_id, booking_date, booking_time, table_number, num_guests, special_requests, booking_status, staff_id):
    cursor.execute("SELECT * FROM Bookings WHERE BookingID = %s;", (booking_id,))
    booking = cursor.fetchone()

    if booking:
        print(f"Booking with ID {booking_id} exists. Updating the booking.")
        update_booking(cursor, con, booking_id, num_guests)
    else:
        print(f"Booking with ID {booking_id} does not exist. Adding a new booking.")
        add_booking(cursor, con, customer_id, booking_date, booking_time, table_number, num_guests, special_requests, booking_status, staff_id)

# Example usage of the procedures
try:
    # Test the GetMaxQuantity procedure
    get_max_quantity(cursor)
    
    # Test the ManageBooking procedure
    manage_booking(cursor, con, 1, '72-055-7985', '2024-11-15', '19:00:00', 5, 4, 'Anniversary dinner', 'Confirmed', 1)
except mysql.connector.Error as err:
    print(f"Error: {err}")

# Close the cursor and connection when done
cursor.close()
con.close()
