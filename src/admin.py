import os
from flask_admin import Admin
from models import db, User, Character, Planet, FavChar, FavPlanet
from flask_admin.contrib.sqla import ModelView

class CharacterAdmin(ModelView):
    column_list = ('id', 'name', 'species', 'age', 'origin_planet')
    form_columns = ('name', 'species', 'age', 'origin_planet')
    
class FavCharAdmin(ModelView):
    column_list = ('id', 'id_user', 'id_char', 'date')
    form_columns = ('id_user', 'id_char', 'date')

class FavPlanetAdmin(ModelView):
    column_list = ('id', 'id_user', 'id_planet', 'date')
    form_columns = ('id_user', 'id_planet', 'date')

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(CharacterAdmin(Character, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(FavCharAdmin(FavChar, db.session))
    admin.add_view(FavPlanetAdmin(FavPlanet, db.session))


    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))