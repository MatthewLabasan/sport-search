"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
# accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, abort, session, flash, url_for, jsonify
from datetime import datetime

# templates
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = '\xc0e\x1fe\xf4\x85\xb1\x84\xcfI\xc0t\xbf\xa4\x8ek-4\x1b\xfbz\t#d' 

# routes
from routes.home_api import home_api

# blueprints
app.register_blueprint(home_api, url_prefix='/home')

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of:
#
#     postgresql://user:password@104.196.222.236/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@104.196.222.236/proj1part2"
#
DATABASEURI = "postgresql://bl3092:938417@104.196.222.236/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
conn = engine.connect()

# The string needs to be wrapped around text()

# conn.execute(text("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );"""))
# conn.execute(text("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');"""))


# conn.execute(text("""SELECT * FROM "Users"; """))

# To make the queries run, we need to add this commit line

# conn.commit() 

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: https://flask.palletsprojects.com/en/2.0.x/quickstart/?highlight=routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: https://flask.palletsprojects.com/en/2.0.x/api/?highlight=incoming%20request%20data

  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  #
  # example of a database query 
  #
  # cursor = g.conn.execute(text("""SELECT * FROM "Sports"; """))
  # g.conn.commit()

  # 2 ways to get results

  # Method 1 - Indexing result by column number
  # names = []
  # for result in cursor:
  #   names.append(result[0])  

  # Method 2 - Indexing result by column name
  # names = []
  # results = cursor.mappings().all()
  # for result in results:
  #   names.append(result["name"])

  # cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #
  #     # creates a <div> tag for each element in data
  #     # will print:
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  # context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html")

#
# This is an example of a different path.  You can see it at:
#
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        coordinate = request.form['coordinate']
        name = request.form['name']
        age = request.form['age']
        
        # Insert into Users table
        insert_query = text("""
            INSERT INTO "Users" (username, coordinate, name, age)
            VALUES (:username, :coordinate, :name, :age)
        """)
        
        try:
            with engine.connect() as conn:
                conn.execute(insert_query, {
                    'username': username,
                    'coordinate': coordinate,
                    'name': name,
                    'age': age
                })
                conn.commit()  # Commit the transaction
            session['username'] = username
            flash("User registered successfully!", "success")
        except Exception as e:
            flash(f"Error registering user: {e}", "error")
        
        return redirect(url_for('home.home'))
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        # Check if user exists
        query = text("""SELECT * FROM "Users" WHERE username = :username """)
        try:
            with engine.connect() as conn:
                result = conn.execute(query, {'username': username}).fetchone()
            if result:
                session['username'] = username
                flash("Logged in successfully!", "success")
                return redirect(url_for('home.home'))
            else:
                flash("Invalid username.", "error")
        except Exception as e:
            flash(f"Error logging in: {e}", "error")
    
    return render_template("login.html")

@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        # Handle the form submission to add a review
        try:
            data = request.form
            sport_type = data['sport_type']
            trail_name = data['trail_name']
            date_completed = data['date_completed']
            rating = data['rating']
            comments = data['comments']

            # debug
            print(f"Form data received: sport_type={sport_type}, trail_name={trail_name}, date_completed={date_completed}, rating={rating}, comments={comments}")

            username = session.get('username')
            if not username:
                flash("User not logged in.", "error")
                return redirect(url_for('login'))

            sport_query = text("""SELECT sport_id 
                               FROM "Sports" 
                               WHERE sport_type = :sport_type AND trail_name = :trail_name
                        """)
            with engine.connect() as conn:
                sport_result = conn.execute(sport_query, {'sport_type': sport_type, 'trail_name': trail_name}).fetchone()
            if not sport_result:
                flash("Sport not found.", "error")
                print("Sport not found.")
                return redirect(url_for('add_review'))
            
            sport_id = sport_result[0]
            time_written = datetime.now().date()

            # Generate a new review_id
            with engine.connect() as conn:
                max_review_query = text("""SELECT COALESCE(MAX(review_id), 0) + 1 FROM \"Review\"""")
                review_id = conn.execute(max_review_query).scalar()
                # debug
                # print(f"Generated new review_id: {review_id}")

            insert_query = text("""
                INSERT INTO "Review" (review_id, username, sport_id, time_written, date_completed, rating, comments, like_count)
                VALUES (:review_id, :username, :sport_id, :time_written, :date_completed, :rating, :comments, :like_count)
            """)
            with engine.connect() as conn:
                conn.execute(insert_query, {
                    'review_id': review_id,
                    'username': username,
                    'sport_id': sport_id,
                    'time_written': time_written,
                    'date_completed': date_completed,
                    'rating': rating,
                    'comments': comments,
                    'like_count': 0
                })
                conn.commit()
                print("Review added successfully.")
                flash("Review added successfully!", "success")
        except Exception as e:
            flash(f"Error adding review: {e}", "error")
            print(f"Error adding review: {e}")
        
        return redirect(url_for('completed'))
    
    elif request.method == 'GET':
        # Handle the GET request to show the add_review form
        sport_id = request.args.get('sport_id')
        sport_type = request.args.get('sport_type')
        trail_name = request.args.get('trail_name')

        if not sport_id or not sport_type or not trail_name:
            flash("Sport details not provided.", "error")
            return redirect(url_for('completed'))

        # Render the add_review.html page with the sport details pre-filled
        return render_template("add_review.html", sport_id=sport_id, sport_type=sport_type, trail_name=trail_name)



