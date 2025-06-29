#!/usr/bin/env python3

from random import randint, choice as rc

from faker import Faker

from config import app, db
from models import Recipe, User

fake = Faker()

with app.app_context():

    print("Deleting all records...")
    Recipe.query.delete()
    User.query.delete()

    fake = Faker()

    print("Creating users...")

    users = []
    usernames = set() # Use a set for efficient uniqueness checking

    for i in range(20):
        
        username = fake.first_name()
        while username in usernames:
            username = fake.first_name()
        usernames.add(username) # Add to the set

        user = User(
            username=username,
            bio=fake.paragraph(nb_sentences=3),
            image_url=fake.url(),
        )

        user.password_hash = user.username + 'password'

        users.append(user)

    db.session.add_all(users)

    print("Creating recipes...")
    recipes = []
    for i in range(100):
        instructions = fake.paragraph(nb_sentences=8)
        
        # Ensure instructions are at least 50 characters for validation
        while len(instructions) < 50:
            instructions += " " + fake.paragraph(nb_sentences=1)

        recipe = Recipe(
            title=fake.sentence(),
            instructions=instructions,
            minutes_to_complete=randint(15,90),
        )

        recipe.user = rc(users)

        recipes.append(recipe)

    db.session.add_all(recipes)
    
    db.session.commit()
    print("Complete.")
