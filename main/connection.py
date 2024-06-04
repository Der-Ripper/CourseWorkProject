import psycopg2

conn = psycopg2.connect(dbname="CourseWork", user="postgres", password="!tim-SQL#", host="127.0.0.1", port="5432")
conn.autocommit = True
cursor = conn.cursor()


def select(table_name):
    cursor.execute(f'SELECT * FROM public."{table_name}"')
    print(cursor.fetchall())


def insert_department(department_id, address, employees_count):
    cursor.execute(f'INSERT INTO public."Department"('
                   f'department_id, address, employees_count)'
                   f'VALUES ({str(department_id)}, \'{address}\', {str(employees_count)});')


def aaa():
    print("Подключение установлено")
    select('Department')
    #insert_department(5, 'Ufa', 15)
    select('Department')


    cursor.close()
    print(cursor.closed)
    conn.close()
