from flask_cors import CORS, cross_origin
# ? Python's built-in library for JSON operations. Here, is used to convert JSON strings into Python dictionaries and vice-versa
import json
import psycopg2
# ? flask - library used to write REST API endpoints (functions in simple words) to communicate with the client (view) application's interactions
# ? request - is the default object used in the flask endpoints to get data from the requests
# ? Response - is the default HTTP Response object, defining the format of the returned data by this api
from flask import Flask, request, Response, make_response, redirect, url_for, render_template, session,jsonify
# ? sqlalchemy is the main library we'll use here to interact with PostgresQL DBMS
import sqlalchemy
# ? Just a class to help while coding by suggesting methods etc. Can be totally removed if wanted, no change
from typing import Dict
from datetime import date
from decimal import Decimal

# ? web-based applications written in flask are simply called apps are initialized in this format from the Flask base class. You may see the contents of `__name__` by hovering on it while debugging if you're curious
app = Flask(__name__)
app.secret_key = 'some_secret_key'  # set a secret key for session encryption
app.config['DEBUG'] = True
CORS(app)

# ? building our `engine` object from a custom configuration string
# ? for this project, we'll use the default postgres user, on a database called `postgres` deployed on the same machine
YOUR_POSTGRES_PASSWORD = "postgres"
connection_string = f"postgresql://postgres:{YOUR_POSTGRES_PASSWORD}@localhost/postgres"
engine = sqlalchemy.create_engine(
    "postgresql://postgres:postgres@localhost/postgres"
)


# ? A dictionary containing
data_types = {
    'boolean': 'BOOL',
    'integer': 'INT',
    'text': 'TEXT',
    'time': 'TIME',
}

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/company_login/')
def company_login():
    return render_template('company_login.html')

@app.route('/company_register/')
def company_register():
    return render_template('company_register.html')

@app.route('/admin_login/')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin_property_access/')
def admin_property():
    return render_template('company_listings.html')

@app.route('/admin_company_access/')
def admin_company():
    return render_template('company_register.html')

@app.route('/admin_users_access/')
def admin_users():
    return render_template('userreg.html')

@app.route('/company_add_account/', methods = ["post", "get"])
def company_add_account():
    company_id = request.form['company_id']
    password = request.form['password']
    try:
        db = engine.connect()
        statement = sqlalchemy.text(f"INSERT INTO company VALUES ('{company_id}', '{password}');")
        db.execute(statement)
        db.commit()
        db.close()
        return company_login()
        
    except sqlalchemy.exc.IntegrityError:        
        return render_template('company_register_repeat.html')
    
@app.route('/company_add_listing/', methods = ["post", "get"])
def add_property():
    property_id = request.form['property_id']
    location = request.form['location']
    size = request.form['size']
    price = request.form['price']
    company_id = request.form['company_id']
    listings = request.form['listings']
    
    try:
        db = engine.connect()
        query = sqlalchemy.text(f"INSERT INTO property VALUES ('{property_id}', '{location}', '{size}', '{price}', '{company_id}');")
        db.execute(query)
        db.commit()
        db.close()
        db = engine.connect()
        statement = sqlalchemy.text(f"SELECT p.property_id, p.location, p.size, p.price FROM property p, company c WHERE p.company_id = c.company_id AND c.company_id = '{company_id}';")
        listings = db.execute(statement)
        db.close()
        return render_template('company_listings.html', company_id=company_id, listings=listings)
    
    except sqlalchemy.exc.IntegrityError: 
        db = engine.connect()
        statement = sqlalchemy.text(f"SELECT p.property_id, p.location, p.size, p.price FROM property p, company c WHERE p.company_id = c.company_id AND c.company_id = '{company_id}';")
        listings = db.execute(statement)
        db.close()
        return render_template('company_listings.html', company_id=company_id, listings=listings)


