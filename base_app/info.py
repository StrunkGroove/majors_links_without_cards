import redis

key_binance = 'binance'
key_huobi = 'huobi'
key_kucoin = 'kucoin'
key_okx = 'okx'
key_bybit = 'bybit'
key_mexc = 'mexc'
key_bitget = 'bitget'
key_pancake = 'pancake'
key_gateio = 'gateio'
key_best_rates = 'rates'

rc = redis.StrictRedis(
    host='188.120.226.254',
    port=6379,
    db=0,
    password='i8Ini9zGEJFp',
    decode_responses=True
)

crypto_list = [
    'USDT',
    'BNB',
    'SOL',
    'BTC',
    'LTC',
    'USDC',
    'DOGE',
    'ETH',
    'DASH',
    'XMR',
    'ETC',
    'XRP',
    'BCH',
    'TRX',
    'DAI',
    'BUSD',
    'BTCB',
    'WBTC',
    'BSV',
    'BTG',
    'WETH',
    'MATIC',
    'ZEC',
    'EURT',
    'USDP',
    'XEM',
    'NEO',
    'EOS',
    'MIOTA',
    'ADA',
    'XML',
    'WAVES',
    'OMG',
    'XVG',
    'ZRX',
    'ICX',
    'KMD',
    'BTT',
    'BAT',
    'ONT',
    'QTUM',
    'LINK',
    'ATOM',
    'XTZ',
    'DOT',
    'UNI',
    'RVN',
    'VET',
    'SHIB',
    'ALGO',
    'MKR',
    'AVAX',
    'YFI',
    'MANA',
    'LUNA',
    'NEAR',
    'CRO',
    'TON',
    'CAKE',
]


