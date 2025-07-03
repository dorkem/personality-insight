from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

class PersonalityModel:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.model = RandomForestClassifier(random_state=42)

    def train(self):
        y = self.df["PERSONALITY"]
        X = self.df.drop("PERSONALITY", axis=1)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(self.X_train, self.y_train)

    def evaluate(self):
        y_pred = self.model.predict(self.X_test)
        acc = accuracy_score(self.y_test, y_pred)
        report = classification_report(self.y_test, y_pred, target_names=["Introvert", "Extrovert"])
        return acc, report

    def get_feature_importance(self):
        return pd.Series(self.model.feature_importances_, index=self.X_train.columns).sort_values(ascending=False)

    def get_model(self):
        return self.model