@app.route('/company_access/', methods = ["post", "get"])
def company_listings():
    company_id = request.form['company_id']
    password = request.form['password']
    try:
        db = engine.connect()
        statement = sqlalchemy.text(f"SELECT * FROM company WHERE company_id ='{company_id}' AND password ='{password}';")
        result = db.execute(statement)
        user = result.fetchone()
        db.close()

        if user is not None:
            db = engine.connect()
            statement = sqlalchemy.text(f"SELECT p.property_id, p.location, p.size, p.price FROM property p, company c WHERE p.company_id = c.company_id AND c.company_id = '{company_id}';")
            listings = db.execute(statement)
            db.close()
            return render_template('company_listings.html', company_id=company_id, listings=listings)
        
        else:
            return render_template('company_login_invalid.html')

    except:
        return company_login()
    
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['userid']
        password = request.form['password']
        
        # Check if the username and password are correct
        if username == 'Admin' and password == 'group3':
            return render_template('admin_page.html')
        else:
            return render_template('admin_login_invalid.html')
    
    return render_template('admin_login.html')


"""
schema to store users informations
Create table users(
first_name varchar(20) not null,
last_name varchar(20) not null,
dob date not null,
ic_number varchar(20) not null,
password varchar(20) not null,
primary key(ic_number)
);

schema to store transaction information 
Create table transactions(
    transaction_id int not null,
    company_id varchar(64) not null,
    ic_number varchar(20) not null,
    property_id varchar(64) not null,
    amount int not null,
    primary key (transaction_id),
    foreign key (company_id) references company(company_id),
    foreign key (property_id) references property(property_id),
    foreign key (ic_number) references users(ic_number)
)
;
"""



@app.route('/userreg/', methods=['GET', 'POST'])
def userreg():
    if request.method == 'GET':
        return render_template('userreg.html')
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        ic_number = request.form['ic_number']
        password = request.form['password']
        try:
            db = engine.connect()
            query = sqlalchemy.text(f'INSERT INTO users VALUES (\'{first_name}\', \'{last_name}\', \'{dob}\', \'{ic_number}\', \'{password}\');')
            db.execute(query)
            db.commit()
            return render_template('userlogin.html')
        except sqlalchemy.exc.IntegrityError: 
            return render_template('userreg.html')



@app.route('/userlogin/', methods=['GET', 'POST'])
def userlogin():
    x = None
    if request.method == 'GET':
        return render_template('userlogin.html')
    else:
        ic_number = request.form['ic_number']
        password = request.form['password']
        name = request.form['first_name']

    # Check if the username and password are correct
        db = engine.connect()
        statement = sqlalchemy.text(f"SELECT * FROM users WHERE ic_number ='{ic_number}' AND password ='{password}';")
        result = db.execute(statement)
        user = result.fetchone()
        db.commit()
        db.close()

        if user is not None:
            x = 1
            session['ic_number'] = ic_number
            session['name'] = name
            return render_template('userin.html', name=user[0], x=x)

        else:
            x = 0
            return render_template('userlogin.html', x=x)


@app.route('/current/')
def current():
    ic_number = session.get('ic_number')
    print(ic_number)
    name = session.get('name')
    # get the following information from the property table and transaction table for the global ic_number and display them in current.html
    db = engine.connect()
    query = sqlalchemy.text("""
    SELECT p.property_id, p.location, p.size, p.price, p.company_id, 
    SUM(t.amount) AS total_investment,
    COALESCE(SUM(CASE WHEN t.ic_number = :ic_number THEN t.amount ELSE 0 END), 0) AS user_investment,
    ROUND((SUM(t.amount) / p.price) * 100, 2) AS investment_percent
    FROM property p
    LEFT JOIN transactions t ON p.property_id = t.property_id
    GROUP BY p.property_id
    HAVING COALESCE(SUM(CASE WHEN t.ic_number = :ic_number THEN t.amount ELSE 0 END), 0) > 0

    """)
    results = db.execute(query, {'ic_number' : ic_number})
    db.commit()
    db.close()
    return render_template('current.html', results=results, name=name)


@app.route('/invest/')
def invest():
    ic_number = session.get('ic_number')
    name = session.get('name')
    #a sql query to get property_id, location, size, price, company_id from property table and sum of amount on that property from transaction table and status = sum(amount)/price * 100  less than 100 and display them in invest.html
    query = sqlalchemy.text("""
    SELECT p.property_id, p.location, p.size, p.price, c.company_id, 
    SUM(t.amount) as amount, 
    ROUND(SUM(t.amount)/p.price * 100, 2) as status
    FROM property p, transactions t, company c
    WHERE p.property_id = t.property_id
	AND p.company_id = c.company_id
    AND p.property_id NOT IN (
        SELECT DISTINCT(p.property_id)
        FROM property p, transactions t
        WHERE p.property_id = t.property_id
        AND t.ic_number = :ic_number)
    GROUP BY p.property_id, p.location, p.size, p.price, c.company_id
    HAVING ROUND(sum(t.amount)/p.price * 100, 2) < 100;
    """)
    db = engine.connect()
    results = db.execute(query, {'ic_number' : ic_number}) 
    db.commit()
    db.close()
    return render_template('invest.html', results=results, name=name)

