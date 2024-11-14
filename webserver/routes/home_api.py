from flask import Blueprint, render_template, g
from sqlalchemy import *
from sqlalchemy.pool import NullPool

home_api = Blueprint('api', __name__)

@home_api.route('/')
def home(): 
    username = "alice01" # must be a tuple"

    # we may want to only show sports in their local area for now
    trail_names = g.conn.execute(text("""
        SELECT trail_name 
        FROM "Sports";
    """))

    user = g.conn.execute(text("""
        SELECT username
        FROM "Users"
        WHERE username = :username
    """), {"username": username})

    trail_names = trail_names.fetchall()
    user = user.fetchone()

    context = { 'trails': trail_names,
                'name': user }
    
    for trail_name in trail_names:
        print(trail_name)

    return render_template('homepage.html', **context)