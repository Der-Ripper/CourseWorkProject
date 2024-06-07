import psycopg2
from psycopg2.extras import Json
from psycopg2.extensions import register_adapter
from conf import DB_NAME, DB_USER, DB_PASSWORD
import json
from uuid import uuid4

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


def select_all_client_claims_0(login):
    print('Client-Claim-LOGIN:', login)
        # Удаление временной таблицы, если она существует
    cursor.execute("DROP TABLE IF EXISTS temp_claim_data;")
    cursor.execute("""
        CREATE TEMP TABLE temp_claim_data (
            full_name VARCHAR(50),
            age VARCHAR(3),
            address_living JSON,
            address_registrations JSON,
            email VARCHAR(25),
            phone_number VARCHAR(11),
            INN VARCHAR(12),
            Passport VARCHAR(11),
            title VARCHAR(50),
            description JSON,
            status VARCHAR(20),
            claim_number VARCHAR(20),
            name VARCHAR(50)
        );
    """)
    print('Temporary table created.')

    # Вызов функции и вставка данных во временную таблицу
    query = """
    INSERT INTO temp_claim_data (full_name, age, address_living, address_registrations, email, phone_number, INN, Passport, title, description, status, claim_number, name)
    SELECT * FROM get_claim_data_phys_web(%s);
    """
    cursor.execute(query, (login,))
    conn.commit()  # Зафиксировать изменения
    print('Function called and data inserted into temp table.')

    # Извлечение данных из временной таблицы
    cursor.execute("SELECT * FROM temp_claim_data")
    claims = cursor.fetchall()
    print('CLAIMS:', claims)
    return claims

def select_all_client_claims_2(login):
    print('Client-Claim-LOGIN:', login)

    # Удаление временной таблицы, если она существует
    cursor.execute("DROP TABLE IF EXISTS temp_claim_data;")
    print('CREATE TABLE:', cursor.execute("""
        CREATE TEMP TABLE temp_claim_data (
            full_name VARCHAR(50),
            age VARCHAR(3),
            address_living JSON,
            address_registrations JSON,
            email VARCHAR(25),
            phone_number VARCHAR(11),
            INN VARCHAR(12),
            Passport VARCHAR(11),
            title VARCHAR(50),
            description JSON,
            status VARCHAR(20),
            claim_number VARCHAR(20),
            name VARCHAR(50)
        );
    """))

    # Вызов функции и вставка данных во временную таблицу
    query = """
    INSERT INTO temp_claim_data (full_name, age, address_living, address_registrations, email, phone_number, INN, Passport, title, description, status, claim_number, name)
    SELECT * FROM get_claim_data_phys(%s);
    """
    print('CALL FUNC:', cursor.execute(query, (login,)))

    # Извлечение данных из временной таблицы
    cursor.execute("SELECT * FROM temp_claim_data")
    claims = cursor.fetchall()
    print('CLAIMS:', claims)
    return claims

def select_all_branch_claims():
    #cursor.execute('SELECT * FROM public.claim ORDER BY claim_id ASC')
    #claims = cursor.fetchall()
    #print(claims)
    
    cursor.execute('SELECT claim_number FROM public.claim')
    claims_numbers = cursor.fetchall()
    print(claims_numbers)
    branch_claims = []
    for claim_number in claims_numbers:
        cursor.execute("DROP TABLE IF EXISTS temp_claim_data1;")
        cursor.execute("""
        CREATE TEMP TABLE temp_claim_data1 (
            case_number VARCHAR(20),
            claim_status VARCHAR(20),
            name VARCHAR(50)
            );
        """)

        query = """
DO $$   
DECLARE   
    v_case_number VARCHAR(20); 
    v_claim_status VARCHAR(20); 
    v_name VARCHAR(50); 
BEGIN   
    -- Вызов процедуры и получение выходных параметров   
    CALL get_branch_data( 
        %s, 
        v_case_number, 
        v_claim_status, 
        v_name 
    ); 

    -- Проверка, существует ли значение для номера дела и отдела
    IF v_case_number IS NOT NULL AND v_name IS NOT NULL THEN
        -- Вставка данных во временную таблицу   
        INSERT INTO temp_claim_data1 (case_number, claim_status, name)    
        VALUES (
            v_case_number, 
            v_claim_status, 
            v_name 
        );
    ELSE
        -- Вставка данных с NULL значением для номера дела и/или отдела, 
        -- или другим значением по умолчанию
        INSERT INTO temp_claim_data1 (case_number, claim_status, name)    
        VALUES (
            COALESCE(v_case_number, 'Unknown'), 
            v_claim_status, 
            COALESCE(v_name, 'Unknown')
        );
    END IF;
END $$;

SELECT * FROM temp_claim_data1;
        """
        #cursor.execute(query, (claim[1],))
        cursor.execute(query, (claim_number,))
        result = cursor.fetchone()
        print(result)
        #if result[0] is not None and result[1] is not None and result[2] is not None:
        #    branch_claims.append(result)
        branch_claims.append(result)
    return branch_claims

