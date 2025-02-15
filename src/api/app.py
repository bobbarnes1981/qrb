from flask import Flask, abort
from flask_restx import Api, Resource, fields, reqparse
from .objects.mcq_question import MCQQuestionRepository, MCQQuestionNotFoundException
from .objects.question_collection import QuestionCollectionRepository, QuestionCollectionNotFoundException
from .objects.fixed_test import FixedTestRepository, FixedTestNotFoundException

app = Flask(__name__)
api = Api(app)

question_model = api.model("MCQQuestion", {
    "question_id": fields.Integer,
    "collection_ids": fields.List(fields.Integer),
    "stem": fields.String,
    "options": fields.List(fields.String),
    "correct_answer": fields.Integer
})

collection_model = api.model("QuestionCollection", {
    "collection_id": fields.Integer,
    "name": fields.String
})

test_model = api.model("FixedTest", {
    "test_id": fields.Integer,
    "name": fields.String,
    "question_ids": fields.List(fields.Integer),
    "pass_mark": fields.Integer
})

c_repo = QuestionCollectionRepository()
c_repo.create("collection 1")
c_repo.create("collection 2")

q_repo = MCQQuestionRepository()
q_repo.create([0], "The answer is a?", ["A", "B", "C", "D"], 0)
q_repo.create([0,1], "The answer is b?", ["A", "B", "C", "D"], 1)

t_repo = FixedTestRepository()
t_repo.create("Test 1", [0,1], 1)

@api.route("/api/v1/mcqquestions")
class MCQQuestionsApi(Resource):
    @api.marshal_with(question_model)
    def post(self):
        """
        create a new question
        """
        parser = reqparse.RequestParser()
        parser.add_argument("collection_ids", type=list[int], location="json")
        parser.add_argument("stem", type=str, location="json")
        parser.add_argument("options", type=list[str], location="json")
        parser.add_argument("correct_answer", type=int, location="json")
        data = parser.parse_args(strict=True)

        return q_repo.create(
            data["collection_ids"],
            data["stem"],
            data["options"],
            data["correct_answer"]
        )
    @api.marshal_with(question_model)
    def get(self):
        """
        get all questions
        """
        return q_repo.all()

@api.route("/api/v1/mcqquestions/<int:question_id>")
class MCQQuestionsManageApi(Resource):
    @api.marshal_with(question_model)
    def get(self, question_id):
        """
        get the question by the id
        """
        try:
            return q_repo.read(question_id)
        except MCQQuestionNotFoundException:
            abort(404)
    @api.marshal_with(question_model)
    def put(self, question_id):
        """
        Update the question by the id
        """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("collection_ids", type=list[int], location="json")
            parser.add_argument("stem", type=str, location="json")
            parser.add_argument("options", type=list[str], location="json")
            parser.add_argument("correct_answer", type=int, location="json")
            data = parser.parse_args(strict=True)

            return q_repo.update(
                question_id,
                data["collection_ids"],
                data["stem"],
                data["options"],
                data["correct_answer"]
            )
        except MCQQuestionNotFoundException:
            abort(404)
    def delete(self, question_id):
        """
        Delete the question by the id
        """
        try:
            q_repo.delete(question_id)
        except MCQQuestionNotFoundException:
            abort(404)
        return {}

@api.route("/api/v1/questioncollections")
class QuestionCollectionsApi(Resource):
    @api.marshal_with(collection_model)
    def post(self):
        """
        create a new collection
        """
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, location="json")
        data = parser.parse_args(strict=True)

        return c_repo.create(
            data["name"]
        )
    @api.marshal_with(collection_model)
    def get(self):
        """
        get all collections
        """
        return c_repo.all()

@api.route("/api/v1/questioncollections/<int:collection_id>")
class QuestionCollectionsManageApi(Resource):
    @api.marshal_with(collection_model)
    def get(self, collection_id):
        """
        get the collection by the id
        """
        try:
            return c_repo.read(collection_id)
        except QuestionCollectionNotFoundException:
            abort(404)
    @api.marshal_with(collection_model)
    def put(self, collection_id):
        """
        Update the collection by the id
        """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str, location="json")
            data = parser.parse_args(strict=True)

            return c_repo.update(
                collection_id,
                data["name"]
            )
        except QuestionCollectionNotFoundException:
            abort(404)
    def delete(self, collection_id):
        """
        Delete the question by the id
        """
        try:
            c_repo.delete(collection_id)
        except QuestionCollectionNotFoundException:
            abort(404)
        return {}

@api.route("/api/v1/fixedtests")
class FixedTestsApi(Resource):
    @api.marshal_with(test_model)
    def post(self):
        """
        create a new test
        """
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, location="json")
        parser.add_argument("question_ids", type=list[int], location="json")
        parser.add_argument("pass_mark", type=int, location="json")
        data = parser.parse_args(strict=True)

        return t_repo.create(
            data["name"],
            data["question_ids"],
            data["pass_mark"]
        )
    @api.marshal_with(test_model)
    def get(self):
        """
        get all tests
        """
        return t_repo.all()

@api.route("/api/v1/fixedtests/<int:test_id>")
class FixedTestsManageApi(Resource):
    @api.marshal_with(test_model)
    def get(self, test_id):
        """
        get the test by the id
        """
        try:
            return t_repo.read(test_id)
        except FixedTestNotFoundException:
            abort(404)
    @api.marshal_with(test_model)
    def put(self, test_id):
        """
        Update the test by the id
        """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str, location="json")
            parser.add_argument("question_ids", type=list[int], location="json")
            parser.add_argument("pass_mark", type=int, location="json")
            data = parser.parse_args(strict=True)

            return t_repo.update(
                test_id,
                data["name"],
                data["question_ids"],
                data["pass_mark"]
            )
        except FixedTestNotFoundException:
            abort(404)
    def delete(self, test_id):
        """
        Delete the test by the id
        """
        try:
            t_repo.delete(test_id)
        except FixedTestNotFoundException:
            abort(404)
        return {}
