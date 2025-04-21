import pytest
from adapters.ui.gui_adapter import GUIAdapter
from application.services import GameService

def test_gui_launch(monkeypatch):
    ga = GUIAdapter(service=GameService(None,None))
    assert ga.root.title() == "Crônicas Adaptativas"