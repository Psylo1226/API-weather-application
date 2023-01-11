from pymongo import MongoClient
import pandas as pd


class MongoDB(object):

    def __init__(self, dBName=None, collectionName=None):
        self.dBName = dBName
        self.collectionName = collectionName
        self.client = MongoClient('localhost', 27017)

        self.DB = self.client[self.dBName]
        self.collection = self.DB[self.collectionName]

    def InsertData(self, path=None):
        """
        :param path: Path os csv file
        :return: None
        """

        df = pd.read_csv(path)
        data = df.to_dict('records')

        self.collection.insert_many(data, ordered=False)


if __name__ == '__main__':
    MongoDB()

