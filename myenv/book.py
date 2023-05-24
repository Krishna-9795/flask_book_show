from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector

app=Flask(__name__)
app.secret_key = 'your_secret_key'
#configuring mysql
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root@123',
    database='bookmyshow')

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('movies'))
    else:
        return render_template('index.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        cursor = db.cursor()
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        values = (name, email, password)
        cursor.execute(query, values)
        db.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        values = (email, password)
        cursor.execute(query, values)
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('movies'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')
        
        
        


@app.route('/')
def homes():
    # Perform database operations
    if 'user_id' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()
        return render_template('movies.html', movies=movies)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))
if __name__=="__main__":
    app.run()
