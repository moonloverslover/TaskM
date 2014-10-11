from flask import *
from functools import wraps


from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super-secret'

# MongoDB Config
app.config['MONGODB_DB'] = 'tasksDB'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017

db = MongoEngine(app)



class Task(db.Document):
	name = db.StringField(max_length=50, required=True)
	due_date = db.StringField(max_length=15, required=True)
	priority = db.StringField(max_length=2, required=True)
	status = db.IntField(required=True)


# Create a user to test with
#@app.before_first_request
#def dummy_task():
#	Task(name='Dummy', due_date='10/10/2999',priority='1',status=0).save()


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
	opentasks = Task.objects(status=1)
	closedtasks = Task.objects(status=0)
	return render_template('tasks.html',opentasks=opentasks,closedtasks=closedtasks)

@app.route('/tasks',methods=['GET','POST'])
@login_required	
def new_task():
	name = request.form['name']
	date = request.form['due_date']
	priority = request.form['priority']
	if not name and not date and not priority:
		flash('You forgot the task name, due date and priority!')
		return redirect(url_for('tasks'))
	elif not name and not date:
		flash('You forgot the name and date!')
		return redirect(url_for('tasks'))
	elif not date and not priority:
		flash('You forgot the date and priority!')
		return redirect(url_for('tasks'))
	elif not name and not priority:
		flash('You forgot the name and priority!')
		return redirect(url_for('tasks'))
	elif not name:
		flash('You forgot the name!')
		return redirect(url_for('tasks'))
	elif not date:
		flash('You forgot the date!')
		return redirect(url_for('tasks'))
	elif not priority:
		flash('You forgot the priority!')
		return redirect(url_for('tasks'))					
	else:
		Task(name=name, due_date=date,priority=priority,status=1).save()
		flash('New entry was successfully posted.')	
		return redirect(url_for('tasks'))	

@app.route('/delete/<task_id>')
@login_required	
def delete_task(task_id):
	Task.objects(id=task_id).delete()
	flash('The task was deleted!')
	return redirect(url_for('tasks'))	

@app.route('/complete/<task_id>')
@login_required	
def mark_complete(task_id):
	task = Task.objects(id=task_id).update(set__status=0)
	flash('The task was marked as complete!')
	return redirect(url_for('tasks'))



@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	return redirect(url_for('home'))	



if __name__ == '__main__':
	app.run(debug=True)
