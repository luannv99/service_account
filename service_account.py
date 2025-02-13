import json
import bcrypt
import mysql.connector
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException
from typing import Optional

app = FastAPI()

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="14032016@",
    database="service_account"
)
class ACC(BaseModel): #
    phone: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

@app.post("/account/create")
def create_account(account: ACC):
    try:
        cursor = mydb.cursor(dictionary=True) # connect sql
        parse_data = account.dict()
        print(parse_data)
        if (parse_data.get("phone") is None or parse_data.get("phone") == "") or (parse_data.get("password") is None or parse_data.get("password") == "") or (parse_data.get("email") is None or parse_data.get("email") == ""):
            print("phone null")
            raise HTTPException(status_code=400, detail="missing param")
        mysql_query = "SELECT phone FROM users WHERE phone = %s"
        params_tupple = (parse_data.get("phone"),)
        cursor.execute(mysql_query, params_tupple)
        record = cursor.fetchone()
        if record is not None:
            raise HTTPException(status_code=400, detail="user existed in system")
        data_password = parse_data.get("password")
        print(data_password)
        password = str.encode(data_password) #chuyen string thanh byte
        hased = bcrypt.hashpw(password, bcrypt.gensalt())
        parse_hash = hased.decode() # #chuyen byte thanh string
        insert_db = "INSERT INTO users(phone,email,password) VALUES(%s, %s, %s)"
        val_db = (parse_data.get("phone"), parse_data.get("email"), parse_hash)
        cursor.execute(insert_db, val_db)
        mydb.commit()
        print(password, parse_hash)
    except Exception as exc:
        print(exc)
        raise exc
    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()
            print("MySQL mydb is closed")
    return {}



@app.post("/login/account")
async def login_account(acc: ACC):
    try:
        cursor = mydb.cursor(dictionary=True)
        parse_data = acc.dict()
        if (parse_data.get("phone") is None or parse_data.get("phone") == "") or (parse_data.get("password") is None or parse_data.get("password") == "") or (parse_data.get("email") is None or parse_data.get("email") == ""):
            print("username null")
            raise HTTPException(status_code=400, detail="missing param")
        # kiem tra user phone va password co ton tai trong he thong khong neu khong ghi ra "user hoac password khong dung"
        mysql_query = "SELECT phone, password FROM users WHERE phone = %s"
        params_tupple = (parse_data.get("phone"),)
        cursor.execute(mysql_query, params_tupple)
        record = cursor.fetchone()
        if record is None:
            raise HTTPException(status_code=400, detail="phone does not existed in system")
        password_client = parse_data.get("password")
        print(password_client)
        password = str.encode(password_client) #chuyen srt thanh byte
        password_db = str.encode(record.get("password"))
        if not (bcrypt.checkpw(password,password_db)):
            raise HTTPException(status_code=400, detail="wrong password")
        return {"login_account": "success"}
    except Exception as exc:
        print(exc)
        raise exc
    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()
            print("MySQL mydb is closed")
            
            
            
@app.post("/update/account")
async def update_account(account: ACC):
    try:
        cursor = mydb.cursor(dictionary = True)
        parse_data = account.dict()
        if (parse_data.get("phone") is None or parse_data.get("phone") == "") or (parse_data.get("email") is None or parse_data.get("email") == "") or (parse_data.get("password") is None or parse_data.get("password") == ""):
            raise HTTPException(status_code = 400, detail = "missing param")
        mysql_update_mail = "UPDATE service_account.users SET email = %s WHERE phone = %s"
        input_mail_update = parse_data.get('email')
        # print(input_mail_update)
        data_phone = parse_data.get('phone')
        # print(data_phone)
        val = (input_mail_update, data_phone)
        cursor.execute(mysql_update_mail, val)
        mydb.commit()
        # recod = cursor.fetchone()
        return{"update": "ok"}
    except Exception as exc:
        raise exc
    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()
            print("Mysql mydb is close")
            
            
            
@app.post("/delete/account")
async def delete_account(account : ACC):
    try:
        cursor = mydb.cursor(dictionary=True)
        parse_data = account.dict()
        if (parse_data.get("phone") is None or parse_data.get("phone") == "") or (parse_data.get("email") is None or parse_data.get("email") == "") or (parse_data.get("password") is None or parse_data.get("password") == ""):
            raise HTTPException(status_code = 400, detail = "missing param")
        mydb_delete_account = "DELETE FROM users WHERE phone = %s"
        data_phone = (parse_data.get('phone'),)
        cursor.execute(mydb_delete_account,data_phone)
        mydb.commit()
        return{"delete account" : "ok"}
    except Exception as exc:
        raise exc
    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()
            print("Mysql connect is close")
# committest
