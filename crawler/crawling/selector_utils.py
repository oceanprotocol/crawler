from bs4 import BeautifulSoup

from crawling.exceptions.ParsingValuesException import ParsingValuesException
from crawling.models.soup_search import SoupSearchObj
from crawling.obj_utils import get_chain_value


def select_soup_element(
    propertyName: str, soup: BeautifulSoup, filters: SoupSearchObj, chain: []
):
    try:
        if filters.many == False:
            obj = soup.find(filters.mainElementTag, filters.criteria)
            if len(chain) > 0:
                return get_chain_value(obj, chain, False)
            return obj
        else:
            obj = soup.findAll(filters.mainElementTag, filters.criteria)
            if filters.many == True:
                obj = obj[filters.position]
                if len(chain) > 0:
                    return get_chain_value(obj, chain, False)
                return obj
            return obj
    except Exception:
        raise ParsingValuesException(propertyName)
