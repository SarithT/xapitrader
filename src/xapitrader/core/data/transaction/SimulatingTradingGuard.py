import random
from typing import Dict
from xapitrader.types import types
from xapitrader.utils import logger
from xapitrader.core.data.transaction.Transaction import Transaction

class SimulatingTradingGuard():
    _transactions: Dict = {}

    @classmethod
    def open_transaction(self, client, trade_info: types.TRADE_TRANS_INFO):
        logger.Logger.info(f"Opening {trade_info.symbol} transaction with open price {str(trade_info.price)}")
        position = random.getrandbits(64)
        logger.Logger.info(f"Transaction {position} for {trade_info.symbol} opened with open price {str(trade_info.price)}")
        transaction = Transaction(position, trade_info)
        transaction.open()
        self._transactions[position] = transaction
        return position

    @classmethod
    def close_transaction(self, client, position:int, closePrice: float):
        if position not in self._transactions:
            raise Exception(f'Position {position} is not open, cannot be closed! Logic error!')
        transaction: Transaction = self._transactions[position]
        trade_info: types.TRADE_TRANS_INFO = transaction.getTradeInfo()
        logger.Logger.info(f"Closing {position} position for {trade_info.symbol} with close price {closePrice}")
        closing_trade_info = types.TRADE_TRANS_INFO(
            trade_info.cmd,
            trade_info.customComment,
            trade_info.expiration,
            trade_info.offset,
            position,
            closePrice,
            trade_info.sl,
            trade_info.symbol,
            trade_info.tp,
            types.TRANSACTION_TYPE.CLOSE,
            trade_info.volume)
        logger.Logger.info(f"Transaction {position} for {closing_trade_info.symbol} closed with close price {str(closing_trade_info.price)}")
        transaction.close(closePrice)
        del self._transactions[position]
        return True