def select_all_client_claims(login):
    print('Client-Claim-LOGIN:', login)

    cursor.execute("DROP TABLE IF EXISTS temp_claim_data;")
    print('\nCREATE TABLE:\n', cursor.execute("""
        CREATE TEMP TABLE temp_claim_data (
            --full_name VARCHAR(50),
            --age VARCHAR(3),
            full_name VARCHAR(50),
            age VARCHAR(3),
            address_living JSON,
            address_registrations JSON,
            email VARCHAR(25),
            phone_number VARCHAR(11),
            INN VARCHAR(12),
            Passport VARCHAR(11),
            title VARCHAR(50),
            description JSON,
            status VARCHAR(20),
            claim_number VARCHAR(20),
            name VARCHAR(50)
        );
    """))

    query = """
    DO $$  
    DECLARE  
        v_full_name VARCHAR(50);  
        v_age VARCHAR(3); 
        v_address_living JSON;
        v_address_registrations JSON;
        v_email VARCHAR(25);
        v_phone_number VARCHAR(11);
    v_INN VARCHAR(12);
       v_Passport VARCHAR(11);
      v_title VARCHAR(50);
       v_description JSON;
       v_claim_status VARCHAR(20);
       v_claim_number VARCHAR(20);
    v_name VARCHAR(50);
    BEGIN  
        -- Вызов процедуры и получение выходных параметров  
        CALL get_claim_data_phys(
            %s, 
            v_full_name, 
            v_age,
            v_address_living,
            v_address_registrations,
            v_email,
            v_phone_number,
      v_INN,
         v_Passport,
        v_title,
         v_description,
         v_claim_status,
         v_claim_number,
      v_name
        );
  
        -- Вставка данных во временную таблицу  
        INSERT INTO temp_claim_data (full_name, age, address_living, address_registrations, email, phone_number, INN, Passport, title, description, status, claim_number, name)   
        VALUES (v_full_name, 
        v_age, 
        v_address_living,
        v_address_registrations,
        v_email,
        v_phone_number,
        v_INN,
        v_Passport,
        v_title,
           v_description,
           v_claim_status,
           v_claim_number,
           v_name
         );  
    END $$;
    """
    print('\nCALL PROC:\n', cursor.execute(query, (login,)))
    print('\nFROM TEMP:\n', cursor.execute("SELECT * FROM temp_claim_data"))
    claims = cursor.fetchall()
    print('\nCLAIMS:\n', claims)
    return claims


def select_branch_claims(login):
    print('Client-Claim-LOGIN:', login)
    query = "CALL get_claim_data_phys(%s); COMMIT;"
    print(cursor.execute(query, (login,)))
    claims = cursor.fetchall()
    print(claims)

def auth_via_db(login, password):
    print('LOGIN:', login)
    print('PASSWORD:', password)
    query = 'SELECT * FROM public."employee" WHERE login=%s AND password=%s'
    cursor.execute(query, (login, password))
    user = cursor.fetchone()
    if user:
        print('\n\nUSSSSER\n\n')
        return user
    query = 'SELECT * FROM public."client" WHERE login=%s AND password=%s'
    cursor.execute(query, (login, password))
    user = cursor.fetchone()
    print(user)
    if user:
        return user
    return None

def registration_client(login, password, pory):
    query = "CALL registration_client(%s, %s, %s); COMMIT; SELECT * FROM public.client ORDER BY client_id ASC"
    print(query)
    print(cursor.execute(query, (login, password, pory)))
    result = cursor.fetchall()
    print(result)
    if result:
        return True
    else:
        return False


def registration_client_yur(name, age, living_address, registration_address, email, phone, inn, ogrn, kpp, okved, title, description, login):
    la = json.dumps(living_address)
    ra = json.dumps(registration_address)
    desc = json.dumps(description)
    query = "CALL registration_client_yur(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); COMMIT; SELECT * FROM public.client ORDER BY client_id ASC"
    print(query)
    print(cursor.execute(query, (name, age, la, ra, email, phone, inn, ogrn, kpp, okved, title, desc, login)))
    result = cursor.fetchall()
    print(result)
    if result:
        return True
    else:
        return False

def test_procedure(name, age, living_address, registration_address, email, phone, inn, passport, title, description, login):
    la = json.dumps(living_address)
    ra = json.dumps(registration_address)
    desc = json.dumps(description)
    query = "CALL registration_client_phys(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); COMMIT; SELECT * FROM public.client ORDER BY client_id ASC"
    print(query)
    cursor.execute(query, (name, age, la, ra, email, phone, inn, passport, title, desc, login))
    result = cursor.fetchall()
    print(result)
    if result:
        return True
    else:
        return False

def select_user_last_claim():
    query = ''

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
