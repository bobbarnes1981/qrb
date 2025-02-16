from flask import Flask, abort
from flask_restx import Api, Resource, fields, reqparse
from .objects.mcq_question import MCQQuestionRepository, MCQQuestionNotFoundException
from .objects.question_collection import QuestionCollectionRepository, QuestionCollectionNotFoundException
from .objects.fixed_test import FixedTestRepository, FixedTestNotFoundException
from .objects.candidate import CandidateRepository, CandidateNotFoundException
from .objects.candidate_test import CandidateTestRepository, CandidateTestNotFoundException

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

candidate_model = api.model("Candidate", {
    "candidate_id": fields.Integer,
    "name": fields.String
})

candidatetest_model = api.model("CandidateTest", {
    "candidatetest_id": fields.Integer,
    "candidate_id": fields.Integer,
    "test_id": fields.Integer
})

c_repo = CandidateRepository()
c_repo.create("Candidate 1")
c_repo.create("Candidate 2")

qc_repo = QuestionCollectionRepository()
qc_repo.create("collection 1")
qc_repo.create("collection 2")

q_repo = MCQQuestionRepository()
q_repo.create([0], "The answer is a?", ["A", "B", "C", "D"], 0)
q_repo.create([0,1], "The answer is b?", ["A", "B", "C", "D"], 1)

t_repo = FixedTestRepository()
t_repo.create("Test 1", [0,1], 1)

ct_repo = CandidateTestRepository()
ct_repo.create(0, 0)
ct_repo.create(0, 1)
ct_repo.create(1, 1)

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

        return qc_repo.create(
            data["name"]
        )
    @api.marshal_with(collection_model)
    def get(self):
        """
        get all collections
        """
        return qc_repo.all()

@api.route("/api/v1/questioncollections/<int:collection_id>")
class QuestionCollectionsManageApi(Resource):
    @api.marshal_with(collection_model)
    def get(self, collection_id):
        """
        get the collection by the id
        """
        try:
            return qc_repo.read(collection_id)
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

            return qc_repo.update(
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
            qc_repo.delete(collection_id)
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

@api.route("/api/v1/candidates")
class CandidatesApi(Resource):
    @api.marshal_with(candidate_model)
    def post(self):
        """
        create a new candidate
        """
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, location="json")
        data = parser.parse_args(strict=True)

        return c_repo.create(
            data["name"]
        )
    @api.marshal_with(candidate_model)
    def get(self):
        """
        get all candidates
        """
        return c_repo.all()

@api.route("/api/v1/candidates/<int:candidate_id>")
class CandidatesManageApi(Resource):
    @api.marshal_with(candidate_model)
    def get(self, candidate_id):
        """
        get the candidate by the id
        """
        try:
            return t_repo.read(candidate_id)
        except CandidateNotFoundException:
            abort(404)
    @api.marshal_with(candidate_model)
    def put(self, candidate_id):
        """
        Update the candidate by the id
        """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str, location="json")
            data = parser.parse_args(strict=True)

            return c_repo.update(
                candidate_id,
                data["name"]
            )
        except CandidateNotFoundException:
            abort(404)
    def delete(self, candidate_id):
        """
        Delete the candidate by the id
        """
        try:
            c_repo.delete(candidate_id)
        except CandidateNotFoundException:
            abort(404)
        return {}


@api.route("/api/v1/candidatetests")
class CandidateTestsApi(Resource):
    @api.marshal_with(candidatetest_model)
    def post(self):
        """
        create a new candidate test
        """
        parser = reqparse.RequestParser()
        parser.add_argument("candidate_id", type=int, location="json")
        parser.add_argument("test_id", type=int, location="json")
        data = parser.parse_args(strict=True)

        return ct_repo.create(
            data["candidate_id"],
            data["test_id"]
        )
    @api.marshal_with(candidatetest_model)
    def get(self):
        """
        get all candidate tests
        """
        return ct_repo.all()

@api.route("/api/v1/candidatetests/<int:candidatetest_id>")
class CandidateTestsManageApi(Resource):
    @api.marshal_with(candidatetest_model)
    def get(self, candidatetest_id):
        """
        get the candidate test by the id
        """
        try:
            return ct_repo.read(candidatetest_id)
        except CandidateTestNotFoundException:
            abort(404)
    @api.marshal_with(candidatetest_model)
    def put(self, candidatetest_id):
        """
        Update the candidate test by the id
        """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("candidate_id", type=int, location="json")
            parser.add_argument("test_id", type=int, location="json")
            data = parser.parse_args(strict=True)

            return ct_repo.update(
                candidatetest_id,
                data["candidate_id"],
                data["test_id"]
            )
        except CandidateTestNotFoundException:
            abort(404)
    def delete(self, candidatetest_id):
        """
        Delete the candidate test by the id
        """
        try:
            ct_repo.delete(candidatetest_id)
        except CandidateTestNotFoundException:
            abort(404)
        return {}
