
from models import User, db

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
db.session.commit()

# Add Users
user1 = User(first_name='Bob', last_name="Sagot", image_url="https://m.media-amazon.com/images/M/MV5BMTQxMTY2NjE1NF5BMl5BanBnXkFtZTcwNjIyMjM2MQ@@._V1_.jpg")
user2 = User(first_name='Doug', last_name="Bowser", image_url="https://static.wikia.nocookie.net/nintendo/images/7/72/Doug_Bowser.jpg/revision/latest?cb=20190221195817&path-prefix=en")
user3 = User(first_name='Elon', last_name="Musk", image_url="https://media.cnn.com/api/v1/images/stellar/prod/2023-11-30t135953z-879534570-rc2on4amk5bn-rtrmadp-3-twitter-musk.jpg?c=16x9&q=h_833,w_1480,c_fill")

# Add new objects to session, so they'll persist
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# Commit--otherwise, this never gets saved!
db.session.commit()
