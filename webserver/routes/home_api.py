from flask import Blueprint, render_template, g
from sqlalchemy import *
from sqlalchemy.pool import NullPool

home_api = Blueprint('api', __name__)

@home_api.route('/')
def home():
    # we may want to only show sports in their local area for now
    trail_names = g.conn.execute(text("""
        SELECT trail_name 
        FROM "Sports";
    """))

    trail_names = trail_names.fetchall()

    context = { 'trails': trail_names }
    for trail_name in trail_names:
        print(trail_name[0])

    return render_template('homepage.html', **context)