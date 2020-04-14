from datetime import datetime
import logging
import os

from flask import Flask, redirect, render_template, request

from google.cloud import datastore

timest = '0'
n = 0
a = 0
# CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')

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
    return render_template('home.html', image_entities=image_entities)


@app.route('/questionpage/<kinde>')
def questionpage(kinde):
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    timest=kinde

    # Use the Cloud Datastore client to fetch information from Datastore about
    # each photo.
    query = datastore_client.query(kind=kinde)
    image_entities = list(query.fetch())

    # Return a Jinja2 HTML template and pass in image_entities as a parameter.
    return render_template('question.html', image_entities=image_entities,kind=kinde)

@app.route('/questionpage/upload_answer<kinde>', methods=['GET', 'POST'])
def upload_answer(kinde):  
    answerr= request.form['nm']
    datastore_client = datastore.Client()
    #query = datastore_client.query(kind=kinde)
    #image_entities = list(query.fetch())
    #for image_entity in image_entities:
    #   n=image_entity['answerNo']
    #   image_entity['answerNo']=n+1 
    kind=kinde
    key = datastore_client.key(kind, answerr)

    entity = datastore.Entity(key)
    entity['quess']=answerr
    datastore_client.put(entity)
    

    query = datastore_client.query(kind=kinde)
    image_entities = list(query.fetch())

    return render_template('question.html', image_entities=image_entities,kind=kinde)


       
      
    
    


    


@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    name = request.form['nm']
 
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Fetch the current date / time.
    current_datetime = datetime.now()
    times=str(current_datetime)

    # The kind for the new entity.
    kind = 'Ques'

    # Create the Cloud Datastore key for the new entity.
    key = datastore_client.key(kind, name)

    entity = datastore.Entity(key)

    entity['timestamp'] = times
    entity['Question']=name
    # entity['joy'] = face_joy
    entity['kinde']=name
    
    # Save the new entity to Datastore.
    datastore_client.put(entity)
    

    #new kind
    kind = times

    # Create the Cloud Datastore key for the new entity.
    key = datastore_client.key(kind, name)

    entity = datastore.Entity(key)
    entity['quess']=name
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
