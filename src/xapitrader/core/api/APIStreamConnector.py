from xapitrader.core.api.JsonSocket import JsonSocket
from xapitrader.core.api import settings
from threading import Thread
from xapitrader.utils import logger

def defaultErrFun(msg):
    pass

class APIStreamConnector(JsonSocket):
    def __init__(self, address=settings.DEFAULT_XAPI_ADDRESS, port=settings.DEFUALT_XAPI_STREAMING_PORT, encrypt=True, ssId=None, 
                 tickFun=None, tradeFun=None, candlesFun=None, balanceFun=None, tradeStatusFun=None, profitFun=None, newsFun=None, errorFun=defaultErrFun):
        super(APIStreamConnector, self).__init__(address, port, encrypt)
        self._ssId = ssId

        self._tickFun = tickFun
        self._tradeFun = tradeFun
        self._candlesFun = candlesFun
        self._balanceFun = balanceFun
        self._tradeStatusFun = tradeStatusFun
        self._profitFun = profitFun
        self._newsFun = newsFun
        self._errorFun = errorFun
        
        if(not self.connect()):
            raise Exception("Cannot connect to streaming on " + address + ":" + str(port) + " after " + str(settings.API_MAX_CONN_TRIES) + " retries")

        self._running = True
        self._t = Thread(target=self._readStream, args=())
        self._t.setDaemon(True)
        self._t.start()

    def _readStream(self):
        while (self._running):
            msg = self._readObj()
            logger.Logger.info("Stream received: " + str(msg))
            try:
                if (msg["command"]=='tickPrices'):
                    self._tickFun(msg)
                elif (msg["command"]=='trade'):
                    self._tradeFun(msg)
                elif (msg["command"]=='candle'):
                    self._candlesFun(msg)
                elif (msg["command"]=="balance"):
                    self._balanceFun(msg)
                elif (msg["command"]=="tradeStatus"):
                    self._tradeStatusFun(msg)
                elif (msg["command"]=="profit"):
                    self._profitFun(msg)
                elif (msg["command"]=="news"):
                    self._newsFun(msg)
            except KeyError:
                errorCode = msg['errorCode']
                errorDescr = msg['errorDescr']
                logger.Logger.error(f"{errorCode} - {errorDescr}")
                self._errorFun(msg)

    def disconnect(self):
        self._running = False
        self._t.join()
        self.close()

    def execute(self, dictionary):
        self._sendObj(dictionary)
    
    def set_tickFun(self, tickFun):
        self._tickFun = tickFun

    def set_candlesFun(self, candlesFun):
        self._candlesFun = candlesFun

    def set_tradeFun(self, tradeFun):
        self._tradeFun = tradeFun
    
    def set_balanceFun(self, balanceFun):
        self._balanceFun = balanceFun
    
    def set_tradeStatusFun(self, tradeStatusFun):
        self._tradeStatusFun = tradeStatusFun
    
    def set_profitFun(self, profitFun):
        self._profitFun = profitFun

    def set_newsFun(self, newsFun):
        self._newsFun = newsFun

    def set_errorFun(self, errorFun):
        self._errorFun = errorFun
