import re


def get_chain_value(start, chain: [], nullable: bool = True):
    current = start
    for attr in chain:
        current = getattr(current, attr, None)
        if current is None:
            if nullable == False:
                raise Exception
            break
    return current


def get_precise_number(value: str):
    return float(re.search("(\d+(?:\,\d{1,2})?)", value)[0].replace(",", "."))


def get_number_from_str(value: str):

    return int(
        re.search("[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+", value)[0]
        .replace(",", "")
        .replace(".", "")
    )
