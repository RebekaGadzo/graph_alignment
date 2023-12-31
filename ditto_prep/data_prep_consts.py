# urls for data
BLOCKING_INPUT_DIR = '../blocking_ditto/input_block/'
COYPU_CITIES_PATH = '../data_preparation/data/COYPU_start.csv'
SCM_PATH = '../data_preparation/data/SCM_start.csv'
COYPU_PATH_PREP = '../data_preparation/data/COYPU_prep_data.csv'
SCM_PATH_PREP = '../data_preparation/data/SCM_prep_data.csv'

# levenstein comparison threshold 
COMPARE_COMPANY_THRESHOLD = 0.30

# selected countries for comparison
ISO_CODES = ['DE', 'US', 'CN']

REMOVE_COMPANY_SUFFIXES = {
    'DE': {
        'ag', 'se', 'eg', 'ev', 'e v', 'ek', 'e k', 'ohg', 'ug', 'gmbh'
    },
    'INTERNATIONAL': {
        'inc','lc', 'l.c.', 'l.c', 'limited company' ,'limited', 'co'
    } 
}    

REMOVAL_WORDS = ['gmbh', ' co ', 'co.', '&', '.inc', ' inc ', 'inc.', 'llc', 'ltd', 'ltd.', 'kg ',' kg', 'k.g.', ' ag ', 'mbh' , 'gbr', ' ohg ', 'corporation', 'corp', \
    'l.l.c.', ' lp', 'l.p', 'l.p.', ' ag ', 'e v', 'e.V.', ' ev ' ,' ek ', ' ug ', ' eg ', ' pty', 'fpi', '(hk) limited', 'aktiengesellschaft', 'haftungsbeschraenkt', 
    'unternehmergesellschaft', 'kommanditgesellschaft', 'eingetragener verein', 'incorporated', 'gesellschaft mit beschraenkter haftung']

REMOVAL_SEPARATORS = [',', '+', '-', '.', '"']

COMPANY_CATEGORIES = {
    'DE': {
        'gmbh':'gmbh', 'gesellschaft mit beschraenkter haftung': 'gmbh', 'g.m.b.h.' : 'gmbh', 'gmbh & co.' : 'gmbh & co.', 'GmbH und Co.':'gmbh & co.', 'gmbh und co.':'gmbh & co.',
        'kg ':'kg', ' kg':'kg', 'k.g.':'kg' ,'kg' : 'kg', 'kommanditgesellschaft':'kg',
        ' ag ':'ag', 'aktiengesellschaft': 'ag',
        ' ug': 'ug', 'unternehmergesellschaft': 'ug', 'haftungsbeschraenkt': 'ug',
        ' ohg ': 'ohg',
        'kirchengemeinden': 'kirchengemeinden',
        'erbengemeinschaft': 'erbengemeinschaft',
        'mbh':'mbh',
        'gbr':'gbr',
        'e v':'eV', 'e.V.':'eV', ' ev ': 'eV', 'eingetragener verein': 'ev', ' e V ':'eV', ' ev ':'eV',
        ' ek ':'ek',
        'eingetragene genossenschaft':'eg', ' eg ':'eg',
        'ltd':'ltd', 'ltd.':'ltd', 'limited':'ltd',
        ' co ': 'co', 'co.' : 'co', 'corporation':'co', 'corp': 'co',
        'stiftung': 'stiftung',
        "bank": "bank", 'volksbank':'bank', 'sparkasse': 'bank',
        'gesellschaft zur foerderung': 'gesellschaft zur foerderung',
        'gesellschaft der freunde': 'gesellschaft der freunde',
        'Vermoegensverwaltungsgesellschaft': 'Vermoegensverwaltungsgesellschaft',
        'gesellschaft buergerlichen rechts mit beschraenkter haftung' : 'gbr mbh',
        'fund': 'fund', 'fonds': 'fonds', 'etf': 'fund', 'fund limited': 'fund', 'trust': 'fund'
        },
    
    'INTERNATIONAL' : {
        ' co ': 'co', 'co.' : 'co', 'corporation':'co', 'corp': 'co',
        '.inc': 'inc', ' inc ':'inc', 'inc.':'inc', 'incorporated': 'inc',
        'llc':'llc', 'l.l.c.':'llc',
        'lc': 'lc', 
        'ltd':'ltd', 'ltd.':'ltd', 'limited':'ltd',
        ' lp':'lp', 'l.p.':'lp', 'limited partnership': 'lp', 'llp': 'llp', 'lllp': 'lllp', 'l.p':'lp',
        ' pty':'pty',
        '(hk) limited':'(hk) limited',
        'fund': 'fund', 'fonds': 'fonds', 'etf': 'fund', 'fund limited': 'fund', 'trust': 'fund',
        'insurance company': 'company', 'travel company': 'company',
        'city of': 'city', 'city': 'city', 'county of':'county', 'county': 'county',
        'church': 'church', 'kirche' : 'kirche',
        'credit union': 'credit union', 'investments': 'investments', 'institute': 'institute','management': 'management', 'advisors': 'advisors', 'trading':'trading',
        'investment group' : 'investment group'
        }     
    }