accept_list_binance = [
    # USDT 
    'USDTBNB',
    'USDTSOL',
    'USDTBTC',
    'USDTLTC',
    'USDTUSDT',
    'USDTDOGE',
    'USDTETH',
    'USDTDASH',
    'USDTXMR',
    'USDTETC',
    'USDTXRP',
    'USDTBCH',
    'USDTTRX',
    'USDTDAI',
    'USDTBUSD',
    'USDTWBTC',
    'USDTMATIC',
    'USDTZEC',
    'USDTUSDPLUS',
    'USDTXEM',
    'USDTNEO',
    'USDTEOS',
    'USDTMIOTA',
    'USDTADA',
    'USDTWAVES',
    'USDTOMG',
    'USDTXVG',
    'USDTZRX',
    'USDTICX',
    'USDTKMD',
    'USDTBAT',
    'USDTONT',
    'USDTQTUM',
    'USDTLINK',
    'USDTATOM',
    'USDTXTZ',
    'USDTDOT',
    'USDTUNI',
    'USDTRVN',
    'USDTVET',
    'USDTSHIB',
    'USDTALGO',
    'USDTMKR',
    'USDTAVAX',
    'USDTYFI',
    'USDTMANA',
    'USDTLUNA',
    'USDTNEAR',
    'USDTCAKE',

    'BNBUSDT',
    'SOLUSDT',
    'BTCUSDT',
    'LTCUSDT',
    'USDTUSDT',
    'DOGEUSDT',
    'ETHUSDT',
    'DASHUSDT',
    'XMRUSDT',
    'ETCUSDT',
    'XRPUSDT',
    'BCHUSDT',
    'TRXUSDT',
    'DAIUSDT',
    'BUSDUSDT',
    'WBTCUSDT',
    'MATICUSDT',
    'ZECUSDT',
    'USDPLUSDT',
    'XEMUSDT',
    'NEOUSDT',
    'EOSUSDT',
    'MIOTAUSDT',
    'ADAUSDT',
    'WAVESUSDT',
    'OMGUSDT',
    'XVGUSDT',
    'ZRXUSDT',
    'ICXUSDT',
    'KMDUSDT',
    'BATUSDT',
    'ONTUSDT',
    'QTUMUSDT',
    'LINKUSDT',
    'ATOMUSDT',
    'XTZUSDT',
    'DOTUSDT',
    'UNIUSDT',
    'RVNUSDT',
    'VETUSDT',
    'SHIBUSDT',
    'ALGOUSDT',
    'MKRUSDT',
    'AVAXUSDT',
    'YFIUSDT',
    'MANAUSDT',
    'LUNAUSDT',
    'NEARUSDT',
    'CAKEUSDT',

    # USDC
    'BNBUSDC',
    'BTCUSDC',
    'ETHUSDC',
    'USDTUSDC',

    'USDCBNB',
    'USDCBTC',
    'USDCETH',
    'USDCUSDT',
]
ban_list_binance = [
    'DAIUSDT',
    'BTGUSDT',

    # USDC
    'USDCDOGE',
    'DOGEUSDC',
    'BTTUSDC',
    'USDCBTT',
    'ETCUSDC',
    'USDCETC',
    'BCHUSDC',
    'USDCBCH',
    'TRXUSDC',
    'USDCTRX',
    'WAVESUSDC',
    'USDCWAVES',
    'LTCUSDC',
    'USDCLTC',
    'XMRUSDC',
    'USDCXMR',
    'XRPUSDC',
    'USDCXRP',
    'LINKUSDC',
    'USDCLINK',
    'USDCBUSD',
    'BUSDUSDC',
    'USDCSOL',
    'SOLUSDC',
    'USDCADA',
    'ADAUSDC',
    'USDCATOM',
    'ATOMUSDC',
    'USDCEOS',
    'EOSUSDC',
    'USDCZEC',
    'ZECUSDC',
    'USDCALGO',
    'ALGOUSDC',
    'USDCONT',
    'ONTUSDC',
    'USDCBAT',
    'BATUSDC',
    'USDCNEO',
    'NEOUSDC',
    # USDC

    'BTGBTC',
    'BTCBTG',

    'DAIBTC',
    'XEMBTC',

    'USDCBNB',
    'DAIBNB',
    'XEMBNB', 

    'BTTUSDT',
    'USDTBTT',
    'BTTTUSD',
    'TUSDBTT',
    'BTTBTC',
    'BTCBTT',
    'BTTBNB',
    'BNBBTT',

    'BNBMANA',
    'MANABNB',
    'BNBDASH',
    'DASHBNB',

    'BNBLUNA',
    'LUNABNB',
    'BTCLUNA',
    'LUNABTC',

    'XVGBTC',
    'BTCXVG',
    'BNBXVG',
    'XVGBNB',

    'OMGBNB',
    'BNBOMG',
    'BTCOMG',
    'OMGBTC',
    
    'ZRXBNB',
    'BNBZRX',

    'QTUMBNB',
    'BNBQTUM',

    'ICXBNB',
    'BNBICX',

    'YFIBNB',
    'BNBYFI',

    'ONTBNB',
    'BNBONT',

    'BNBDOGE',
    'DOGEBNB',

    'WAVESBNB',
    'BNBWAVES',

    'BNBZEC',
    'ZECBNB',

    'BNBUSDP',
    'USDPBNB',
    'BTCUSDP',
    'USDPBTC',
    'TUSDUSDP',
    'USDPTUSD',

    'BNBXTZ',
    'XTZBNB',

    'BATBNB',
    'BNBBAT',

    'MKRBNB',
    'BNBMKR',
]


