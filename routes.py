from flask import *
from functools import wraps

app = Flask(__name__)

app.secret_key = 'token'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

#test to see if login is in session
def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('Please login to your account.')
			return redirect(url_for('log'))
	return wrap	

@app.route('/account-home')
@login_required
def accountHome():
	return render_template('account-home.html')

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash("You have successfully logged")
	return redirect (url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def log():
	error = None
	if request.method == "POST":
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Username and/or password.'
		else:
			session['logged_in'] = True
			return redirect(url_for('accountHome'))
	return render_template('login.html', error=error)


if __name__== '__main__':
	app.run(debug=True) #remove debuger=True for production