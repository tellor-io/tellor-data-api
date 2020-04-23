from main import db
from sqlalchemy.dialects.postgresql import JSON, BYTEA
from sqlalchemy_serializer import SerializerMixin

class CustomSerializerMixin(SerializerMixin):
    serialize_types = (
        (bytes, lambda x: x.hex()),
    )

"""
The models mirror the events in the ABI

db.Numeric type is used for (u)int256 across the schema
to handle any overflows that might happen using db.Intger
"""

class EthereumBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    block_height = db.Column(db.Integer())
    mined_at = db.Column(db.DateTime)

class EthereumEvent(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    args = db.Column(JSON)
    event = db.Column(db.String(128))
    logIndex = db.Column(db.Integer())
    transactionIndex = db.Column(db.Integer())
    transactionHash = db.Column(db.String(68))
    address = db.Column(db.String(68))
    blockHash = db.Column(db.String(68))
    blockNumber = db.Column(db.String(64))

class NewDispute(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    disputeId = db.Column(db.Numeric())
    requestId = db.Column(db.Numeric())
    timestamp = db.Column(db.Numeric())
    miner = db.Column(db.String(64))
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

class Voted(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    disputeID = db.Column(db.Numeric())
    position = db.Column(db.Boolean())
    voter = db.Column(db.String(64))
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

class DisputeVoteTallied(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    disputeID = db.Column(db.Numeric())
    result = db.Column(db.Numeric())
    reportedMiner = db.Column(db.String(64))
    reportingParty = db.Column(db.String(64))
    active = db.Column(db.Boolean())
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

class NewTellorAddress(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    newTellor = db.Column(db.String(64))
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

class NewStake(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    sender = db.Column(db.String(64))
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

class StakeWithdrawn(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    sender = db.Column(db.String(64))
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

class StakeWithdrawRequested(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    sender = db.Column(db.String(64))
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

class Approval(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    owner = db.Column(db.String(64))
    spender = db.Column(db.String(64))
    value = db.Column(db.Numeric())
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

class Transfer(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    # NOTE: "from" is a reserve word in Python and Postgres
    fromAddress = db.Column(db.String(64))
    to = db.Column(db.String(64))
    value = db.Column(db.Numeric())
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

class TipAdded(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    sender = db.Column(db.String(64))
    requestId = db.Column(db.Numeric())
    tip = db.Column(db.Numeric())
    totalTips = db.Column(db.Numeric())
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

class DataRequested(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    sender = db.Column(db.String(64))
    query = db.Column(db.String(512))
    querySymbol = db.Column(db.String(32))
    granularity = db.Column(db.Numeric())
    requestId = db.Column(db.Numeric())
    totalTips = db.Column(db.Numeric())
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)


class NewChallenge(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    currentChallenge = db.Column(db.LargeBinary())
    currentRequestId = db.Column(db.Numeric())
    difficulty = db.Column(db.Numeric())
    multiplier = db.Column(db.Numeric())
    query = db.Column(db.String(512))
    totalTips = db.Column(db.Numeric())
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

class NewRequestOnDeck(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    requestId = db.Column(db.Numeric())
    query = db.Column(db.String(512))
    onDeckQueryHash = db.Column(db.LargeBinary())
    onDeckTotalTips = db.Column(db.Numeric())
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

class NewValue(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    requestId = db.Column(db.Numeric())
    time = db.Column(db.Numeric())
    value = db.Column(db.Numeric())
    totalTips = db.Column(db.Numeric())
    currentChallenge = db.Column(db.LargeBinary())
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

class NonceSubmitted(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    miner = db.Column(db.String(64))
    nonce = db.Column(db.String(128))
    requestId = db.Column(db.Numeric())
    value = db.Column(db.Numeric())
    currentChallenge = db.Column(db.LargeBinary())
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

# No API endpoints for these Ownership* models
class OwnershipTransferred(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    previousOwner = db.Column(db.String(64))
    newOwner = db.Column(db.String(64))
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)

class OwnershipProposed(db.Model, CustomSerializerMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    previousOwner = db.Column(db.String(64))
    newOwner = db.Column(db.String(64))
    ethereum_event_id = db.Column(db.Integer, db.ForeignKey('ethereum_event.id'), nullable=False)
