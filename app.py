import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
# Excel file path
excel_file = 'users.xlsx'

# Initialize Excel file if not exists
try:
    df = pd.read_excel(excel_file, index_col=0)
except FileNotFoundError:
    df = pd.DataFrame(columns=['username', 'password'])
    df.to_excel(excel_file)

def save_new_user(username, password):
    global df
    hashed_password = generate_password_hash(password)
    new_user_df = pd.DataFrame({'username': [username], 'password': [hashed_password]})
    df = pd.concat([df, new_user_df], ignore_index=True)
    df.to_excel(excel_file)

def check_user(username, password):
    global df
    user = df[df['username'] == username]
    if not user.empty:
        return check_password_hash(user.iloc[0]['password'], password)
    return False

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if check_user(username, password):
            return redirect(url_for('profile'))
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        global df
        save_new_user(username, password)
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=True)
