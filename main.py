from fastapi import FastAPI
import mysql.connector                                         #mysql connection module
import json
import time
from helper_class import create_dict


app = FastAPI()
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=" ",
        database="bank"
    )


@app.get("/")
def read_root(limit: int=100):
    mycursor = mydb.cursor()
    sql = "Select * from Customers limit %s;"
    val = (limit)
    mycursor.execute(sql, (val,))
    df = mycursor.fetchall()
    response_json = add_keys_to_json(df)
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
def filter_data_based_transaction_range(start: int=0, end: int=0, limit: int=100):
    mycursor = mydb.cursor()
    sql = "select Customer_id, Mobile_no, sum(transaction_amount) as Total_Amt from customers where transaction_amount between %s and %s\
          group by Mobile_no\
          order by Total_Amt desc limit %s;"
    val = (start,end, limit)
    mycursor.execute(sql, val)
    df = mycursor.fetchall()
    response_json = add_keys_to_json(df)
    return response_json

@app.get("/top_customers_per_pincode/")
def top_customers_per_pincode(state: str=''):
    mycursor = mydb.cursor()
    sql = "Select distinct  c.Customer_id, c.Mobile_no, c.Pincode from ( Select c.Customer_id, c.Mobile_no, c.transaction_amount, c.Pincode, @pincode_rank := IF(@current_pincode =  c.Pincode, @pincode_rank + 1, 1) AS pincode_rank,  @current_pincode:=  c.Pincode FROM Customers as c ORDER BY  c.Pincode,  c.transaction_amount desc ) c LEFT JOIN  pincode_master as p ON c.pincode = p.pincode where pincode_rank<=5 and p.statename = %s ;"
    val = (state)
    mycursor.execute(sql,(val,))
    df = mycursor.fetchall()
    response_json = add_keys_to_json(df)
    return response_json


def add_keys_to_json(data):
    dict=create_dict()
    for row in data:
        dict.add(row[0], ({"Customer_id": row[0], "Mobile_no": row[1], "Pincode": row[2]}))
    stud_json = json.dumps(dict, indent=2, sort_keys=True)
    response_json = json.loads(stud_json)
    return response_json


