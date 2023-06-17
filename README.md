Topic: Property Investment
Description
This application is a channel through which property developers are able to connect with investors who are interested in investing in properties on an individual level. 
We adopt the idea of crowdfunding, but instead, having properties as the ‘project’, allowing individuals to participate in the investing of properties on a personal level with lower hurdles. 
Since developing a property from scratch requires huge amounts of capital, investing in property development has always been done by companies or individuals who are able to afford millions in investing. Instead, this app would allow people to partake in the property investment at a small cost.


Design and Functionalities 
Users and companies are required to create an account and log in. 
Companies can add their preferred properties, update their properties, delete their properties or change the status of their properties as fully invested.
Users are able to browse the list of available properties for investment and decide how much they wish to invest in it. They can also view the properties they have already invested in, as well as the current status of the investment.
The system is able to display the top invested properties such that users can make better-informed decisions on their investments. For each property listing, it would also display the percentage of the funded amount from the goal and show the status as ‘Fully Funded’ when the goal amount has been reached. The system also ensures that no financial transactions take place once the status is fully funded.


Data
We plan to generate our data using www.mockaroo.com with the following attributes for each entity:
Company: company_id, company_password

Property: property_id, location, size, price, company_id

User: first_name, last_name, dob, ic_number  

Transactions: transaction_id, company_id, ic_number, property_id, amount

Status: company_id, property_id, property_price, invested_amount, status


The company entity will store all the names of the companies that are in this property development market. Each company will have a unique numerical Id known as  company_id which will be used as a primary key for this entity. 

The property entity will be used to store the location, size and price of the property. The entity will also include the name of the company that is working on the development of the property. Furthermore, there is a status attribute which will show the percentage that has been invested in the property. Once the project price is equal to the amount of money invested it will show fully funded. Once the property is fully funded, the system will no longer accept fund transactions for this property. Every property has a unique property Id which will be used as a primary key for the entity. The property entity references the company entity with company_id as the foreign key. 

User entity represents all the investors who are willing to invest in the development of the property. The following attributes first_name, Last_name, date of birth and IC_number are used to store information of each investor. IC_number is unique for each investor so it is being used as a primary key for the entity 

Transaction entity keeps track of all the transactions taking place using this app. Each transaction is allocated an unique transaction_id which is used as the primary key and the amount for each transaction is recorded under the amount attribute. The entity links with the user and company entities using ic_number and company_id as their foreign keys respectively. 


Link to the website 
http://54.255.148.131:5000/



Uploading it2002 Project Group 3 video.mp4…


