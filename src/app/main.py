from os import environ
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from config import DevelopmentConfig, ProductionConfig
from time import sleep

FLASK_ENV = environ.get("FLASK_ENV", "local")

app = Flask(__name__)

if FLASK_ENV == "development":
    app.config.from_object(DevelopmentConfig)
elif FLASK_ENV == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

auth = HTTPBasicAuth()

users = {
    app.config["BACKEND_USERNAME"]: generate_password_hash(app.config["BACKEND_PASSWORD"])
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from models import EthereumEvent, NewDispute, Voted, DisputeVoteTallied, NewTellorAddress,\
                   NewStake, StakeWithdrawn, StakeWithdrawRequested, Approval,\
                   Transfer, TipAdded, DataRequested, NewChallenge, NewRequestOnDeck,\
                   NewValue, NonceSubmitted, OwnershipTransferred, OwnershipProposed
from monitor import check

def to_list(records):
    return [r.to_dict(rules=('-id','-ethereum_event_id',)) for r in records]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update')
@auth.login_required
def update():
    from_block, to_block = check(db)
    return "Updated database with events from {0} to {1}".format(from_block, to_block)

@app.route('/api/newDispute')
def disputes():
    disputes = db.session.query(NewDispute)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(disputes))

@app.route('/api/voted')
def voted():
    voted = db.session.query(Voted)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(voted))

@app.route('/api/disputeVoteTallied')
def disputeVoteTallied():
    disputeVoteTallied = db.session.query(DisputeVoteTallied)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(disputeVoteTallied))

@app.route('/api/newTellorAddress')
def newTellorAddress():
    newTellorAddresses = db.session.query(NewTellorAddress)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(newTellorAddresses))

@app.route('/api/newStake')
def newStake():
    newStakes = db.session.query(NewStake)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(newStakes))

@app.route('/api/stakeWithdrawn')
def stakeWithdrawn():
    stakeWithdrawn = db.session.query(StakeWithdrawn)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(stakeWithdrawn))

@app.route('/api/stakeWithdrawnRequested')
def stakeWithdrawnRequested():
    stakeWithdrawnRequested = db.session.query(StakeWithdrawRequested)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(stakeWithdrawnRequested))

@app.route('/api/approval')
def approvals():
    approvals = db.session.query(Approval)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(approvals))

@app.route('/api/transfer')
def transfers():
    transfers = db.session.query(Transfer)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(transfers))

@app.route('/api/tipAdded')
def tipAdded():
    tipAdded = db.session.query(TipAdded)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(tipAdded))

@app.route('/api/dataRequested')
def dataRequested():
    dataRequested = db.session.query(DataRequested)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(dataRequested))

@app.route('/api/newChallenge')
def newChallenge():
    newChallenges = db.session.query(NewChallenge)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(newChallenges))

@app.route('/api/newRequestOnDeck')
def newRequestOnDeck():
    newRequestOnDeck = db.session.query(NewRequestOnDeck)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(newRequestOnDeck))

@app.route('/api/newValue')
def newValue():
    newValue = db.session.query(newValue)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(newValue))

@app.route('/api/nonceSubmitted')
def nonceSubmitted():
    nonceSubmitted = db.session.query(NonceSubmitted)\
                          .join(EthereumEvent)\
                          .order_by(EthereumEvent.blockNumber.desc())\
                          .limit(100)\
                          .all()
    return jsonify(to_list(nonceSubmitted))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0')
