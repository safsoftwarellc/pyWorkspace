import os
import unittest
import sys

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from main import create_app, db
from main.model import user
from __init__ import blueprint
from main.model import blacklist

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)
migarte = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()

@manager.command
def test():
    """unit tests"""
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1        

if __name__ == '__main__':
    manager.run()


