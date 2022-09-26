from bs4 import BeautifulSoup

from crawling.exceptions.ParsingValuesException import ParsingValuesException
from crawling.models.selectorModels import SoupSearchObj
from crawling.objUtils import getChainValue


#
#
# def getElements(soup, config: SelectorsValue):
#     if config.type == "jsSelector":
#             return selectNrElement(config, soup.select(config.value))
#     elif config.type == "soup":
#
#         return selectNrElement(config, selectSoupElement(config, soup))
#     else:
#         return None
#
#
# def selectSoupElement(config: SelectorsValue, obj:BeautifulSoup):
#
#     if config.value:
#         print(config.classValue)
#         if config.classValue:
#             return obj.find_all(config.value, {"class": config.classValue})
#         elif config.titleValue:
#             return obj.find_all(config.value, {"title": config.titleValue})
#         else:
#             return obj.find_all(config.value)
#
# def selectNrElement(config: SelectorsValue, obj):
#
#     if config.getFirstElement:
#
#         return selectFinalElement(config, obj[0])
#     return selectFinalElement(config, obj)
#
# def selectFinalElement(config: SelectorsValue, obj):
#     result = {
#         None: lambda x: x,
#         'href': lambda x: x["href"],
#         'a.href': lambda x: x.a["href"],
#         'text': lambda x: x.text
#     }[config.selectElement]
#     return result(obj)


def selectSoupElement(
    propertyName: str, soup: BeautifulSoup, filters: SoupSearchObj, chain: []
):
    try:
        if filters.many == False:
            obj = soup.find(filters.mainElementTag, filters.criteria)
            if len(chain) > 0:
                return getChainValue(obj, chain, False)
            return obj
        else:
            obj = soup.findAll(filters.mainElementTag, filters.criteria)
            if filters.many == True:
                obj = obj[filters.position]
                if len(chain) > 0:
                    return getChainValue(obj, chain, False)
                return obj
            return obj
    except Exception:
        raise ParsingValuesException(propertyName)