accept_list_bybit = [
    # USDT
    'BNBUSDT',
    'SOLUSDT',
    'BTCUSDT',
    'LTCUSDT',
    'USDTUSDT',
    'DOGEUSDT',
    'ETHUSDT',
    'ETCUSDT',
    'XRPUSDT',
    'BCHUSDT',
    'TRXUSDT',
    'DAIUSDT',
    'BUSDUSDT',
    'WBTCUSDT',
    'BTGUSDT',
    'MATICUSDT',
    'XEMUSDT',
    'EOSUSDT',
    'ADAUSDT',
    'WAVESUSDT',
    'OMGUSDT',
    'ZRXUSDT',
    'ICXUSDT',
    'BTTUSDT',
    'BATUSDT',
    'QTUMUSDT',
    'LINKUSDT',
    'ATOMUSDT',
    'XTZUSDT',
    'DOTUSDT',
    'UNIUSDT',
    'RVNUSDT',
    'SHIBUSDT',
    'ALGOUSDT',
    'MKRUSDT',
    'AVAXUSDT',
    'YFIUSDT',
    'MANAUSDT',
    'LUNAUSDT',
    'NEARUSDT',
    'TONUSDT',
    'CAKEUSDT',

    'USDTBNB',
    'USDTSOL',
    'USDTBTC',
    'USDTLTC',
    'USDTUSDT',
    'USDTDOGE',
    'USDTETH',
    'USDTETC',
    'USDTXRP',
    'USDTBCH',
    'USDTTRX',
    'USDTDAI',
    'USDTBUSD',
    'USDTWBTC',
    'USDTBTG',
    'USDTMATIC',
    'USDTXEM',
    'USDTEOS',
    'USDTADA',
    'USDTWAVES',
    'USDTOMG',
    'USDTZRX',
    'USDTICX',
    'USDTBTT',
    'USDTBAT',
    'USDTQTUM',
    'USDTLINK',
    'USDTATOM',
    'USDTXTZ',
    'USDTDOT',
    'USDTUNI',
    'USDTRVN',
    'USDTSHIB',
    'USDTALGO',
    'USDTMKR',
    'USDTAVAX',
    'USDTYFI',
    'USDTMANA',
    'USDTLUNA',
    'USDTNEAR',
    'USDTTON',
    'USDTCAKE',

    # USDC
    'SOLUSDC',
    'BTCUSDC',
    'LTCUSDC',
    'USDTUSDC',
    'DOGEUSDC',
    'ETHUSDC',
    'XRPUSDC',
    'TRXUSDC',
    'MATICUSDC',
    'EOSUSDC',
    'ADAUSDC',
    'LINKUSDC',
    'DOTUSDC',
    'SHIBUSDC',
    'AVAXUSDC',
    'MANAUSDC',

    'USDCSOL',
    'USDCBTC',
    'USDCLTC',
    'USDCUSDT',
    'USDCDOGE',
    'USDCETH',
    'USDCXRP',
    'USDCTRX',
    'USDCMATIC',
    'USDCEOS',
    'USDCADA',
    'USDCINK',
    'USDCDOT',
    'USDCSHIB',
    'USDCAVAX',
    'USDCMANA',
]
ban_list_bybit = [
    'ZECUSDT',
    'USDTZEC',
    'DASHUSDT',
    'USDTDASH',
]


accept_list_huobi = [
    # USDT
    'bnbusdt',
    'solusdt',
    'btcusdt',
    'ltcusdt',
    'usdtusdt',
    'dogeusdt',
    'ethusdt',
    'dashusdt',
    'xmrusdt',
    'etcusdt',
    'xrpusdt',
    'bchusdt',
    'trusdt',
    'daiusdt',
    'bsvusdt',
    'zecusdt',
    'eurtusdt',
    'usdplusdt',
    'xemusdt',
    'neousdt',
    'eosusdt',
    'miotausdt',
    'adausdt',
    'wavesusdt',
    'omgusdt',
    'xvgusdt',
    'zrxusdt',
    'icusdt',
    'kmdusdt',
    'bttusdt',
    'batusdt',
    'ontusdt',
    'qtumusdt',
    'linkusdt',
    'atomusdt',
    'xtzusdt',
    'dotusdt',
    'uniusdt',
    'rvnusdt',
    'vetusdt',
    'shibusdt',
    'algousdt',
    'mkrusdt',
    'avaxusdt',
    'yfiusdt',
    'manausdt',
    'lunausdt',
    'nearusdt',
    'tonusdt',
    'cakeusdt',

    'usdtbnb',
    'usdtsol',
    'usdtbtc',
    'usdtltc',
    'usdtusdt',
    'usdtdoge',
    'usdteth',
    'usdtdash',
    'usdtxmr',
    'usdtetc',
    'usdtxrp',
    'usdtbch',
    'usdttrx',
    'usdtdai',
    'usdtbsv',
    'usdtzec',
    'usdteurt',
    'usdtpusd',
    'usdtxem',
    'usdtneo',
    'usdteos',
    'usdtmiota',
    'usdtada',
    'usdtwaves',
    'usdtomg',
    'usdtxvg',
    'usdtzrx',
    'usdticx',
    'usdtkmd',
    'usdtbtt',
    'usdtbat',
    'usdtonnt',
    'usdtqtum',
    'usdtlink',
    'usdtatom',
    'usdtxtz',
    'usdtdot',
    'usdtuni',
    'usdtrvn',
    'usdtvet',
    'usdtshib',
    'usdtalgo',
    'usdtmkr',
    'usdtavax',
    'usdtyfi',
    'usdtmana',
    'usdtluna',
    'usdtnear',
    'usdtton',
    'usdtcake',

    # USDC
    'btcusdc',
    'usdtusdc',
    'ethusdc',
    'bttusdc',

    'usdcbtc',
    'usdcusdt',
    'usdceth',
    'usdcbtt',
]
ban_list_huobi = []