REMOVAL_WORDS_LOCATION_SCM = [
    " china", 
    "h.k, ",
    "kds, ",
    "china, ",
    "scc, ",
    "japan, ",
    "lux, ",
    "hk, ",
    "foxconn, ",
    " china, s1a s1b s1c",
    ", songjiang",
    "china, ",
    " city",
    ", msc",
    "4403046751, ",
    "sz, ",
    "g.z, ",
    " province",
    " downtown",
    " branch",
    "china, ",
    "szx, ",
    "macao commercial offshore, ",
    "shanghai shenhe thermal magnetic electronics co., ltd., ",
    " ",
    "aoc, ",
    "sip, ",
    "m, ",
    " city",
    "sz, ",
    " china, cfab",
    "prosperity technology, ",
    "group, ",
    "delphi, ",
    "Fujian, ",
    "smic, ",
    " china, united semiconductor",
    " china, fab 16a/b",
    "pumps and industrial fans",
    "asia, ",
    " city",
    "amecco, ",
    " china, ssec",
    "“nexchip”, ",
    "ap, ",
    ", cny invoicing only",
    " bahnhof",
    " germany",
    #"suedwestmetall, ",
    "germany, ",
    #" (, baden",
    "wk plastics, ",
    "formerly poly one corporation, ",
    "europe, ",
    "deutschland",
    #"mitte",
    "deutschland, ",
    "kuenstlersozialkasse, ",
    "international business machines, ",
    #"(, ruhr",
    "pty, ",
    "official, ",
    "fraenkische industrial pipes , ",
    #" (, saar",
    "downers grove, ",
    'suzhou , '
    'germany, ',
    'dongguan, ',
    'import export, ',
    'engineering office, ',
    'm, ',
    'tosoh smd group, ',
    'bp group, ',
    'umc, ',
    'america, ',
    'basf group, ',
    'pty, ',
    'formerly poly one corporation, ',
    'umc, ',
    'uac, ',
    'a division of bachus son , ',
    'manufacturing tooling center, ',
    'ex value plastics, ',
    'former alcoa ees, ',
    'college station',
    'f.s. fehrer automotive, ',
    'americas, ',
    'fpi, ',
    'pidc, ',
    'form. alan l grant centrotrade wurfbain, ',
    'saco community based outpatient clinic',
    'uk, '
]

REMOVAL_WORDS_LOCATION_SCM = [
    " china", 
    "h.k, ",
    "kds, ",
    "china, ",
    "scc, ",
    "japan, ",
    "lux, ",
    "hk, ",
    "foxconn, ",
    " china, s1a s1b s1c",
    "china, ",
    " city",
    ", msc",
    "4403046751, ",
    "sz, ",
    "g.z, ",
    " province",
    " downtown",
    " branch",
    "china, ",
    "szx, ",
    "macao commercial offshore, ",
    "shanghai shenhe thermal magnetic electronics co., ltd., ",
    "aoc, ",
    "sip, ",
    "m, ",
    " city",
    "sz, ",
    " china, cfab",
    "prosperity technology, ",
    "group, ",
    "delphi, ",
    "smic, ",
    " china, united semiconductor",
    " china, fab 16a/b",
    "pumps and industrial fans",
    "asia, ",
    " city",
    "amecco, ",
    " china, ssec",
    "“nexchip”, ",
    "ap, ",
    ", cny invoicing only",
    " bahnhof",
    " germany",
    "suedwestmetall, ",
    "germany, ",
    "wk plastics, ",
    "formerly poly one corporation, ",
    "europe, ",
    "deutschland",
    "deutschland, ",
    "kuenstlersozialkasse, ",
    "international business machines, ",
    "pty, ",
    "official, ",
    "fraenkische industrial pipes , ",
    "downers grove, ",
    'germany, ',
    'import export, ',
    'engineering office, ',
    'm, ',
    'tosoh smd group, ',
    'bp group, ',
    'umc, ',
    'america, ',
    'basf group, ',
    'pty, ',
    'formerly poly one corporation, ',
    'umc, ',
    'uac, ',
    'a division of bachus son , ',
    'manufacturing tooling center, ',
    'ex value plastics, ',
    'former alcoa ees, ',
    'college station',
    'f.s. fehrer automotive, ',
    'americas, ',
    'fpi, ',
    'pidc, ',
    'form. alan l grant centrotrade wurfbain, ',
    'saco community based outpatient clinic',
    'uk, '
]


REMOVAL_WORDS_COMPANY_NAME_SCM = [
    "china", 
    "japan",
    "s1a s1b s1c",
    "songjiang",
    "city",
    "4403046751",
    "province",
    "downtown",
    "branch",
    "Fujian",
    "asia",
    "bahnhof",
    "germany",
    "europe",
    "deutschland",
    "mitte",
    'suzhou'
    'dongguan',
    'america',
    'americas',
    'uk'
]
