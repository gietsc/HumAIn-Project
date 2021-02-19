import json

from pandas.core.frame import DataFrame


# class Tags:
#     def __init__(self, list_string: list[str]):
#         self.tag_list = list_string
#         pass
    



class ArticleWrapper:
    def __init__(self, article_name,topic_name , tags) :
        self.article_name = article_name
        self.topic_name = topic_name
        self.tags = tags

    def convert_to_json(self):
        return json.dump(self)

class Topic:
    '''
    tags are dataframes with following columns:
    index : starting from 0, sorted ascending based on weight
    Name : string of the tag
    Weight : float representing the weight of this tag in it's topic
    '''
    def __init__(self, name: str, tags: DataFrame):
        self.name = name
        self.tags = tags
        tags.index.names = [name]
       

