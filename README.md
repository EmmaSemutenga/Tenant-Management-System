# Tenant-Management-System
System to manage tenants
Owner or landloard will manage the system

As the owner:
0-Should be able to register
1-Should be able to login
2-Should be able to add, delete, update,  houses information
3-Should be able to add other and remove users(Fellow Admins)
4-Should be able to add, remove and update tenants (to free house)
5-Should be able to add payments
6-Should be able to search for tenants
7-Should be able to print payment, tenant details
8-Should be able to export details to csv

Database: Rental
Table: Owners; id(serial), name(varchar), username(varchar), password(varchar)
Table: Houses; id(serial), house_no(varchar), type_of_house(varchar), location(varchar), rent_amount(integer), status(interger)(availability)
Table: Tenants; id(serial), first_name(varchar), last_name(varchar), image(varchar), contact(varchar), house_id(integer), occupation(varchar), previous_residence(varchar), join_date(timestamp), email(varchar)
Table: Next_of_Kins; id(serial), first_name(varchar), last_name(varchar), contact(varchar), tenant_id(integer)
Table: Payments; id(serial), month(varchar), date_paid(timestamp), tenant_id(integer), amount(integer), balance(integer)  

Feel free to update accordingly
