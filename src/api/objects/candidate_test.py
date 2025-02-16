
class CandidateTest(object):
    def __init__(self, candidatetest_id: int, candidate_id: int, test_id: int):
        self.candidatetest_id = candidatetest_id
        self.candidate_id = candidate_id
        self.test_id = test_id

class CandidateTestNotFoundException(Exception):
    pass

class CandidateTestRepository(object):
    def __init__(self):
        self._counter = 0
        self._candidatetests: dict[int,CandidateTest] = {}
    def all(self) -> list[CandidateTest]:
        return list(self._candidatetests.values())
    def create(self, candidate_id: int, test_id: int) -> CandidateTest:
        candidatetest = CandidateTest(
            self._counter,
            candidate_id,
            test_id
        )
        self._candidatetests[candidatetest.candidatetest_id] = candidatetest
        self._counter+=1
        return candidatetest
    def read(self, candidatetest_id: int) -> CandidateTest:
        if candidatetest_id not in self._candidatetests.keys():
            raise CandidateTestNotFoundException()
        return self._candidatetests[candidatetest_id]
    def update(self, candidatetest_id: int, candidate_id: int, test_id: int) -> CandidateTest:
        if candidatetest_id not in self._candidatetests.keys():
            raise CandidateTestNotFoundException()
        candidatetest = CandidateTest(
            candidatetest_id,
            candidate_id,
            test_id
        )
        self._candidatetests[candidatetest.candidatetest_id] = candidatetest
        return candidatetest
    def delete(self, candidatetest_id: int) -> bool:
        if candidatetest_id not in self._candidatetests.keys():
            raise CandidateTestNotFoundException()
        del self._candidatetests[candidatetest_id]
