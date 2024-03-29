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

@app.route('/api/delete_timeline_post/<int:id>', methods=['DELETE'])
def delete_timeline_post(id):
    try:
        timeline_post = TimelinePost.get_by_id(id)
        timeline_post.delete_instance()
        return 'Timeline post deleted successfully', 200
    except TimelinePost.DoesNotExist:
        return 'Timeline post not found', 404