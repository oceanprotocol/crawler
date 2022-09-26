

class SoupSearchObj:
    mainElementTag:  str
    criteria: dict
    many: bool
    position: int

    def __init__(self, mainElementTag, criteria, many= False, position = 0):
        self.mainElementTag = mainElementTag
        self.criteria = criteria
        self.many = many
        self.position = position