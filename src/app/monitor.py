import models
from copy import deepcopy
from functools import partial
from eth_abi.exceptions import DecodingError
from eth_utils import event_abi_to_log_topic
from web3.auto import w3
from web3._utils.events import get_event_data
from json import loads, dumps
from os import environ
import re
from sqlalchemy.orm.exc import NoResultFound
from tellor import TELLOR_ABI_JSON
from datetime import datetime

# WEB3_PROVIDER_URI required
TELLOR_ADDRESS = environ.get("TELLOR_ADDRESS", "0x0Ba45A8b5d5575935B8158a88C631E9F9C95a2e5")
TELLOR_GENESIS_BLOCK = environ.get("TELLOR_GENESIS_BLOCK", 8265522)
BLOCK_RANGE_MAX = int(environ.get("BLOCK_RANGE_MAX", 50))
MODE = environ.get("MODE", "monitor")

def check(db):
    """
    Get the last block checked and the current block
    """
    last_block = db.session.query(models.EthereumBlock)\
                           .order_by(models.EthereumBlock.block_height.desc())\
                           .first()
    if last_block:
        last_block = last_block.block_height
    else:
        last_block = TELLOR_GENESIS_BLOCK - 1

    current_block = w3.eth.blockNumber

    if current_block - last_block > BLOCK_RANGE_MAX:
        current_block = last_block + BLOCK_RANGE_MAX
        print("Difference between last and current block too large")
        print("Taking incremental step from {0} to {1}".format(last_block, current_block))

    block_data = w3.eth.getBlock(current_block)
    if not block_data:
        print("Block data not available yet.")
        return

    if last_block < current_block:
        print("Scanning and saving events from {0} to {1}".format(last_block, current_block))
        scan_and_save(last_block + 1, current_block, db)
        mined_at = datetime.fromtimestamp(block_data.timestamp)
        eth_block = models.EthereumBlock(block_height=current_block, mined_at=mined_at)
        db.session.add(eth_block)
        db.session.commit()
        return last_block + 1, current_block

def scan_and_save(from_block, to_block, db):
    events = _load_contract_events(from_block, to_block)
    print("Found Events: ", len(events))
    for event in events:
        # print(event["args"])
        # print(event)
        try:
            args = dumps(dict(event["args"]))
        except TypeError:
            args = {}
            for key, value in event["args"].items():
                # NOTE: Cleans "nonce" submissions to fit into postgres as strings
                pattern = re.compile('[\W_]+', re.UNICODE)
                if isinstance(value, bytes):
                    args[key] = pattern.sub('', value.hex())
                elif isinstance(value, str):
                    args[key] = pattern.sub('',value.replace("\\","\\\\"))
                else:
                    args[key] = value

            args = dumps(args)
        _event = {}
        for key, value in event.items():
            if key != "args":
                _event[key] = value
            else:
                _event[key] = args
        _event = models.EthereumEvent(**_event)
        # print(_event)
        db.session.add(_event)
        db.session.commit()
        record = _transform_event(event, loads(_event.args))
        record.ethereum_event_id = _event.id
        db.session.add(record)
        db.session.commit()


def _transform_event(event, args):
    # Convert event name to class
    cls = eval("models." + event["event"])
    # Convert params to kwargs
    args_dict = {}
    for key, value in event["args"].items():
        if key == '_from':
            args_dict["fromAddress"] = value
        elif key == '_nonce': # Patch for bytes nonce
            args_dict["nonce"] = args["_nonce"]
        else:
            args_dict[key.replace("_","")] = value

    record = cls(**args_dict)
    return record


def _load_contract_events(from_block, to_block):
    decoders = _get_log_decoders(loads(TELLOR_ABI_JSON))
    logs = w3.eth.getLogs({
        'address': TELLOR_ADDRESS,
        'fromBlock': int(from_block),
        'toBlock': int(to_block)
    })
    # print("Getting all events from filter", from_block, to_block)
    # print(logs)
    # event_logs = event_filter.get_all_entries()
    return _decode_logs(logs, decoders)


def _get_log_decoders(contract_abi):
    """
    Source: banteg/tellor
    """
    decoders = {
        event_abi_to_log_topic(abi): partial(get_event_data, w3.codec, abi)
        for abi in contract_abi if abi['type'] == 'event'
    }
    # fix for byte nonce in events
    nonce_string_abi = next(x for x in contract_abi if x.get('name') == 'NonceSubmitted')
    nonce_string_topic = event_abi_to_log_topic(nonce_string_abi)
    nonce_bytes_abi = deepcopy(nonce_string_abi)
    nonce_bytes_abi['inputs'][1]['type'] = 'bytes'
    decoders[nonce_string_topic] = partial(_decode_log_with_fallback, [nonce_string_abi, nonce_bytes_abi])
    return decoders


def _decode_log_with_fallback(abis_to_try, log):
    """
    Source: banteg/tellor
    """
    for abi in abis_to_try:
        try:
            log_with_replaced_topic = deepcopy(log)
            log_with_replaced_topic['topics'][0] = event_abi_to_log_topic(abi)
            return get_event_data(w3.codec, abi, log_with_replaced_topic)
        except DecodingError:
            print('trying fallback log decoder')
    raise DecodingError('could not decode log')


def _decode_logs(logs, decoders):
    """
    Source: banteg/tellor
    """
    result = []
    for log in logs:
        topic = log['topics'][0]
        if topic in decoders:
            try:
                decoded = decoders[topic](log)
                result.append(decoded)
            except DecodingError as e:
                print('could not decode log')
                print(log)
                print(e)
    return result
