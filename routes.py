from flask import *
from functools import wraps
import pymongo

from flask.ext.mongoengine import MongoEngine
from mongoengine import connect





app = Flask(__name__)
app.config.from_object(__name__)
app.config['DATABASE']

"""
app.config['MONGODB_SETTINGS'] = {
    'db': 'tasks',
    'host': 'localhost',
    'port': 27017
}
connect('tasks')

db = MongoEngine(app)

"""
#db.createCollection(alltasks)
#task = {'name':'CGM','date':'10/15/2014','priority':'1','status':1}
#db.alltasks.insert(task)

app.secret_key = 'my precious'



def connect_db():
	return pymongo.MongoClient()

@app.route('/',methods=['GET','POST'])
def home():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'BoyiJiang' or request.form['password'] != '843073':
			error = 'Invalid username or password, please try again.'
		else:
			session['logged_in'] = True
			return redirect(url_for('tasks'))
	return render_template('home.html', error = error)

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to log in first.')
			return redirect(url_for('home'))
	return wrap	


@app.route('/tasks')
@login_required
def tasks():
	task = db.alltasks.find_one()

	return render_template('tasks.html',task=task)

@app.route('/tasks')
@login_required	
def new_task():
	name = request.form['name']
	date = request.form['due_date']
	priority = request.form['priority']
	if not name and not date and not priority:
		flash('You forgot the task name, due date and priority!')
		return redirect(url_for('tasks'))
	else:
		task = {"name":name,"date":date,"priority":priority,"status":1}
		db.alltasks.insert(task)
		flash('New entry was successfully posted')	
		return redirect(url_for('tasks'))	
	

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	return redirect(url_for('home'))	






if __name__ == '__main__':
	app.run(debug=True)
