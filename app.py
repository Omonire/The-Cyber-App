import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash, g
from extensions import db
from dotenv import load_dotenv
from functools import wraps

# These imports will be used later, including the new User model
from flask import session
from modules.feeds import get_news, get_blog_posts
from modules.tasks import get_tasks
from modules.tools import analyze_password_strength

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')

# Initialize the database with the app
db.init_app(app)

# Import models here to ensure they are registered with SQLAlchemy
from models import User

from flask import session
# --- Decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash('An account with this email already exists.', 'error')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=g.user)

@app.route('/tasks')
@login_required
def tasks():
    all_tasks = get_tasks()
    completed_tasks = g.user.completed_tasks if g.user else []

    available_tasks = [task for task in all_tasks if task not in completed_tasks]

    daily_task = "You've completed all available tasks! Great job staying secure." if not available_tasks else available_tasks[0]

    return render_template('tasks.html', task=daily_task, all_tasks_completed=(not available_tasks))

@app.route('/complete-task', methods=['POST'])
@login_required
def complete_task():
    task_text = request.form.get('task_text')
    if task_text and g.user:
        current_tasks = g.user.completed_tasks
        if task_text not in current_tasks:
            current_tasks.append(task_text)
            g.user.completed_tasks = current_tasks
            db.session.commit()
            flash('Great job! Task marked as complete.', 'success')

    return redirect(url_for('tasks'))

@app.route('/news')
def news():
    articles = get_news()
    return render_template('news.html', articles=articles)

@app.route('/blog')
def blog():
    posts = get_blog_posts()
    return render_template('blog.html', posts=posts)

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/tools/password-strength-analyzer', methods=['GET', 'POST'])
def password_strength_analyzer():
    results = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password:
            results = analyze_password_strength(password)
    return render_template('password_strength_analyzer.html', results=results)

@app.route('/payment-instructions/<plan>')
@login_required
def payment_instructions(plan):
    plans_info = {
        "Basic": {"price": "₦10,000"},
        "Pro": {"price": "₦25,000"}
    }
    return render_template('payment_instructions.html', plan=plan, plan_info=plans_info.get(plan, {}))

if __name__ == '__main__':
    app.run(debug=True, port=8000)