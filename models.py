from extensions import db
import json
import bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    subscription_plan = db.Column(db.String(20), nullable=False, default='Starter')

    # Using a simple JSON string to store a list of completed tasks
    _completed_tasks = db.Column(db.Text, nullable=False, default='[]')

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    @property
    def completed_tasks(self):
        return json.loads(self._completed_tasks)

    @completed_tasks.setter
    def completed_tasks(self, value):
        self._completed_tasks = json.dumps(value)

    def __repr__(self):
        return f'<User {self.username}>'