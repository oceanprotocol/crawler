import re

def getValueIfNotNull(start, *chain):
    current = start
    for c in chain:
        current = getattr(current, c, None)
        if current is None:
            break
    return current

def getNumberFromStr(value: str):

    return int(re.search('[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', value)[0].replace(',','').replace('.',''))