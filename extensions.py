from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy instance without an app,
# it will be initialized in the main app file.
db = SQLAlchemy()