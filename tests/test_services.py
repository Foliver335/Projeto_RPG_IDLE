import pytest
from adapters.db.sqlite_adapter import SQLiteAdapter
from adapters.ml.recommender import Recommender
from application.services import GameService

@pytest.fixture
def service(tmp_path):
    db = SQLiteAdapter(str(tmp_path/'db.sqlite'))
    ml = Recommender()
    return GameService(db, ml)

def test_start_and_idle(service):
    char = service.start_game('Ana')
    assert char.level == 1
    exp = service.idle_tick(char)
    assert isinstance(exp, int)