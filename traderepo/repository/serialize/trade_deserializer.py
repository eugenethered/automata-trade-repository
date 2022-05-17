from core.number.BigFloat import BigFloat
from core.trade.InstrumentTrade import InstrumentTrade, Status
from coreutility.collection.dictionary_utility import as_data
from coreutility.string.string_utility import is_empty


def deserialize_trade(trade) -> InstrumentTrade:
    instrument_from = as_data(trade, 'instrument_from')
    instrument_to = as_data(trade, 'instrument_to')
    quantity = BigFloat(as_data(trade, 'quantity'))
    price = as_data(trade, 'price')
    value = as_data(trade, 'value')
    status = as_data(trade, 'status')
    description = as_data(trade, 'description')
    order_id = as_data(trade, 'order_id')
    interval = as_data(trade, 'interval')
    deserialized_trade = InstrumentTrade(instrument_from, instrument_to, quantity)
    set_price_as_available(deserialized_trade, price)
    set_value_as_available(deserialized_trade, value)
    set_status_as_available(deserialized_trade, status)
    set_description_as_available(deserialized_trade, description)
    set_orderid_as_available(deserialized_trade, order_id)
    set_interval_as_available(deserialized_trade, interval)
    return deserialized_trade


def set_price_as_available(deserialized_trade, value):
    if not is_empty(value):
        deserialized_trade.price = BigFloat(value)


def set_value_as_available(deserialized_trade, value):
    if not is_empty(value):
        deserialized_trade.value = BigFloat(value)


def set_status_as_available(deserialized_trade, value):
    if value is not None:
        deserialized_trade.status = Status.parse(value)


def set_description_as_available(deserialized_trade, value):
    if not is_empty(value):
        deserialized_trade.description = value


def set_orderid_as_available(deserialized_trade, value):
    if not is_empty(value):
        deserialized_trade.order_id = value


def set_interval_as_available(deserialized_trade, value):
    if value is not None:
        deserialized_trade.interval = value