@app.route('/find_sport', methods=['GET', 'POST'])
def find_sport():
    username = session.get('username')
    if not username:
        flash("User not logged in.", "error")
        return redirect(url_for('login'))
    
    sport_types = ["skiing", "hiking", "biking", "kayaking", "scuba diving"]
    difficulties = ["beginner", "intermediate", "advanced"]
    sports = []
    if request.method == 'POST':
        sport_type = request.form.get('sport_type')
        trail_name = request.form.get('trail_name')
        rating = request.form.get('rating', type=float)
        difficulty = request.form.get('difficulty')

        query ="""
            SELECT s.sport_id, s.sport_type, s.trail_name, s.difficulty, s.rating, s.price, s.num_people_completed
            FROM "Sports" s
            WHERE s.sport_type = :sport_type
        """
        params = {'sport_type': sport_type}

        if trail_name:
            query += " AND trail_name = :trail_name"
            params['trail_name'] = trail_name
        if rating is not None:
            query += " AND rating >= :rating"
            params['rating'] = rating
        if difficulty:
            query += " AND difficulty = :difficulty"
            params['difficulty'] = difficulty

        try:
            with engine.connect() as conn:
                result = conn.execute(text(query), params)
                sports = [dict(row) for row in result.mappings()]

                # Check which sports have been completed by the user
                for sport in sports:
                    check_completed_query = text("""
                        SELECT status FROM "Status"
                        WHERE username = :username AND sport_id = :sport_id AND status = 'completed'
                    """)
                    completed_result = conn.execute(check_completed_query, {'username': username, 'sport_id': sport['sport_id']}).fetchone()
                    if completed_result:
                        sport['completed'] = True  # Mark the sport as completed
                    else:
                        sport['completed'] = False  # Mark the sport as not completed
                
                # Add "save button" visibility based on whether it's saved or not
                for sport in sports:
                    check_saved_query = text("""
                        SELECT * FROM "Status"
                        WHERE username = :username AND sport_id = :sport_id AND status = 'saved'
                    """)
                    saved_result = conn.execute(check_saved_query, {'username': username, 'sport_id': sport['sport_id']}).fetchone()
                    if saved_result:
                        sport['saved'] = True  # Mark the sport as saved
                    else:
                        sport['saved'] = False 

        except SQLAlchemyError as e:
            flash(f"Error finding sports: {e}", "error")
            return redirect(url_for('find_sport'))
    return render_template("find_sport.html", sports=sports, sport_types=sport_types, difficulties=difficulties)


@app.route('/like_sport', methods=['POST'])
def like_sport():
    username = session.get('username')
    if not username:
        flash("User not logged in.", "error")
        return redirect(url_for('login'))
    
    sport_id = request.form.get('sport_id')
    if not sport_id:
        flash("Sport ID not provided.", "error")
        return redirect(url_for('find_sport'))
    
    like_query = text("""
        INSERT INTO "Likes" (username, sport_id, date_liked)
        VALUES (:username, :sport_id, :date_liked)
    """)
    try:
        with engine.connect() as conn:
            conn.execute(like_query, {
                'username': username,
                'sport_id': sport_id,
                'date_liked': datetime.now().date()
            })
            conn.commit()
        flash("Sport liked successfully!", "success")
    except Exception as e:
        flash(f"Error liking sport: {e}", "error")
    return redirect(url_for('find_sport'))


@app.route('/completed', methods=['GET'])
def completed():
    username = session.get('username')
    if not username:
        flash("User not logged in.", "error")
        return redirect(url_for('login'))
    
    query = text("""
        SELECT s.sport_id, s.sport_type, s.trail_name, s.difficulty, s.rating
        FROM "Sports" s
        JOIN "Status" st ON s.sport_id = st.sport_id
        WHERE st.username = :username AND st.status = 'completed'
    """)
    try:
        with engine.connect() as conn:
            result = conn.execute(query, {'username': username})
            completed_sports = [dict(row) for row in result.mappings()]
            # Debugging
            print(f"Completed Sports for {username}: {completed_sports}")
    except Exception as e:
        flash(f"Error fetching completed sports: {e}", "error")
        completed_sports = []
    
    return render_template("completed.html", completed_sports=completed_sports)