@app.route('/successful/')
def successful():
    ic_number = session.get('ic_number')
    name = session.get('name')
    #reveives the amount the user wants to invest and the property_id from the invest.html
    amount = request.args.get('amount')
    company_id = request.args.get('companyID')
    property_id = request.args.get('propertyID')
    #transaction_id is equal to the very last transaction id in the transaction table + 1

    # get the property_id from the invest.html for which the user wants to invest and insert the following information into the transaction table including the amount the user wants to invest
    # and display the following information in successful.html
    db = engine.connect()
    query = sqlalchemy.text(f"INSERT INTO transactions VALUES (:transaction_id, :ic_number, :property_id, :amount)")
    querz = sqlalchemy.text("""
    SELECT transaction_id
    FROM transactions
    ORDER BY transaction_id DESC
    LIMIT 1
    """)
    transaction_id = db.execute(querz).fetchone()[0] + 1 
    results = db.execute(query, {"transaction_id":transaction_id, "ic_number":ic_number, "property_id":property_id, "amount":amount})
    db.commit()
    db.close()
    return render_template('successful.html', results=results)


def generate_table_return_result(res):
    rows = []
    columns = list(res.keys())
    for row_number, row in enumerate(res):
        rows.append({})
        for column_number, value in enumerate(row):
            if isinstance(value,date):
                formatted_value=value.strftime('%Y-%m-%d');
                rows[row_number][columns[column_number]] = formatted_value;
            elif isinstance(value,Decimal):
                my_decimal_str = str(value)
                json_data = json.dumps(my_decimal_str)
                rows[row_number][columns[column_number]] = json_data
            else:
                rows[row_number][columns[column_number]] = value
            

    # ? JSON object with the relation data
    output = {}
    output["columns"] = columns  # ? Stores the fields
    output["rows"] = rows  # ? Stores the tuples
    
    return json.dumps(output)

@app.route('/company_list/')
def Company_list():
    relation_name = request.args.get('name', default="", type=str)
    db = engine.connect()
    try:
        statement = sqlalchemy.text(f"SELECT * FROM company;")
        results = db.execute(statement)
        db.close()
        return render_template('company_info.html',results=results)
    except Exception as e:
        db.rollback()
        return Response(str(e), 403)
    
@app.route('/transaction_list/')
def Transaction_list():
    relation_name = request.args.get('name', default="", type=str)
    db = engine.connect()
    try:
        statement = sqlalchemy.text(f"SELECT * FROM transactions;")
        results = db.execute(statement)
        db.close()
        return render_template('transaction_info.html',results=results)
    except Exception as e:
        db.rollback()
        return Response(str(e), 403)
    
@app.route('/user_list/')
def User_list():
    relation_name = request.args.get('name', default="", type=str)
    db = engine.connect()
    try:
        statement = sqlalchemy.text(f"SELECT * FROM users;")
        results = db.execute(statement)
        db.close()
        return render_template('user_info.html',results=results)
    except Exception as e:
        db.rollback()
        return Response(str(e), 403)

@app.route('/property_list/')
def Property_list():
    relation_name = request.args.get('name', default="", type=str)
    db = engine.connect()
    try:
        statement = sqlalchemy.text(f"SELECT * FROM property;")
        results = db.execute(statement)
        db.close()
        return render_template('property_info.html',results=results)
    except Exception as e:
        db.rollback()
        return Response(str(e), 403)


@app.route('/delete_company_listing/', methods = ["post", "get"])
def delete_company_listing():
    company_id = request.form['company_id']
    password = request.form['password']
    db = engine.connect()
    query = sqlalchemy.text(f"DELETE FROM company WHERE company_id ='{company_id}' AND password ='{password}';")
    db.execute(query)
    db.commit()
    db.close()
    db = engine.connect()
    statement = sqlalchemy.text(f"SELECT * FROM company;")
    results = db.execute(statement)
    db.close()
    return render_template('company_info.html', results=results)
        
