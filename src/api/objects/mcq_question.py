
class MCQQuestion(object):
    def __init__(self, question_id: int, collection_ids: list[int], stem: str, options: list[str], correct_answer: int):
        self.question_id = question_id
        self.collection_ids = collection_ids
        self.stem = stem
        self.options = options
        self.correct_answer = correct_answer

class MCQQuestionNotFoundException(Exception):
    pass

class MCQQuestionRepository(object):
    def __init__(self):
        self._counter = 0
        self._questions: dict[int,MCQQuestion] = {}
    def all(self) -> list[MCQQuestion]:
        return list(self._questions.values())
    def create(self, collection_ids: list[int], stem: str, options: list[int], correct_answer: int) -> MCQQuestion:
        question = MCQQuestion(
            self._counter,
            collection_ids,
            stem,
            options,
            correct_answer
        )
        self._questions[question.question_id] = question
        self._counter+=1
        return question
    def read(self, question_id: int) -> MCQQuestion:
        if question_id not in self._questions.keys():
            raise MCQQuestionNotFoundException()
        return self._questions[question_id]
    def update(self, question_id: int, collection_ids: list[int], stem: str, options: list[int], correct_answer: int) -> MCQQuestion:
        if question_id not in self._questions.keys():
            raise MCQQuestionNotFoundException()
        question = MCQQuestion(
            question_id,
            collection_ids,
            stem,
            options,
            correct_answer
        )
        self._questions[question.question_id] = question
        return question
    def delete(self, question_id: int) -> bool:
        if question_id not in self._questions.keys():
            raise MCQQuestionNotFoundException()
        del self._questions[question_id]
