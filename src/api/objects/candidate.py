
class Candidate(object):
    def __init__(self, candidate_id: int, name: str):
        self.candidate_id = candidate_id
        self.name = name

class CandidateNotFoundException(Exception):
    pass

class CandidateRepository(object):
    def __init__(self):
        self._counter = 0
        self._candidates: dict[int,Candidate] = {}
    def all(self) -> list[Candidate]:
        return list(self._candidates.values())
    def create(self, name: str) -> Candidate:
        candidate = Candidate(
            self._counter,
            name
        )
        self._candidates[candidate.candidate_id] = candidate
        self._counter+=1
        return candidate
    def read(self, candidate_id: int) -> Candidate:
        if candidate_id not in self._candidates.keys():
            raise CandidateNotFoundException()
        return self._candidates[candidate_id]
    def update(self, candidate_id: int, name: str) -> Candidate:
        if candidate_id not in self._candidates.keys():
            raise CandidateNotFoundException()
        candidate = Candidate(
            candidate_id,
            name
        )
        self._candidates[candidate.candidate_id] = candidate
        return candidate
    def delete(self, candidate_id: int) -> bool:
        if candidate_id not in self._candidates.keys():
            raise CandidateNotFoundException()
        del self._candidates[candidate_id]
