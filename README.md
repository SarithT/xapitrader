# xapitrader
Wrapper and set of tools which provides abstraction over most usefull methodes for algorythmic trading using xAPI Protocol used by XTB broker (https://www.xtb.com).
It follows official API documentation http://developers.xstore.pro/documentation and allows for real-time trading/informations exchange with your XTB account through JSON WebSockets.

# Installation
Project is on early stage development and it is not recommended to use it for making real transactions.
Currently it is rather supposed to be used for writing and testing algorythmic trading strategies based on real-live data.

Development-like installation is advised by following these steps:
1. create python virtualenv
2. clone the repository
3. install as local package for modification 'pip install -e xapitrader'

Basic application settings are defined in settings.py file. By default application logs and made transactions will be logged into files.

!WARNING!
Setting SIMULATION_MODE to 'False' will cause real trade transactions using your real money to be executed instead of 'fakes' one.

# Examples
You can find simple example with explenation in 'examples/bollingerBands.py' where basic strategy is implemented using xapitrader.
