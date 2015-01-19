from scrapy.item import Item, Field


# class Website(Item):
#
#     name = Field()
#     description = Field()
#     url = Field()
#     pubDate = Field()


class Post(Item):

    messURL = Field()
    redirURL = Field()
    refURL = Field()
    depth = Field()

    # original = Field()
    message = Field()
    subject = Field()
    title = Field()
    forum = Field()
    title = Field()
    numRepls = Field()
    date=Field()
    link=Field()
    # authrURL = Field()

