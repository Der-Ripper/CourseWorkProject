import psycopg2
from psycopg2.extras import Json
from psycopg2.extensions import register_adapter
from conf import DB_NAME, DB_USER, DB_PASSWORD
import json

conn = psycopg2.connect(dbname=DB_NAME , user=DB_USER, password=DB_PASSWORD, host="127.0.0.1", port="5432")
conn.autocommit = True
cursor = conn.cursor()


def select(table_name):
    cursor.execute(f'SELECT * FROM public."{table_name}"')
    print(cursor.fetchall())

def client_auth(login, password):
    query = 'SELECT * FROM public."client" WHERE login=%s and password=%s'
    cursor.execute(query, (login, password))
    user = cursor.fetchone()
    print(user)
    if user:
        return user
    return None

def test_procedure(name, age, living_address, registration_address, email, phone, inn, passport, title, description):
    print(type(living_address), type(registration_address), type(description))
    #la = register_adapter(living_address, Json)
    #ra = register_adapter(registration_address, Json)
    #desc = register_adapter(description, Json)
    la = json.dumps(living_address)
    ra = json.dumps(registration_address)
    desc = json.dumps(description)
    args = [name, age, la, ra, email, phone, inn, passport, title, desc]
    print(args)

    result = cursor.callproc('registration_client_phys', args)
    print(result)

def insert_department(department_id, address, employees_count):
    cursor.execute(f'INSERT INTO public."Department"('
                   f'department_id, address, employees_count)'
                   f'VALUES ({str(department_id)}, \'{address}\', {str(employees_count)});')


def aaa():
    print("Подключение установлено")
    select('branch')
    #insert_department(5, 'Ufa', 15)
    select('Department')


    cursor.close()
    print(cursor.closed)
    conn.close()
