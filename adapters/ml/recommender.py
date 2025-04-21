import pickle, os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np
from domain.entities import Quest
from adapters.db.sqlite_adapter import SQLiteAdapter

class Recommender:
    def __init__(self, model_path: str = None):
        self.path = model_path
        self.model = None
        if model_path and os.path.exists(model_path):
            self.model = pickle.load(open(model_path, 'rb'))

    def suggest_quests(self, data: dict) -> list[Quest]:
        level = data.get('level', 1)
        if self.model:
            cls = self.model.predict([[data['xp'], data['xp'], 1, level]])[0]
            return [Quest(id=f"que_ml_{cls}", description=f"Quest preferida #{cls}", difficulty=level, rewards={'ouro':level*10})]
        return [Quest(id=f"que_{level}_1", description="Defenda a vila", difficulty=level, rewards={'ouro':level*10})]

    def train(self):
        db = SQLiteAdapter('game.db')
        bh = pd.DataFrame(db.load_battles_all())
        qs = pd.DataFrame(db.load_all_quests())
        if bh.empty or qs.empty:
            print("Dados insuficientes para treino.")
            return
        fav = qs.groupby('char_id')['difficulty'].mean().rename('avg_diff')
        stats = bh.groupby('char_id').agg({'xp':['mean','sum'],'victory':'mean'})
        stats.columns = ['xp_mean','xp_sum','win_rate']
        data = stats.join(fav, how='inner').reset_index()
        X = data[['xp_mean','xp_sum','win_rate','avg_diff']]
        y = np.random.choice([0,1,2], size=len(X))
        params = {'max_depth':[3,5,10],'min_samples_split':[2,5,10]}
        grid = GridSearchCV(DecisionTreeClassifier(), param_grid=params, cv=3)
        grid.fit(X, y)
        self.model = grid.best_estimator_
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        pickle.dump(self.model, open(self.path, 'wb'))
        print(f"Treino concluído. {grid.best_params_}")