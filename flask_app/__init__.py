from flask import Flask

app = Flask(__name__)

app.secret_key = 'I_hate_MealPrep'
#Controls Maximum file upload for app to 10 megabyte
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000