from config.settings import DB_PATH, MODEL_PATH
from adapters.db.sqlite_adapter import SQLiteAdapter
from adapters.ml.recommender import Recommender
from application.services import GameService
from adapters.ui.gui_adapter import GUIAdapter
from adapters.ui.cli_adapter import CLIAdapter


def main():
    # Inicializa adaptadores e serviço
    db = SQLiteAdapter(DB_PATH)
    ml = Recommender(MODEL_PATH)
    service = GameService(db, ml)
    # Inicia versão GUI com Tkinter
    gui = GUIAdapter(service)
    gui.run()
    CLIAdapter(service).run()


if __name__ == '__main__':
    main()