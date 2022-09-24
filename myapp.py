import string

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# instantiate the app
app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


class Verbraucher(db.Model):
    __tablename__ = 'verbraucher'

    verbraucherId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.verbraucherId)

    def serialize(self):
        return {
            'verbraucherId': self.verbraucherId,
            'name': self.name
        }


class Stromlastdaten(db.Model):
    __tablename__ = 'stromlastdaten'

    stromlastdatenId = db.Column(db.Integer, primary_key=True)
    zeit = db.Column(db.String())
    kw = db.Column(db.String)
    verbraucherId = db.Column(db.Integer)
    isPrediction = db.Column(db.BOOLEAN)

    def __init__(self, zeit, kw, verbraucherId, isPrediction):
        self.zeit = zeit
        self.kw = kw
        self.verbraucherId = verbraucherId
        self.isPrediction = isPrediction

    def __repr__(self):
        return '<id {}>'.format(self.stromlastdatenId)

    def serialize(self):
        return {
            'stromlastdatenId': self.stromlastdatenId,
            'zeit': self.zeit,
            'kw': self.kw,
            'verbraucherId': self.verbraucherId,
            'isPrediction': self.isPrediction
        }


@app.route('/csv', methods=['POST'])
def import_csv():
    data = request.get_json()
    name: string = data['verbraucher']
    verbraucherId = 0
    try:
        verbraucher = Verbraucher(
            name=name
        )
        db.session.add(verbraucher)
        db.session.commit()
        print("Verbraucher added. verbraucher id={}".format(verbraucher.verbraucherId))
        verbraucherId = verbraucher.verbraucherId
        # return "Verbraucher added. book id={}".format(verbraucher.verbraucherId)
    except Exception as e:
        print(e)
        # return str(e)

    verbrauchsdaten = data['verbrauchsdaten']
    for datum in verbrauchsdaten:
        timing = datum['zeit']
        try:
            verbrauchsdatum = Stromlastdaten(
                zeit=datum['zeit'],
                kw=datum['kw'],
                verbraucherId=verbraucherId,
                isPrediction=False
            )
            db.session.add(verbrauchsdatum)
            db.session.commit()
            print("Stromlastdaten added. stromlastdatenId id={}".format(verbrauchsdatum.stromlastdatenId))
            # return "Verbraucher added. book id={}".format(verbraucher.verbraucherId)
        except Exception as e:
            print(e)
    return "Verbraucher und Stromlastdaten in DB gespeichert"


@app.route("/getallverbraucher", methods=['GET'])
def get_all_verbraucher():
    try:
        verbraucher = Verbraucher.query.all()
        return jsonify([e.serialize() for e in verbraucher])
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(port=os.environ.get('BACKEND_PORT'))
