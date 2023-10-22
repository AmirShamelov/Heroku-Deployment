import os 
import unittest

from project import db, app
from project.models import User
from project._config import basedir

TEST_DB = 'test.db'

class MainTests(unittest.TestCase):

    #setup and teardown#

    def setUp(self):
            app.config['TESTING'] = True
            app.config['WTF_CSRF_ENABLED'] = False
            app.config['DEBUG'] = False
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                os.path.join(basedir, TEST_DB)
            self.app = app
            self.app_ctxt = self.app.app_context()
            self.app_ctxt.push() 
            db.create_all()
            self.client = self.app.test_client()
   
            self.assertEquals(app.debug, False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctxt.pop()
        self.app = None
        self.app_ctxt = None

    def login(self, name, password):
        return self.client.post('/', data=dict(
            name= name, password=password), follow_redirects=True)


    #test#

    def test_404_error(self):
        response = self.client.get('/this_route_does_not_exist/')
        self.assertEquals(response.status_code, 404)
        self.assertIn(b'Sorry. There is nothing here.', response.data)

    def test_500_error(self):
        bad_user=User(
            name='Jeremy',
            email='jeremy@realpython.com',
            password='django'
        )
        db.session.add(bad_user)
        db.session.commit()
        self.assertRaises(ValueError, self.login, 'Jeremy', 'django')
        try:
            response = self.login('Jeremy', 'django')
            self.assertEquals(response.status_code, 500)
        except ValueError:
            pass


if __name__ == '__main__':
    unittest.main()