accept_list_kucoin = [
    # USDT 
    'BNB-USDT',
    'SOL-USDT',
    'BTC-USDT',
    'LTC-USDT',
    'USDT-USDT',
    'DOGE-USDT',
    'ETH-USDT',
    'DASH-USDT',
    'XMR-USDT',
    'ETC-USDT',
    'XRP-USDT',
    'BCH-USDT',
    'TRX-USDT',
    'BUSD-USDT',
    'BSV-USDT',
    'MATIC-USDT',
    'ZEC-USDT',
    'USDPLUSDT',
    'XEM-USDT',
    'NEO-USDT',
    'EOS-USDT',
    'ADA-USDT',
    'WAVES-USDT',
    'OMG-USDT',
    'ICX-USDT',
    'KMD-USDT',
    'BTT-USDT',
    'BAT-USDT',
    'ONT-USDT',
    'LINK-USDT',
    'ATOM-USDT',
    'XTZ-USDT',
    'DOT-USDT',
    'UNI-USDT',
    'RVN-USDT',
    'VET-USDT',
    'SHIB-USDT',
    'ALGO-USDT',
    'MKR-USDT',
    'AVAX-USDT',
    'YFI-USDT',
    'MANA-USDT',
    'LUNA-USDT',
    'NEAR-USDT',
    'CRO-USDT',
    'TON-USDT',
    'CAKE-USDT',

    'USDT-BNB',
    'USDT-SOL',
    'USDT-BTC',
    'USDT-LTC',
    'USDT-USDT',
    'USDT-DOGE',
    'USDT-ETH',
    'USDT-DASH',
    'USDT-XMR',
    'USDT-ETC',
    'USDT-XRP',
    'USDT-BCH',
    'USDT-TRX',
    'USDT-BUSD',
    'USDT-BSV',
    'USDT-MATIC',
    'USDT-ZEC',
    'USDT-XEM',
    'USDT-NEO',
    'USDT-EOS',
    'USDT-ADA',
    'USDT-WAVES',
    'USDT-OMG',
    'USDT-ICX',
    'USDT-KMD',
    'USDT-BTT',
    'USDT-BAT',
    'USDT-ONT',
    'USDT-LINK',
    'USDT-ATOM',
    'USDT-XTZ',
    'USDT-DOT',
    'USDT-UNI',
    'USDT-RVN',
    'USDT-VET',
    'USDT-SHIB',
    'USDT-ALGO',
    'USDT-MKR',
    'USDT-AVAX',
    'USDT-YFI',
    'USDT-MANA',
    'USDT-LUNA',
    'USDT-NEAR',
    'USDT-CRO',
    'USDT-TON',
    'USDT-CAKE',

    # USDC
    'BNB-USDC',
    'SOL-USDC',
    'BTC-USDC',
    'LTC-USDC',
    'USDT-USDC',
    'DOGE-USDC',
    'ETH-USDC',
    'ETC-USDC',
    'XRP-USDC',
    'BCH-USDC',
    'TRX-USDC',
    'BUSD-USDC',
    'BSV-USDC',
    'MATIC-USDC',
    'EOS-USDC',
    'ADA-USDC',
    'LINK-USDC',
    'ATOM-USDC',
    'DOT-USDC',
    'SHIB-USDC',
    'ALGO-USDC',
    'AVAX-USDC',
    'LUNA-USDC',
    'NEAR-USDC',

    'USDC-BNB',
    'USDC-SOL',
    'USDC-BTC',
    'USDC-LTC',
    'USDC-USDT',
    'USDC-DOGE',
    'USDC-ETH',
    'USDC-ETC',
    'USDC-XRP',
    'USDC-BCH',
    'USDC-TRX',
    'USDC-BUSD',
    'USDC-BSV',
    'USDC-MATIC',
    'USDC-EOS',
    'USDC-ADA',
    'USDC-LINK',
    'USDC-ATOM',
    'USDC-DOT',
    'USDC-SHIB',
    'USDC-ALGO',
    'USDC-AVAX',
    'USDC-LUNA',
    'USDC-NEAR',
]
ban_list_kucoin = []


