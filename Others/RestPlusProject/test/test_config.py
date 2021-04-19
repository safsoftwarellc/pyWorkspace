import os
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app
from main.config import basedir

class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('main.config.DevelopmentConfig')
        return app

    def test_app_for_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'thisnotscecret')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
        )

class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('main.config.TestingConfig')
        return app
    
    def test_app_for_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'thisnotscecret')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
        )

class TestProdcutionConfig(TestCase):
    def create_app(self):
        app.config.from_object('main.config.ProdcutionConfig')
        return app
    
    def test_app_for_production(self):
        self.assertTrue(app.config['DEBUG'] is False)
    
if __name__ == '__main__':
    unittest.main()