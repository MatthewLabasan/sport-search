from flask import Blueprint, render_template, g, session, flash, redirect, url_for
from sqlalchemy import *
from sqlalchemy.pool import NullPool

home_api = Blueprint('home', __name__)
DATABASEURI = "postgresql://bl3092:938417@104.196.222.236/proj1part2"
engine = create_engine(DATABASEURI)

@home_api.route('/')
def home(): 
    username = session.get('username', None)
    name = session.get('name', None)
    # state = session.get('state', None)

    if not username:
        flash("User not logged in.", "error")
        return redirect(url_for('login'))
    
    user_query = text("""SELECT coordinate FROM "Users" WHERE username = :username""")
    with engine.connect() as conn:
        user_result = conn.execute(user_query, {'username': username}).fetchone()
    
    if not user_result:
        flash("User's location not found.", "error")
        return redirect(url_for('home'))
    
    coordinate = user_result[0]
    latitude, longitude = map(float, coordinate.split())
    
    lat_min = latitude - 5
    lat_max = latitude + 5
    lon_min = longitude - 5
    lon_max = longitude + 5

    # get sports in their city
    # sports_query = """
    #                SELECT *
    #                FROM "Sports" S INNER JOIN "Location" L
    #                     ON S.coordinate = L.coordinate
    #                WHERE L.state = :state
    #                """
    sports_query = """
            SELECT * FROM "Sports"
            WHERE 
                substring(coordinate from '^[^ ]+')::float BETWEEN :lat_min AND :lat_max
                AND substring(coordinate from '[^ ]+$')::float BETWEEN :lon_min AND :lon_max
    """
    
    # sports_paramaters = {'state': state}
    sports_paramaters = {
        'lat_min': lat_min,
        'lat_max': lat_max,
        'lon_min': lon_min,
        'lon_max': lon_max
    }
    sports = g.conn.execute(text(sports_query), sports_paramaters)
    sports = sports.fetchall()

    for sport in sports:
        print(sport)

    context = { 'sports': sports,
                'name': name }

    return render_template('homepage.html', **context)