accept_list_okx = [
    # USDT
    'BNBUSDT',
    'SOLUSDT',
    'BTCUSDT',
    'LTCUSDT',
    'USDTUSDT',
    'DOGEUSDT',
    'ETHUSDT',
    'DASHUSDT',
    'XMRUSDT',
    'ETCUSDT',
    'XRPUSDT',
    'BCHUSDT',
    'TRXUSDT',
    'DAIUSDT',
    'BTCBUSDT',
    'WBTCUSDT',
    'BSVUSDT',
    'BTGUSDT',
    'MATICUSDT',
    'ZECUSDT',
    'EURTUSDT',
    'XEMUSDT',
    'NEOUSDT',
    'EOSUSDT',
    'ADAUSDT',
    'WAVESUSDT',
    'OMGUSDT',
    'ZRXUSDT',
    'ICXUSDT',
    'BTTUSDT',
    'BATUSDT',
    'ONTUSDT',
    'QTUMUSDT',
    'LINKUSDT',
    'ATOMUSDT',
    'XTZUSDT',
    'DOTUSDT',
    'UNIUSDT',
    'RVNUSDT',
    'SHIBUSDT',
    'ALGOUSDT',
    'MKRUSDT',
    'AVAXUSDT',
    'YFIUSDT',
    'MANAUSDT',
    'LUNAUSDT',
    'NEARUSDT',
    'CROUSDT',
    'TONUSDT',

    'USDTBNB',
    'USDTSOL',
    'USDTBTC',
    'USDTLTC',
    'USDTUSDT',
    'USDTDOGE',
    'USDTETH',
    'USDTDASH',
    'USDTXMR',
    'USDTETC',
    'USDTXRP',
    'USDTBCH',
    'USDTTRX',
    'USDTDAI',
    'USDTBTCB',
    'USDTWBTC',
    'USDTBSV',
    'USDTBTG',
    'USDTMATIC',
    'USDTZEC',
    'USDTEURT',
    'USDTXEM',
    'USDTNEO',
    'USDTEOS',
    'USDTADA',
    'USDTWAVES',
    'USDTOMG',
    'USDTZRX',
    'USDTICX',
    'USDTBTT',
    'USDTBAT',
    'USDTONT',
    'USDTQTUM',
    'USDTLINK',
    'USDTATOM',
    'USDTXTZ',
    'USDTDOT',
    'USDTUNI',
    'USDTRVN',
    'USDTSHIB',
    'USDTALGO',
    'USDTMKR',
    'USDTAVAX',
    'USDTYFI',
    'USDTMANA',
    'USDTLUNA',
    'USDTNEAR',
    'USDTOCRO',
    'USDTTON',

    # USDC
    'BNBUSDC',
    'SOLUSDC',
    'BTCUSDC',
    'LTCUSDC',
    'USDTUSDC',
    'DOGEUSDC',
    'ETHUSDC',
    'DASHUSDC',
    'XMRUSDC',
    'ETCUSDC',
    'XRPUSDC',
    'BCHUSDC',
    'TRXUSDC',
    'BSVUSDC',
    'MATICUSDC',
    'ZECUSDC',
    'EOSUSDC',
    'ADAUSDC',
    'WAVESUSDC',
    'OMGUSDC',
    'LINKUSDC',
    'ATOMUSDC',
    'XTZUSDC',
    'DOTUSDC',
    'UNIUSDC',
    'SHIBUSDC',
    'ALGOUSDC',
    'MKRUSDC',
    'AVAXUSDC',
    'YFIUSDC',
    'MANAUSDC',
    'LUNAUSDC',
    'NEARUSDC',
    'CROUSDC',
    'TONUSDC',

    'USDCBNB',
    'USDCSOL',
    'USDCBTC',
    'USDCLTC',
    'USDCUSDT',
    'USDCDOGE',
    'USDCETH',
    'USDCDASH',
    'USDCXMR',
    'USDCETC',
    'USDCXRP',
    'USDCBCH',
    'USDCTRX',
    'USDCBSV',
    'USDCMATIC',
    'USDCZEC',
    'USDCEOS',
    'USDCADA',
    'USDCWAVES',
    'USDCOMG',
    'USDCLINK',
    'USDCATOM',
    'USDCXTZ',
    'USDCDOT',
    'USDCUNI',
    'USDCSHIB',
    'USDCALGO',
    'USDCMKR',
    'USDCAVAX',
    'USDCYFI',
    'USDCMANA',
    'USDCLUNA',
    'USDCNEAR',
    'USDCCRO',
    'USDCTON',
]
ban_list_okx = []


accept_list_mexc = [
]
ban_list_mexc = []


accept_list_bitget = [
]
ban_list_bitget = []


accept_list_gateio = [
]
ban_list_gateio = []


accept_list_pancake = [
]
ban_list_pancake = [
    'USDTLUNA',
    'LUNAUSDT',
]


base_token_2 = [
    'USDT',
    # 'BTC',
]


base_token = [
    'USDT',
    'USDC',
]


exchanges = [
    'binance',
    'bybit',
]