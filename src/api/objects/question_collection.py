
class QuestionCollection(object):
    def __init__(self, collection_id: int, name: str):
        self.collection_id = collection_id
        self.name = name

class QuestionCollectionNotFoundException(Exception):
    pass

class QuestionCollectionRepository(object):
    def __init__(self):
        self._counter = 0
        self._collections: dict[int,QuestionCollection] = {}
    def all(self) -> list[QuestionCollection]:
        return list(self._collections.values())
    def create(self, name: str) -> QuestionCollection:
        collection = QuestionCollection(
            self._counter,
            name
        )
        self._collections[collection.collection_id] = collection
        self._counter+=1
        return collection
    def read(self, collection_id: int) -> QuestionCollection:
        if collection_id not in self._collections.keys():
            raise QuestionCollectionNotFoundException()
        return self._collections[collection_id]
    def update(self, collection_id: int, name: str) -> QuestionCollection:
        if collection_id not in self._collections.keys():
            raise QuestionCollectionNotFoundException()
        collection = QuestionCollection(
            collection_id,
            name
        )
        self._collections[collection.collection_id] = collection
        return collection
    def delete(self, collection_id: int) -> bool:
        if collection_id not in self._collections.keys():
            raise QuestionCollectionNotFoundException()
        del self._collections[collection_id]
