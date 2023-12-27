from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.app_context().push()

with app.app_context():
    db.drop_all()
    db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample User and post."""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="TestUser", last_name="dog", image_url='fake')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title='orange', content= 'orange juice', user_id= self.user_id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id


    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    '''all users test'''
    def test_list_Users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)

    '''user info test'''
    def test_show_User(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)

    '''submission test'''
    def test_add_User(self):
        with app.test_client() as client:
            d = {"first_name": "asdf", "last_name": "cat", "image_url": 'fake2'}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('asdf', html)

    # post testing
            
    '''post submission test'''
    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "potato", "content": "content", "user_id": self.user_id}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
    

    '''deletion test for post'''
    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertNotIn('orange', html)


    '''deletion test for user'''
    def test_delete_User(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertNotIn('TestUser', html)

    
            
    