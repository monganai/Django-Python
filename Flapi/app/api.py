from app import app,db
from ddtrace import patch_all
import logging
patch_all()


logging.basicConfig(filename='error.log',level=logging.DEBUG)
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'CrashLocationPoint' : CrashLocationPoint}
