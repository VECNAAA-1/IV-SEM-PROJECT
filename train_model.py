import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

base_dir = os.path.dirname(__file__)
dataset_path = os.path.join(base_dir, 'dataset.csv')

df = pd.read_csv(r"C:\Users\Saurav Gautam\Downloads\merged_feedback_project\ml_model\dataset.csv")
df.dropna(inplace=True)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['text'])

model = LogisticRegression(max_iter=200)
model.fit(X, df['label'])

model_path = os.path.join(base_dir, "model.pkl")

with open(model_path, "wb") as f:
    pickle.dump((model, vectorizer), f)

print("Model trained and saved successfully!")