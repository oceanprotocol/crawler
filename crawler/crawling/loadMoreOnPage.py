# from bs4 import BeautifulSoup
# from crawling.mongo.models.CrawlerConfig import SelectorsValue
#
#
# def (soup, config: SelectorsValue):
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
#         else:
#             return obj.find_all(config.value)
#
# def selectNrElement(config: SelectorsValue, obj):
#
#     if config.getFirstElement:
#         print(obj)
#         print("FIST")
#         return selectFinalElement(config, obj[0])
#     return selectFinalElement(config, obj)
#
# def selectFinalElement(config: SelectorsValue, obj):
#     print(config)
#     print(obj)
#     result = {
#         None: lambda x: x,
#         'href': lambda x: x.a["href"],
#         'text': lambda x: x.text
#     }[config.selectElement]
#     return result(obj)
