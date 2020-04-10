from datetime import datetime
import logging
import os

from flask import Flask, redirect, render_template, request

from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision


#CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')
blockList=[]



app = Flask(__name__)
@app.route('/')
def homepage():
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Use the Cloud Datastore client to fetch information from Datastore about
    # each photo.
    query = datastore_client.query(kind='Ques')
    image_entities = list(query.fetch())

    # Return a Jinja2 HTML template and pass in image_entities as a parameter.
    return render_template('homepage.html', image_entities=image_entities, length =len(blockList))


@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    

   
    name = request.form['nm']
    blockList.append(name)
    blockList.append('answer1')
    blockList.append('answer2')
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Fetch the current date / time.
    current_datetime = datetime.now()

    # The kind for the new entity.
    kind = 'Ques'

    # The name/ID for the new entity.
    #name = blob.name

    # Create the Cloud Datastore key for the new entity.
    key = datastore_client.key(kind, name)

    # Construct the new entity using the key. Set dictionary values for entity
    # keys blob_name, storage_public_url, timestamp, and joy.
    entity = datastore.Entity(key)
    #entity['blob_name'] = blob.name
    #entity['image_public_url'] = blob.public_url
    #entity['question'] = name
    for i in range(len(blockList)):
        entity[i]=blockList[i]

    entity['timestamp'] = current_datetime
    #entity['joy'] = face_joy

    # Save the new entity to Datastore.
    datastore_client.put(entity)

    # Redirect to the home page.
    return redirect('/')


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)