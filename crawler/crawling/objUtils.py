import re


def getChainValue(start, chain: [], nullable: bool = True):
    current = start
    for c in chain:
        current = getattr(current, c, None)
        if current is None:
            if nullable == False:
                raise Exception
            break
    return current


def getPreciseNumber(value: str):
    return float(re.search("(\d+(?:\,\d{1,2})?)", value)[0].replace(",", "."))


def getNumberFromStr(value: str):

    return int(
        re.search("[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+", value)[0]
        .replace(",", "")
        .replace(".", "")
    )
