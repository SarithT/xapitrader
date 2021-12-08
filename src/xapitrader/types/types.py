from typing import NamedTuple
from typing import List

class CMD(object):
    BUY = 0
    SELL = 1
    BUY_LIMIT = 2
    SELL_LIMIT = 3
    BUY_STOP = 4
    SELL_STOP = 5
    BALANCE = 6
    CREDIT = 7

class PERIOD(object):
    PERIOD_M1 = 1
    PERIOD_M5 = 5
    PERIOD_M15 = 15
    PERIOD_M30 = 30
    PERIOD_H1 = 60
    PERIOD_H4 = 240
    PERIOD_D1 = 1440
    PERIOD_W1 = 10080
    PERIOD_MN1 = 43200

class TRANSACTION_TYPE(object):
    OPEN = 0
    PENDING = 1
    CLOSE = 2
    MODIFY = 3
    DELETE = 4

class Level(object):
    BASE = -1
    ALL = 0

class State(object):
    MODIFIED = "Modified"
    DELETED = "Deleted"

class QuoteId(object):
    fixed = 1
    float = 2
    depth = 3
    cross = 4

class MarginMode(object):
    Forex = 101
    CFD_leveraged = 102
    CFD = 103

class ProfitMode(object):
    FOREX = 5
    CFD = 6

class STREAMING_BALANCE_RECORD(NamedTuple):
    balance: float
    credit: float
    equity: float
    margin: float
    marginFree: float
    marginLevel: float

class STREAMING_NEWS_RECORD(NamedTuple):
    body: str
    key: str
    time: float
    title: str

class STREAMING_PROFIT_RECORD(NamedTuple):
    order: int
    order2: int
    position: int
    profit: float

class TRADE_RECORD(NamedTuple):
    close_price: float
    close_time: float
    closed: bool
    cmd: CMD
    comment: str
    commission: float
    customComment: str
    digits: int
    expiration: int
    margin_rate: float
    offset: int
    open_price: float
    open_time: int
    order: int
    order2: int
    position: int
    profit: float
    sl: float
    state: State
    storage: float
    symbol: str
    tp: float
    volume: float

class STREAMING_TRADE_RECORD(NamedTuple):
    trade_record: TRADE_RECORD
    type: TRANSACTION_TYPE

class GET_TRADE_RECORD(NamedTuple):
    trade_record: TRADE_RECORD
    expirationString: str
    open_timeString: str

class SYMBOL_RECORD(NamedTuple):
    ask: float
    bid: float
    categoryName: str
    contractSize: int
    currency: str
    currencyPair: bool
    currencyProfit: str
    description: str
    exemode: int
    expiration: int
    groupName: str
    high: float
    initialMargin: int
    instantMaxVolume: int
    leverage: float
    longOnly: bool
    lotMax: float
    lotMin: float
    lotStep: float
    low: float
    marginHedged: int
    marginHedgedStrong: bool
    marginMaintenance: int
    marginMode: MarginMode
    percentage: float
    pipsPrecision: int
    precision: int
    profitMode: ProfitMode
    quoteId: QuoteId
    quoteIdCross: int
    shortSelling: bool
    spreadRaw: float
    spreadTable: float
    starting: int
    stepRuleId: int
    stopsLevel: int
    swap_rollover3days: int
    swapEnable: bool
    swapLong: float
    swapShort: float
    swapType: int
    symbol: str
    tickSize: float
    tickValue: float
    time: float
    timeString: str
    trailingEnabled: bool
    type: int

class RATE_INFO_RECORD(NamedTuple):
    close: float
    ctm: int
    ctmString: str
    high: float
    low: float
    open: float
    vol: float

class STREAMING_CANDLE_RECORD(NamedTuple):
    rate_info_record: RATE_INFO_RECORD
    quoteId: float
    symbol: float

class TICK_RECORD(NamedTuple):
    ask: float
    askVolume: int
    bid: float
    bidVolume: int
    high: float
    level: int
    low: float
    spreadRaw: float
    spreadTable: float
    symbol: float
    timestamp: int

class DAY(object):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7

class QUOTES_RECORD(NamedTuple):
    day: DAY
    fromT: int
    toT: int

class TRADING_RECORD(NamedTuple):
    day: DAY
    fromT: int
    toT: int

class TRADING_HOURS_RECORD(NamedTuple):
    quotes: List[QUOTES_RECORD]
    symbol: str
    trading: List[TRADING_RECORD]

class REQUEST_STATUS(NamedTuple):
    ERROR = 0
    PENDING = 1
    ACCEPTED = 3
    REJECTED = 4

class TRADE_TRANSACTION_STATUS(NamedTuple):
    ask: float
    bid: float
    customComment: str
    message: str
    order: int
    requestStatus: REQUEST_STATUS

class TRADE_TRANS_INFO(NamedTuple):
    cmd: CMD
    customComment: str
    expiration: int
    offset: int
    order: int
    price: float
    sl: float
    symbol: str
    tp: float
    type: TRANSACTION_TYPE
    volume: float
