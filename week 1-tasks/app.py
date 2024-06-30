from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'myDatabase'

mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

cursor = mysql.cursor()

@app.route('/')
def index():
    msg = ''
    cursor.execute('SELECT quote FROM quotes ORDER BY RAND() LIMIT 1')
    data = cursor.fetchone()
    return render_template('index.html', msg=msg, data=data)

@app.route('/add_entries', methods=['GET', 'POST'])
def addQuote():
  msg = ''
  cursor.execute('SELECT quote FROM quotes ORDER BY RAND() LIMIT 1')
  data = cursor.fetchone()
  if request.method == 'POST' and 'quote' in request.form:
    quote = request.form['quote']
    cursor.execute('SELECT * FROM quotes WHERE quote = %s', (quote,))
    check = cursor.fetchone()
    if check:
      msg = '✖ Quote already exists!'
    elif not quote:
      msg = '✖ Please enter a quote!'
    else:
      cursor.execute('INSERT INTO quotes VALUES (NULL, %s)', (quote,))
      mysql.commit()
      msg = '✔ Quote added successfully!'
      return render_template('index.html', msg=msg, data=data)
  elif request.method == 'POST':
      msg = '✖ Please fill out input box!'
  return render_template('index.html', msg=msg, data=data)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def updateQuote(id):
  if request.method == 'GET':
    cursor.execute('SELECT * FROM quotes WHERE id = %s', (id,))
    data = cursor.fetchone()
    return render_template('edit.html', data=data)
  elif request.method == 'POST':
    quote = request.form['quote']
    cursor.execute('UPDATE quotes SET quote = %s WHERE id = %s', (quote, id))
    mysql.commit()
    return redirect(url_for('index'))

@app.route('/listofquotes')
def listofquotes():
  cursor.execute('SELECT * FROM quotes')
  data = cursor.fetchall()
  return render_template('listofquotes.html', data=data)

@app.route('/delete_entries', methods=['POST'])
def deleteQuote():
  msg = ''
  prefix = request.form['delete-quote']
  prefix_with_wildcard = f'{prefix}%'
  cursor.execute('DELETE FROM quotes WHERE quote LIKE %s', (prefix_with_wildcard,))
  mysql.commit()
  cursor.execute('SELECT quote FROM quotes ORDER BY RAND() LIMIT 1')
  data = cursor.fetchone()
  return render_template('index.html', msg=msg, data=data)