@app.route('/add_company/',methods = ["post", "get"])
def add_company():
    company_id = request.args.get('company_id')
    password = request.args.get('password')
    db = engine.connect()
    query = sqlalchemy.text(f"INSERT INTO company VALUES ('{company_id}','{password}')")
    results = db.execute(query)
    db.commit()
    db.close()
    db = engine.connect()
    statement = sqlalchemy.text(f"SELECT * FROM company;")
    results = db.execute(statement)
    db.close()
    return render_template('company_info.html', results=results)

@app.route('/delete_user_listing/', methods = ["post", "get"])
def delete_user_listing():
    ic_number = request.form['ic_number']
    db = engine.connect()
    query = sqlalchemy.text(f"DELETE FROM users WHERE ic_number ='{ic_number}';")
    db.execute(query)
    db.commit()
    db.close()
    db = engine.connect()
    statement = sqlalchemy.text(f"SELECT * FROM users;")
    results = db.execute(statement)
    db.close()
    return render_template('user_info.html', results=results)
        
@app.route('/add_user/',methods = ["post", "get"])
def add_user():
    first_name = request.args.get('first_name')
    last_name=request.args.get('last_name')
    dob=request.args.get('dob')
    ic_number=request.args.get('ic_number')
    password = request.args.get('password')
    db = engine.connect()
    query = sqlalchemy.text(f"INSERT INTO users VALUES ('{first_name}','{last_name}','{dob}','{ic_number}','{password}')")
    results = db.execute(query)
    db.commit()
    db.close()
    db = engine.connect()
    statement = sqlalchemy.text(f"SELECT * FROM users;")
    results = db.execute(statement)
    db.close()
    return render_template('user_info.html', results=results)  
  
@app.route('/delete_property_listing/', methods = ["post", "get"])
def delete_property_listing():
    property_id = request.form['property_id']
    db = engine.connect()
    query = sqlalchemy.text(f"DELETE FROM property WHERE property_id ='{property_id}';")
    db.execute(query)
    db.commit()
    db.close()
    db = engine.connect()
    statement = sqlalchemy.text(f"SELECT * FROM property;")
    results = db.execute(statement)
    db.close()
    return render_template('property_info.html', results=results)
        
@app.route('/add_property/',methods = ["post", "get"])
def admin_add_property():
    property_id = request.args.get('property_id')
    location=request.args.get('location')
    size=request.args.get('size')
    price=request.args.get('price')
    company_id = request.args.get('company_id')
    db = engine.connect()
    query = sqlalchemy.text(f"INSERT INTO property VALUES ('{property_id}','{location}','{size}','{price}','{company_id}')")
    results = db.execute(query)
    db.commit()
    db.close()
    db = engine.connect()
    statement = sqlalchemy.text(f"SELECT * FROM property;")
    results = db.execute(statement)
    db.close()
    return render_template('property_info.html', results=results)    

@app.route('/delete_transaction_listing/', methods = ["post", "get"])
def delete_transaction_listing():
    transaction_id = request.form['transaction_id']
    db = engine.connect()
    query = sqlalchemy.text(f"DELETE FROM transactions WHERE transaction_id ='{transaction_id}';")
    db.execute(query)
    db.commit()
    db.close()
    db = engine.connect()
    statement = sqlalchemy.text(f"SELECT * FROM transactions;")
    results = db.execute(statement)
    db.close()
    return render_template('transaction_info.html', results=results)
        
@app.route('/add_transaction/',methods = ["post", "get"])
def admin_add_transaction():
    transaction_id = request.args.get('transaction_id')
    ic_number=request.args.get('ic_number')
    amount=request.args.get('amount')
    property_id = request.args.get('property_id')
    db = engine.connect()
    query = sqlalchemy.text(f"INSERT INTO transactions VALUES ('{transaction_id}','{ic_number}','{property_id}','{amount}')")
    results = db.execute(query)
    db.commit()
    db.close()
    db = engine.connect()
    statement = sqlalchemy.text(f"SELECT * FROM transactions;")
    results = db.execute(statement)
    db.close()
    return render_template('transaction_info.html', results=results)    

if __name__ == "__main__":
    app.run("0.0.0.0", 5000)