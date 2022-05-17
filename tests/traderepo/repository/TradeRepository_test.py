import unittest

from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.number.BigFloat import BigFloat
from core.trade.InstrumentTrade import InstrumentTrade, Status

from traderepo.repository.TradeRepository import TradeRepository


class TradeRepositoryTestCase(unittest.TestCase):

    def setUp(self) -> None:
        options = {
            'REDIS_SERVER_ADDRESS': '192.168.1.90',
            'REDIS_SERVER_PORT': 6379,
            'TRADE_KEY': 'test:trade'
        }
        self.cache = RedisCacheHolder(options)
        self.repository = TradeRepository(options)

    def tearDown(self):
        self.cache.delete('test:trade')
        self.cache.delete('test:trade:history')

    def test_should_store_and_retrieve_trade(self):
        trade = InstrumentTrade(instrument_from='OTC', instrument_to='GBP', quantity=BigFloat('100.00'), price=BigFloat('1.01'), value=BigFloat('101'), status=Status.SUBMITTED, order_id='8888-8888', instant=1)
        self.repository.store_trade(trade)
        stored_trade = self.repository.retrieve_trade()
        self.assertEqual(trade, stored_trade)

    def test_should_store_executed_trade_on_historic_trades_list(self):
        historic_trades = self.repository.retrieve_historic_trades()
        self.assertTrue(len(historic_trades) == 0)
        trade = InstrumentTrade(instrument_from='OTC', instrument_to='GBP', quantity=BigFloat('100.00'), price=BigFloat('1.01'), value=BigFloat('101'), status=Status.EXECUTED, order_id='8888-8888', instant=1)
        self.repository.store_trade(trade)
        historic_trades = self.repository.retrieve_historic_trades()
        self.assertTrue(len(historic_trades) == 1)

    def test_should_not_store_non_executed_trade_on_historic_trades_list(self):
        historic_trades = self.repository.retrieve_historic_trades()
        self.assertTrue(len(historic_trades) == 0)
        trade = InstrumentTrade(instrument_from='OTC', instrument_to='GBP', quantity=BigFloat('100.00'), price=BigFloat('1.01'), value=BigFloat('101'), status=Status.SUBMITTED, order_id='8888-8888', instant=1)
        self.repository.store_trade(trade)
        historic_trades = self.repository.retrieve_historic_trades()
        self.assertTrue(len(historic_trades) == 0)

    def test_should_not_store_trade_without_order_id_on_historic_trades_list(self):
        historic_trades = self.repository.retrieve_historic_trades()
        self.assertTrue(len(historic_trades) == 0)
        trade = InstrumentTrade(instrument_from='OTC', instrument_to='GBP', quantity=BigFloat('100.00'), price=BigFloat('1.01'), value=BigFloat('101'), status=Status.EXECUTED, instant=1)
        self.repository.store_trade(trade)
        historic_trades = self.repository.retrieve_historic_trades()
        self.assertTrue(len(historic_trades) == 0)

    def test_should_not_store_same_executed_trade_on_historic_trades_list(self):
        trade = InstrumentTrade(instrument_from='OTC', instrument_to='GBP', quantity=BigFloat('100.00'), price=BigFloat('1.01'), value=BigFloat('101'), status=Status.EXECUTED, order_id='8888-8888', instant=1)
        self.repository.store_trade(trade)
        historic_trades = self.repository.retrieve_historic_trades()
        self.assertTrue(len(historic_trades) == 1)
        # try string the same trade again (based on equality) in history
        other = InstrumentTrade(instrument_from='OTC', instrument_to='GBP', quantity=BigFloat('200.00'), price=BigFloat('2.02'), value=BigFloat('404'), status=Status.EXECUTED, order_id='8888-8888', instant=1)
        self.repository.store_trade(other)
        historic_trades = self.repository.retrieve_historic_trades()
        self.assertTrue(len(historic_trades) == 1)


if __name__ == '__main__':
    unittest.main()
