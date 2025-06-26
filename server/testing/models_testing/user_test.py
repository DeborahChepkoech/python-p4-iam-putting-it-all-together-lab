from sqlalchemy.exc import IntegrityError
import pytest

from config import app, db, bcrypt
from models import User, Recipe

class TestUser:
    '''User in models.py'''

    def test_has_attributes(self, session):
        '''has attributes username, _password_hash, image_url, and bio.'''

        user = User(
            username="Liz",
            image_url="https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg",
            bio="""Dame Elizabeth Rosemond Taylor DBE (February 27, 1932""" + \
                """ - March 23, 2011) was a British-American actress. """ + \
                """She began her career as a child actress in the early""" + \
                """ 1940s and was one of the most popular stars of """ + \
                """classical Hollywood cinema in the 1950s. She then""" + \
                """ became the world's highest paid movie star in the """ + \
                """1960s, remaining a well-known public figure for the """ + \
                """rest of her life. In 1999, the American Film Institute""" + \
                """ named her the seventh-greatest female screen legend """ + \
                """of Classic Hollywood cinema."""
        )

        user.password_hash = "whosafraidofvirginiawoolf"

        session.add(user)
        session.commit()

        created_user = User.query.filter(User.username == "Liz").first()

        assert created_user.username == "Liz"
        assert created_user.image_url == "https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg"
        assert created_user.bio == \
            """Dame Elizabeth Rosemond Taylor DBE (February 27, 1932""" + \
            """ - March 23, 2011) was a British-American actress. """ + \
            """She began her career as a child actress in the early""" + \
            """ 1940s and was one of the most popular stars of """ + \
            """classical Hollywood cinema in the 1950s. She then""" + \
            """ became the world's highest paid movie star in the """ + \
            """1960s, remaining a well-known public figure for the """ + \
            """rest of her life. In 1999, the American Film Institute""" + \
            """ named her the seventh-greatest female screen legend """ + \
            """of Classic Hollywood cinema."""

        assert bcrypt.check_password_hash(created_user._password_hash.encode('utf-8'), b'whosafraidofvirginiawoolf')

        with pytest.raises(AttributeError):
            created_user.password_hash

    def test_requires_username(self, session):
        '''requires each record to have a username.'''

        with pytest.raises(ValueError, match='Username must be present.'):
            user = User(username="")
            user.password_hash = "somepassword"
            session.add(user)
            session.commit()

    def test_requires_unique_username(self, session):
        '''requires each record to have a unique username.'''

        user_1 = User(username="Ben")
        user_1.password_hash = "pass1"

        session.add(user_1)
        session.commit()

        with pytest.raises(ValueError, match='Username must be unique.'):
            user_2 = User(username="Ben")
            user_2.password_hash = "pass2"
            session.add(user_2)
            session.commit()

    def test_has_list_of_recipes(self, session):
        '''has records with lists of recipes records attached.'''

        user = User(username="Prabhdip")
        user.password_hash = "prabhdippass"

        recipe_1 = Recipe(
            title="Delicious Shed Ham",
            instructions="""Or kind rest bred with am shed then. In""" + \
                """ raptures building an bringing be. Elderly is detract""" + \
                """ tedious assured private so to visited. Do travelling""" + \
                """ companions contrasted it. Mistress strongly remember""" + \
                """ up to. Ham him compass you proceed calling detract.""" + \
                """ Better of always missed we person mr. September""" + \
                """ smallness northward situation few her certainty""" + \
                """ something.""",
            minutes_to_complete=60,
            )
        recipe_2 = Recipe(
            title="Hasty Party Ham",
            instructions="""As am hastily invited settled at limited""" + \
                         """ civilly fortune me. Really spring in extent""" + \
                         """ an by. Judge but built gay party world. Of""" + \
                         """ so am he remember although required. Bachelor""" + \
                         """ unpacked be advanced at. Confined in declared""" + \
                         """ marianne is vicinity.""" + \
                         """ This line is to ensure it is at least 50 characters long for validation.""",
            minutes_to_complete=30,
            )

        user.recipes.append(recipe_1)
        user.recipes.append(recipe_2)

        session.add(user)
        session.commit()

        session.refresh(user)

        assert user.id is not None
        assert recipe_1.id is not None
        assert recipe_2.id is not None

        assert recipe_1 in user.recipes
        assert recipe_2 in user.recipes

        assert recipe_1.user_id == user.id
        assert recipe_2.user_id == user.id