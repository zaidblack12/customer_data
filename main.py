from fastapi import FastAPI
import mysql.connector                                         #mysql connection module
import json
import time


app = FastAPI()
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="zaid1234",
        database="bank"
    )
mycursor = mydb.cursor()


class create_dict(dict):

    # __init__ function
    def __init__(self):
        self = dict()

        # Function to add key:value

    def add(self, key, value):
        self[key] = value

@app.get("/")
def read_root():
    mycursor.execute("SELECT * FROM CUSTOMERS LIMIT 100;")
    df = mycursor.fetchall()
    mydict = create_dict()
    for row in df:
        mydict.add(row[0],({"Customer_id": row[0], "transaction_amount": row[1], "Mobile_no": row[2], "Pincode": row[4]}))
    stud_json = json.dumps(mydict, indent=2, sort_keys=True)
    response_json = json.loads(stud_json)
    return response_json

@app.post("/insert_data/")
def insert_data(id: int=0, amount: int=0, mobileno: int=0, pincode: int=0):
    current_datetime = time.strftime('%Y-%m-%d %H:%M:%S')
    mycursor = mydb.cursor()
    sql = "INSERT INTO customers (Customer_id, transaction_amount, Mobile_no, transaction_datetime, Pincode) VALUES (%s, %s, %s, %s, %s)"
    val = (id,amount,mobileno,current_datetime,pincode)
    mycursor.execute(sql,val)
    mydb.commit()
    return "data created"


@app.get("/transaction_range/")
def filter_data_based_transaction_range(start: int=0, end: int=0):
    mycursor = mydb.cursor()
    sql = "select Customer_id, Mobile_no, sum(transaction_amount) as Total_Amt from customers where transaction_amount between %s and %s\
          group by Mobile_no\
          order by Total_Amt desc;"
    val = (start,end)
    mydict = create_dict()
    mycursor.execute(sql, val)
    df = mycursor.fetchall()
    for row in df:
        mydict.add(row[0],({"Customer_id": row[0],"Mobile_no": row[1], "Total_Amt": row[2]}))
    stud_json = json.dumps(mydict, indent=2, sort_keys=True)
    response_json = json.loads(stud_json)
    return response_json

@app.get("/top_customers_per_pincode/")
def top_customers_per_pincode(state: str=''):
    mycursor = mydb.cursor()
    sql = "Select distinct  c.Customer_id, c.Mobile_no, c.Pincode from ( Select c.Customer_id, c.Mobile_no, c.transaction_amount, c.Pincode, @pincode_rank := IF(@current_pincode =  c.Pincode, @pincode_rank + 1, 1) AS pincode_rank,  @current_pincode:=  c.Pincode FROM Customers as c ORDER BY  c.Pincode,  c.transaction_amount desc ) c LEFT JOIN  pincode_master as p ON c.pincode = p.pincode where pincode_rank<=5 and p.statename = %s ;"
    val = (state)
    mydict = create_dict()
    mycursor.execute(sql,(val,))
    df = mycursor.fetchall()
    for row in df:
        mydict.add(row[0], ({"Customer_id": row[0], "Mobile_no": row[1], "Pincode": row[2]}))
    stud_json = json.dumps(mydict, indent=2, sort_keys=True)
    response_json = json.loads(stud_json)
    return response_json


