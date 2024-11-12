import mysql.connector

# Establish the connection
con = mysql.connector.connect(
    user='root',
    host='localhost',
    database='db_littlelemon',
    passwd='Xoominboox'
)
cursor = con.cursor()

# 1. Create GetMaxQuantity stored procedure
create_get_max_quantity_proc = """
CREATE PROCEDURE GetMaxQuantity()
BEGIN
    SELECT MAX(Quantity) FROM Orders;
END;
"""
cursor.execute(create_get_max_quantity_proc)
print("Stored procedure GetMaxQuantity created successfully.")

# 2. Create AddBooking stored procedure
create_add_booking_proc = """
CREATE PROCEDURE AddBooking(
    IN customerID VARCHAR(50),
    IN bookingDate DATE,
    IN bookingTime TIME,
    IN tableNumber INT,
    IN numGuests INT,
    IN specialRequests VARCHAR(255),
    IN bookingStatus VARCHAR(50),
    IN staffID INT
)
BEGIN
    INSERT INTO Bookings (CustomerID, BookingDate, BookingTime, TableNumber, NumberOfGuests, SpecialRequests, BookingStatus, StaffID)
    VALUES (customerID, bookingDate, bookingTime, tableNumber, numGuests, specialRequests, bookingStatus, staffID);
END;
"""
cursor.execute(create_add_booking_proc)
print("Stored procedure AddBooking created successfully.")

# 3. Create UpdateBooking stored procedure
create_update_booking_proc = """
CREATE PROCEDURE UpdateBooking(
    IN bookingID INT,
    IN newNumGuests INT
)
BEGIN
    UPDATE Bookings
    SET NumberOfGuests = newNumGuests
    WHERE BookingID = bookingID;
END;
"""
cursor.execute(create_update_booking_proc)
print("Stored procedure UpdateBooking created successfully.")

# 4. Create CancelBooking stored procedure
create_cancel_booking_proc = """
CREATE PROCEDURE CancelBooking(
    IN bookingID INT
)
BEGIN
    DELETE FROM Bookings
    WHERE BookingID = bookingID;
END;
"""
cursor.execute(create_cancel_booking_proc)
print("Stored procedure CancelBooking created successfully.")

# 5. Create ManageBooking stored procedure
create_manage_booking_proc = """
CREATE PROCEDURE ManageBooking(
    IN bookingID INT,
    IN customerID VARCHAR(50),
    IN bookingDate DATE,
    IN bookingTime TIME,
    IN tableNumber INT,
    IN numGuests INT,
    IN specialRequests VARCHAR(255),
    IN bookingStatus VARCHAR(50),
    IN staffID INT
)
BEGIN
    DECLARE existing_booking INT;
    
    SELECT COUNT(*) INTO existing_booking 
    FROM Bookings 
    WHERE BookingID = bookingID;
    
    IF existing_booking > 0 THEN
        UPDATE Bookings
        SET NumberOfGuests = numGuests
        WHERE BookingID = bookingID;
    ELSE
        INSERT INTO Bookings (CustomerID, BookingDate, BookingTime, TableNumber, NumberOfGuests, SpecialRequests, BookingStatus, StaffID)
        VALUES (customerID, bookingDate, bookingTime, tableNumber, numGuests, specialRequests, bookingStatus, staffID);
    END IF;
END;
"""
cursor.execute(create_manage_booking_proc)
print("Stored procedure ManageBooking created successfully.")

# Commit the changes to create the procedures
con.commit()

# Verify the stored procedures in the database
check_procs_query = """
SELECT ROUTINE_NAME 
FROM INFORMATION_SCHEMA.ROUTINES 
WHERE ROUTINE_TYPE = 'PROCEDURE' 
AND ROUTINE_SCHEMA = 'db_littlelemon';
"""
cursor.execute(check_procs_query)
procedures = cursor.fetchall()
print("Stored Procedures in db_littlelemon:")
for proc in procedures:
    print(proc[0])

# Close the cursor and connection
cursor.close()
con.close()
