from flask import Flask
from flask_cors import CORS
import os

from file_upload.file_upload import file_import_page

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(file_import_page)


if __name__ == '__main__':
    app.run(port=os.environ.get('BACKEND_PORT'), debug=True)
