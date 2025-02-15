
class FixedTest(object):
    def __init__(self, test_id: int, name: str, question_ids: list[int], pass_mark: int):
        self.test_id = test_id
        self.name = name
        self.question_ids = question_ids
        self.pass_mark = pass_mark

class FixedTestNotFoundException(Exception):
    pass

class FixedTestRepository(object):
    def __init__(self):
        self._counter = 0
        self._tests: dict[int,FixedTest] = {}
    def all(self) -> list[FixedTest]:
        return list(self._tests.values())
    def create(self, name: str, question_ids: list[int], pass_mark: int) -> FixedTest:
        test = FixedTest(
            self._counter,
            name,
            question_ids,
            pass_mark
        )
        self._tests[test.test_id] = test
        self._counter+=1
        return test
    def read(self, test_id: int) -> FixedTest:
        if test_id not in self._tests.keys():
            raise FixedTestNotFoundException()
        return self._tests[test_id]
    def update(self, test_id: int, name: str, question_ids: list[int], pass_mark: int) -> FixedTest:
        if test_id not in self._tests.keys():
            raise FixedTestNotFoundException()
        test = FixedTest(
            test_id,
            name,
            question_ids,
            pass_mark
        )
        self._tests[test.test_id] = test
        return test
    def delete(self, test_id: int) -> bool:
        if test_id not in self._tests.keys():
            raise FixedTestNotFoundException()
        del self._tests[test_id]
