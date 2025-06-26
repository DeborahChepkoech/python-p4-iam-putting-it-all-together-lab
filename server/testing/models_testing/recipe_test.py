import pytest
from sqlalchemy.exc import IntegrityError

from config import app, db
from models import User, Recipe

class TestRecipe:
    '''Recipe in models.py'''

    @pytest.fixture(autouse=True)
    def setup_user_for_recipes(self, session, request):
        unique_username = f'recipeowner_{request.node.nodeid.split("::")[-1]}'
        user = User(username=unique_username, bio='Owner of recipes')
        user.password_hash = 'ownerpass'
        session.add(user)
        session.commit()
        self.user = user

    def test_has_attributes(self, session):
        '''has attributes title, instructions, and minutes_to_complete.'''

        recipe = Recipe(
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
                user=self.user
                )

        session.add(recipe)
        session.commit()

        new_recipe = Recipe.query.filter(Recipe.title == "Delicious Shed Ham").first()

        assert new_recipe.title == "Delicious Shed Ham"
        assert new_recipe.instructions == """Or kind rest bred with am shed then. In""" + \
                """ raptures building an bringing be. Elderly is detract""" + \
                """ tedious assured private so to visited. Do travelling""" + \
                """ companions contrasted it. Mistress strongly remember""" + \
                """ up to. Ham him compass you proceed calling detract.""" + \
                """ Better of always missed we person mr. September""" + \
                """ smallness northward situation few her certainty""" + \
                """ something."""
        assert new_recipe.minutes_to_complete == 60
        assert new_recipe.user == self.user

    def test_requires_title(self, session):
        '''requires each record to have a title.'''

        with pytest.raises(ValueError, match='Recipe title must be present.'):
            recipe = Recipe(
                title="",
                instructions="This is a dummy instruction text that is long enough, at least 50 characters, to pass validation.",
                minutes_to_complete=30,
                user=self.user
            )
            session.add(recipe)
            session.commit()

    def test_requires_50_plus_char_instructions(self, session):
        '''must raise either a sqlalchemy.exc.IntegrityError with constraints or a custom validation ValueError'''
        with pytest.raises( (ValueError, IntegrityError) ) as excinfo:
            recipe = Recipe(
                title="Generic Ham",
                instructions="idk lol",
                user=self.user)
            session.add(recipe)
            session.commit()
        assert "Recipe instructions must be at least 50 characters long." in str(excinfo.value)
