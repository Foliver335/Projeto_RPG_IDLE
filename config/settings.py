'''import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'game.db')
MODEL_DIR = os.path.join(BASE_DIR, '..', 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'recommender.pkl')'''

import os
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = ':memory:'  # Banco em memória para desenvolvimento temporário
MODEL_DIR = os.path.join(BASE_DIR, '..', 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'recommender.pkl')

#API_KEY = os.getenv("OPENAI_API_KEY")