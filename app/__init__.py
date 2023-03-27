import os
import datetime
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict
from peewee import DatabaseProxy

mydb = DatabaseProxy()


load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri = True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

# if os.getenv("TESTING") == "true":
#     print("Running in test mode")
#     test_db = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
#     mydb.initialize(test_db)
#     mydb.connect()
# else:
#     mydb.initialize(MySQLDatabase(os.getenv("MYSQL_DATABASE"),
#         user=os.getenv("MYSQL_USER"),
#         password=os.getenv("MYSQL_PASSWORD"),
#         host=os.getenv("MYSQL_HOST"),
#         port=3306
#     ))
#     mydb.connect()

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)


    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

mydb.close()
@app.before_request
def _db_connect():
    mydb.connect()

# This hook ensures that the connection is closed when we've finished processing the request.
@app.teardown_request
def _db_close(exc):
    if not mydb.is_closed():
        mydb.close()

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")


# @app.route('/api/timeline_post', methods=['POST'])
# def post_time_line_post():
#     name = request.form['name']
#     email = request.form['email']
#     content = request.form['content']
#     timeline_post = TimelinePost.create(name=name, email=email, content=content)

#     return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if not name:
        return {'error': 'Missing name parameter'}, 400

    if not email:
        return {'error': 'Missing email parameter'}, 400

    if not content:
        return {'error': 'Missing content parameter'}, 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

# Suggested
    # if not content:
    #     abort(400, 'Invalid content')
    # elif not name:
    #     abort(400, 'Name is required')
    # elif not re.match(r'^[a-zA-Z\s]+$', name):
    #     abort(400, 'Invalid name')
    # elif not re.match(r'^\S+@\S+\.\S+$', email):
    #     abort(400, 'Invalid email')

# @app.route('/api/timeline_post', methods=['GET'])
# def get_time_line_post():
#     return {
#         'timeline_posts': [
#             model_to_dict(p)
#             for p in 
# TimelinePost.select().order_by(TimelinePost.created_at.desc())
#         ]
#     }

# From the unit test
"""
In the test code, the test_get_time_line_post method was failing due to an assertion error. Specifically, 
the assertion self.assertEqual(first_post_data['id'], first_post.id) failed with an error AssertionError: 2 != 1.
To fix the issue, I updated the test code to correctly set the id value of the first post, which was expected to 
be 1 instead of the default value of 2. The line assert first_post.id == 1 was added to the test_timeline_post method 
to ensure that the first post's id was set correctly. Additionally, the tearDown method was modified to close 
the database connection after dropping the tables to avoid any potential resource leaks.
"""

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    timeline_posts = (
        TimelinePost
        .select()
        .order_by(TimelinePost.created_at.asc())
    )
    return {
        'timeline_posts': [            model_to_dict(p)            for p in timeline_posts        ]
    }

#Suggested
# @app.route('/api/timeline_post', methods=['GET'])
# def get_time_line_post():
#     return {
#         'timeline_posts': [
#             model_to_dict(p)
#             for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
#         ]
#     }

@app.route('/api/delete_timeline_post/<int:id>', methods=['DELETE'])
def delete_timeline_post(id):
    try:
        timeline_post = TimelinePost.get_by_id(id)
        timeline_post.delete_instance()
        return 'Timeline post deleted successfully', 200
    except TimelinePost.DoesNotExist:
        return 'Timeline post not found', 404
    





# name: Deploy

# on:
#   push:
#     branches:
#       - main
#   workflow_dispatch:

# jobs:
#   deploy:
#     name: "Deploy to VPS"
#     runs-on: ubuntu-latest
#     steps:
#       - name: Configure SSH
#         run: |
#           mkdir -p ~/.ssh/
#           echo "$SSH_PRIVATE_KEY" > ~/.ssh/deploy-key.pem
#           chmod 600 ~/.ssh/deploy-key.pem
#           cat >> ~/.ssh/config <<END
#           Host my-vps
#             HostName $SSH_IP
#             User $SSH_USER
#             IdentityFile ~/.ssh/deploy-key.pem
#             StrictHostKeyChecking no
#           END
#         env:
#           SSH_USER: ${{ secrets.SSH_USER }}
#           SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
#           SSH_IP: ${{ secrets.SSH_IP }}
#           PROJECT_ROOT: ${{ secrets.PROJECT_ROOT }}

#       - name: Print project root directory
#         run: ssh my-vps 'cd $PROJECT_ROOT && pwd'