@app.route('/saved', methods=['GET'])
def saved():
    username = session.get('username')
    if not username:
        flash("User not logged in.", "error")
        return redirect(url_for('login'))
    
    query = text("""
        SELECT s.sport_id, s.sport_type, s.trail_name, s.difficulty, s.rating 
        FROM "Sports" s
        JOIN "Status" st ON s.sport_id = st.sport_id
        WHERE st.username = :username AND st.status = 'saved'
    """)
    try:
        with engine.connect() as conn:
            result = conn.execute(query, {'username': username})
            saved_sports = [dict(row) for row in result.mappings()]
            # Debugging
            print(f"Saved Sports for {username}: {saved_sports}")
    except Exception as e:
        flash(f"Error fetching saved sports: {e}", "error")
        saved_sports = []
    
    return render_template("saved.html", saved_sports=saved_sports)


@app.route('/save_sport', methods=['POST'])
def save_sport():
    username = session.get('username')
    if not username:
        flash("User not logged in.", "error")
        return redirect(url_for('login'))
    
    sport_id = request.form.get('sport_id')
    if not sport_id:
        flash("Sport ID not provided.", "error")
        return redirect(url_for('find_sport'))
    
    # Check if the sport is already saved by the user
    check_query = text("""
        SELECT * FROM "Status" 
        WHERE username = :username AND sport_id = :sport_id AND status = 'saved'
    """)
    try:
        with engine.connect() as conn:
            existing_entry = conn.execute(check_query, {
                'username': username,
                'sport_id': sport_id
            }).fetchone()
            if existing_entry:
                # flash("You already saved this sport.", "error")
                # return redirect(url_for('find_sport'))
                return jsonify({'message': "You already saved this sport."}), 200
            else:
                # Insert the saved sport into the Status table
                insert_query = text("""
                    INSERT INTO "Status" (username, sport_id, status)
                    VALUES (:username, :sport_id, 'saved')
                """)
                conn.execute(insert_query, {
                    'username': username,
                    'sport_id': sport_id
                })
                conn.commit()
                return jsonify({'message': "Sport saved successfully!"}), 200
                # flash("Sport saved successfully!", "success")
    except Exception as e:
        # flash(f"Error saving sport: {e}", "error")
        return jsonify({'message': f"Error saving sport: {str(e)}"}), 500
    
    return redirect(url_for('find_sport'))


@app.route('/unsave_sport', methods=['POST'])
def unsave_sport():
    username = session.get('username')
    if not username:
        flash("User not logged in.", "error")
        return redirect(url_for('login'))

    sport_id = request.form.get('sport_id')
    if not sport_id:
        flash("Sport ID not provided.", "error")
        return redirect(url_for('saved'))

    # Remove the saved sport from the Status table
    delete_query = text("""
        DELETE FROM "Status"
        WHERE username = :username AND sport_id = :sport_id AND status = 'saved'
    """)
    try:
        with engine.connect() as conn:
            result = conn.execute(delete_query, {
                'username': username,
                'sport_id': sport_id
            })
            conn.commit()
            if result.rowcount > 0:
                flash("Sport unsaved successfully!", "success")
            else:
                flash("Sport could not be unsaved. Please try again.", "error")
    except Exception as e:
        flash(f"Error unsaving sport: {e}", "error")

    return redirect(url_for('saved'))


@app.route('/complete_sport', methods=['POST'])
def complete_sport():
    username = session.get('username')
    if not username:
        flash("User not logged in.", "error")
        return redirect(url_for('login'))

    sport_id = request.form.get('sport_id')
    if not sport_id:
        flash("Sport ID not provided.", "error")
        return redirect(url_for('saved'))

    # Check if the sport is saved by the user
    check_query = text("""
        SELECT * FROM "Status" 
        WHERE username = :username AND sport_id = :sport_id AND status = 'saved'
    """)
    try:
        with engine.connect() as conn:
            existing_entry = conn.execute(check_query, {'username': username, 'sport_id': sport_id}).fetchone()
            # Debugging: Print if the sport is already saved or not
            if existing_entry:
                print("Sport is currently saved, proceeding to update the status to completed.")
            else:
                print("Sport is not saved or already completed.")

            
            if not existing_entry:
                flash("Sport is not saved or already marked as completed.", "error")
                return redirect(url_for('saved'))

            # Update the status to 'completed'
            update_query = text("""
                UPDATE "Status"
                SET status = 'completed'
                WHERE username = :username AND sport_id = :sport_id AND status = 'saved'
            """)
            result = conn.execute(update_query, {'username': username, 'sport_id': sport_id})
            conn.commit()
            
            if result.rowcount == 0:
                print("Update failed. No rows were affected.")
                flash("Sport could not be marked as completed. Please try again.", "error")
            else:
                print("Update succeeded. Sport marked as completed.")
                flash("Sport marked as completed successfully!", "success")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        flash(f"Error marking sport as completed: {e}", "error")
    
    return redirect(url_for('saved'))


# @app.route('/login')
# def login():
#     abort(401)
#     this_is_never_executed()

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python3 server.py

    Show the help text using:

        python3 server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()

