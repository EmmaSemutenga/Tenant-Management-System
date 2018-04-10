# Tenant-Management-System
System to manage tenants
Owner or landloard will manage the system

As the owner:
1-Should be able to login
2-Should be able to add, delete, update,  houses information
3-Should be able to add other and remove users(Fellow Admins)
4-Should be able to add, remove and update tenants (to free house)
5-Should be able to add payments
6-Should be able to search for tenants
7-Should be able to print payment, tenant details
8-Should be able to export details to csv

Database: Rental
Table: Owners; id, name, username, password
Table: Houses; id, house_no, type_of_house, location, rent_amount, status(availability)
Table: Tenants; id, first_name, last_name, image, contact, house_id, occupation, previous_residence, join_date, email
Table: Next_of_Kins; id, first_name, last_name, contact, tenant_id
Table: Payments; id, month, date_paid, tenant_id, amount, balance  

Feel free to update accordingly
