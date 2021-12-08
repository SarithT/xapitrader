from typing import Dict
from xapitrader.types import types
from xapitrader.utils import logger
from xapitrader.core.data.retreive import commands
from xapitrader.core.data.transaction.Transaction import Transaction

class TradingGuard():
    """
    Helps to manage real transactions.
    It abstracts correct transaction process which includes opening, verifing and closing.
    Follows official xstore api tutorial:
    http://developers.xstore.pro/api/tutorials/opening_and_closing_trades2
    """

    _transactions: Dict = {}

    @classmethod
    def _verify_transaction(self, client, order) -> types.TRADE_TRANSACTION_STATUS:
        tradeTransactionStatus = commands.tradeTransactionStatus(client, order).call()
        while tradeTransactionStatus.requestStatus != types.REQUEST_STATUS.PENDING:
            tradeTransactionStatus = commands.tradeTransactionStatus(client, order).call()
        if tradeTransactionStatus.requestStatus != types.REQUEST_STATUS.ACCEPTED:
            raise Exception("Transaction {order} did not succeed!")
        return tradeTransactionStatus

    @classmethod
    def open_transaction(self, client, trade_info: types.TRADE_TRANS_INFO):
        """Opens and verifies real transaction"""
    
        logger.Logger.info(f"Opening {trade_info.symbol} transaction with open price {str(trade_info.price)}")
        order = commands.tradeTransaction(client, trade_info).call()
        tradeTransactionStatus = self._verify_transaction(client, order)
        tradeData = commands.getTrades(client, True).call()
        tradeRecordToClose = None
        for tradeRecord in tradeData:
            if tradeRecord.trade_record.order2 == tradeTransactionStatus.order:
                tradeRecordToClose = tradeRecord
                break
        position = tradeRecordToClose.trade_record.position
        logger.Logger.info(f"Transaction {position} for {trade_info.symbol} opened with open price {str(trade_info.price)}")
        transaction = Transaction(position, trade_info)
        transaction.open()
        self._transactions[position] = transaction
        return position

    @classmethod
    def close_transaction(self, client, position:int, closePrice: float):
        """Closing previously opened real transaction"""

        if position not in self._transactions:
            raise Exception(f'Position {position} is not open, cannot be closed! Logic error!')
        transaction: Transaction = self._transactions[position]
        trade_info: types.TRADE_TRANS_INFO = transaction.getTradeInfo()
        logger.Logger.info(f"Closing {position} position for {trade_info.symbol} with close price {closePrice}")
        trade_info.type = types.TRANSACTION_TYPE.CLOSE
        trade_info.price = closePrice
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
        order = commands.tradeTransaction(client, closing_trade_info).call()
        tradeTransactionStatus = self._verify_transaction(client, order)
        logger.Logger.info(f"Transaction {position} for {closing_trade_info.symbol} closed with close price {str(closing_trade_info.price)}")
        transaction.close(closePrice)
        del self._transactions[position]
        return True
