create database db_littlelemon;
show databases;
USE db_littlelemon;

SELECT * FROM ordersview;
SELECT 
    c.CustomerID,
    c.CustomerName,
    o.OrderID,
    o.TotalCost,
    m.MenuName,
    mi.CourseName,
    mi.StarterName
FROM 
    Customers c
JOIN 
    Orders o ON c.CustomerID = o.CustomerID
JOIN 
    Menu m ON m.MenuItemID = o.MenuItemID  -- Adjust this join if necessary based on your schema
JOIN 
    MenuItems mi ON m.MenuItemID = mi.MenuItemID
WHERE 
    o.TotalCost > 150
ORDER BY 
    o.TotalCost ASC;
SELECT 
    cd.CustomerID,
    cd.CustomerName,
    o.OrderID,
    o.TotalCost,
    m.MenuName,
    mi.CourseName,
    mi.StarterName
FROM 
    customerdetails cd
JOIN 
    orders o ON cd.CustomerID = o.CustomerID
JOIN 
    menu m ON m.MenuItemID = o.MenuItemID  -- Adjust this join based on your actual schema
JOIN 
    menuitems mi ON m.MenuItemID = mi.MenuItemID  -- Ensure this join matches your schema
WHERE 
    o.TotalCost > 150
ORDER BY 
    o.TotalCost ASC;
SELECT 
    cd.CustomerID,
    cd.CustomerName,
    o.OrderID,
    o.TotalCost,
    m.MenuName,
    m.CourseName,  -- Assuming CourseName is in the menu table
    m.StarterName  -- Assuming StarterName is in the menu table
FROM 
    customerdetails cd
JOIN 
    orders o ON cd.CustomerID = o.CustomerID
JOIN 
    menu m ON m.MenuItemID = o.MenuItemID  -- Adjust this join based on your actual schema
WHERE 
    o.TotalCost > 150
ORDER BY 
    o.TotalCost ASC;
SELECT 
    cd.CustomerID,
    cd.CustomerName,
    o.OrderID,
    o.TotalCost,
    m.CuisineName,  -- Adjust as needed for the type of data
    m.CourseName,
    m.StarterName
FROM 
    customerdetails cd
JOIN 
    orders o ON cd.CustomerID = o.CustomerID
JOIN 
    orderdetails od ON o.OrderID = od.OrderID
JOIN 
    menu m ON od.MenuItemID = m.MenuItemID
WHERE 
    o.TotalCost > 150
ORDER BY 
    o.TotalCost ASC;
SELECT 
    cd.CustomerID,
    cd.CustomerName,
    o.OrderID,
    o.TotalCost,
    m.CuisineName,
    m.CourseName,
    m.StarterName
FROM 
    customerdetails cd
JOIN 
    bookings b ON cd.CustomerID = b.CustomerID
JOIN 
    orders o ON b.BookingID = o.BookingID
JOIN 
    orderdetails od ON o.OrderID = od.OrderID
JOIN 
    menu m ON od.MenuItemID = m.MenuItemID
WHERE 
    o.TotalCost > 150
ORDER BY 
    o.TotalCost ASC;

