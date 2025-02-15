from flask import Flask
from flask_restx import Api,Resource,fields

app = Flask(__name__)
api = Api(app)

model = api.model("MultipleChoiceQuestion", {
    "question_id": fields.Integer,
    "collection_ids": fields.List(fields.Integer),
    "stem": fields.String,
    "options": fields.List(fields.String),
    "correct_answer": fields.Integer
})

class MultipleChoiceQuestion(object):
    def __init__(self, question_id: int, collection_ids: list[int], stem: str, options: list[str], correct_answer: int):
        self.question_id = question_id
        self.collection_ids = collection_ids
        self.stem = stem
        self.options = options
        self.correct_answer = correct_answer

class QuestionNotFoundException(Exception):
    pass

class QuestionRepository(object):
    def __init__(self):
        self._counter = 0
        self._questions: dict[int,MultipleChoiceQuestion] = {}
    def create(self, question: MultipleChoiceQuestion) -> MultipleChoiceQuestion:
        question.question_id = self._counter
        self._questions[question.question_id] = question
        self._counter+=1
        return question
    def read(self, question_id: int) -> MultipleChoiceQuestion:
        if question_id not in self._questions.keys():
            raise QuestionNotFoundException()
        return self._questions[question_id]
    def update(self, question: MultipleChoiceQuestion) -> MultipleChoiceQuestion:
        if question.id in self._questions.keys():
            raise QuestionNotFoundException()
        self._questions[question.question_id] = question
        return question
    def delete(self, question_id: int) -> bool:
        if question_id in self._questions.keys():
            raise QuestionNotFoundException()
        del self._questions[question_id]

q_repo = QuestionRepository()
q_repo.create(MultipleChoiceQuestion(None, [], "The answer is a?", ["A", "B", "C", "D"], 0))
q_repo.create(MultipleChoiceQuestion(None, [], "The answer is b?", ["A", "B", "C", "D"], 1))

@api.route("/api/v1/questions")
class QuestionsCreate(Resource):
    @api.marshal_with(model)
    def post(self, question: MultipleChoiceQuestion):
        """
        create a new question
        """
        return q_repo.create(question)
        

@api.route("/api/v1/questions/<int:question_id>")
class QuestionsManage(Resource):
    @api.marshal_with(model)
    def get(self, question_id):
        """
        get the question by the id
        """
        try:
            return q_repo.read(question_id)
        except QuestionNotFoundException:
            return {}, 404
    @api.marshal_with(model)
    def put(self, question: MultipleChoiceQuestion):
        """
        Update the question by the id
        """
        try:
            return q_repo.update(question)
        except QuestionNotFoundException:
            return {}, 404
    def delete(self, question_id):
        """
        Delete the question by the id
        """
        try:
            q_repo.delete(question_id)
        except QuestionNotFoundException:
            return {}, 404
        return {}
