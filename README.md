# customer_data

# **Getting Started**

This API is tested with Python 3.9.13
 
 
**Setup**

Please follow the below steps to setup the api in your local environment.

Prerequisite:
* Python 3.9.13
* MySQL server 8.0.31
* MySQL workbench 8.0.31
 
**Steps for MySQL installation :**

* Download the MySQL installer from this link, here we can install MySQL server and Workbench. https://dev.mysql.com/downloads/installer/

* Setup the local Database in the installation process and make sure to capture the hostname = localhost, username and password. 
Steps for Database setup:
Create the Database from the below query and run on the Workbench.

`CREATE DATABASE Bank;`

 
* Create Customers Table from the below query.

`CREATE TABLE customers (
    Customer_id int,
    transaction_amount float,
    Mobile_no varchar(255),
    transaction_datetime DATETIME,
    Pincode int
);`

 
* Create the State Table from the query.

`CREATE TABLE state_master (
    officename varchar(50),
    pincode int,
    statename varchar(50)
);`

 
**Importing the dummy data:**
* Download the MOCK_DATA.csv and import in the Customers Table refer the below screenshot, you can create your own dummy data from the below link.
https://www.mockaroo.com/

* Download the state_master and import in the state_master Table refer the above screenshot, you can download the data from the below link.
https://data.gov.in/sites/default/files/all_india_pin_code.csv
 
**Steps for the Project setup:**
Before preceding this ensure that you’ve followed the above steps.

**Step 1
Installation from source (requires git):**

`$ git clone https://github.com/zaidblack12/customer_data.git`

`$ cd customer_data`

**Step 2
Install the necessary module with below command**

`$ pip install -r requirements.txt`
 
**Step 3
Start the server to bring up the api service.**

`$ uvicorn main:app —reload`

**Step 4 Install the postman for using the post api while inserting the data**

https://www.postman.com/downloads/


# **API Endpoints**
 
<table>
<tr>
    <th>URL</th>
    <th>Http method</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>‘/’</td>
    <td>get</td>
    <td>Get all the customer data
Limit can be added to restrict the data to any number. Eg ‘/?limit=50’ will return 50 records. Default limit is 100 if limit query is not passed
</td>
  </tr>
  <tr>
    <td>‘/transaction_range/?start=2000&end=5000’</td>
    <td>get</td>
    <td>Get all the customer data whose total transaction amount is between param start and end, this month, or this year or all time.
Limit can be added to restrict the data, Default limit is 100 
</td>
<tr>
    <td>/top_customers_per_pincode/?state=PUNJAB</td>
    <td>get</td>
    <td>Get Top 5 customer data per pincode for all the pincode in the state.
Filter the customer data by any ‘state’ name</td>
  </tr>
<tr>
    <td>/insert_data/?id=75&amount=224&mobileno=8976437363&pincode=241434</td>
    <td>post</td>
    <td>Insert customer data in database within param is ‘id’,’amount’,’mobileno’,’pincode’.
Date time data is auto set ar current date and time, 
(yyyy-mm-dd hh:mm:ss), and kindly put all the parameter in the postman while using this POST API</td>
    
  </tr>
  </tr>
    </tr>
</table>
