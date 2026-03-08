# 🧠 FeedbackIQ — Intelligent Customer Feedback Analysis System

An AI-powered Flask web application that automatically analyzes customer feedback using NLP, detects sentiment, extracts key themes, and generates actionable business insights.

---

## 📁 Project Structure

```
feedback_analysis/
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
│
├── config/
│   ├── __init__.py
│   └── settings.py                 # Dev / Prod / Test configs
│
├── app/
│   ├── __init__.py                 # Flask app factory
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py                 # Page routes (/, /upload, /results, /about)
│   │   └── api.py                  # REST API endpoints (/api/*)
│   │
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── preprocessor.py         # Text cleaning & tokenization
│   │   ├── sentiment.py            # Sentiment classification (TextBlob)
│   │   ├── theme_extractor.py      # TF-IDF keyword & phrase extraction
│   │   ├── insight_generator.py    # Business insight & recommendation engine
│   │   └── visualizer.py          # Chart generation (Matplotlib, WordCloud)
│   │
│   ├── templates/
│   │   ├── base.html               # Shared layout with sidebar
│   │   ├── index.html              # Dashboard
│   │   ├── upload.html             # Feedback input (text + file)
│   │   ├── results.html            # Full results visualization
│   │   └── about.html             # System info & API docs
│   │
│   └── static/
│       ├── css/style.css           # Dark-theme UI styles
│       └── js/
│           ├── app.js              # Shared utilities
│           ├── upload.js           # Upload page logic
│           └── results.js          # Results rendering logic
│
├── data/
│   ├── sample_feedback.csv         # Sample data for testing
│   └── uploads/                    # Uploaded files (auto-created)
│
└── tests/
    └── test_modules.py             # Unit tests for all NLP modules
```

---

## 🚀 Getting Started

### 1. Clone & set up environment

```bash
git clone <repo-url>
cd feedback_analysis

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Run in development

```bash
python run.py
```

Visit: [http://localhost:5000](http://localhost:5000)

### 3. Run in production (Gunicorn)

```bash
gunicorn run:app --workers 4 --bind 0.0.0.0:8000
```

---

## 🔌 REST API

### Health Check
```
GET /api/health
```

### Analyze Text
```
POST /api/analyze/text
Content-Type: application/json

{
  "feedback": [
    "Amazing product, highly recommend!",
    "Shipping was very slow and disappointing.",
    "Okay experience overall."
  ]
}
```

### Analyze File
```
POST /api/analyze/file
Content-Type: multipart/form-data

file: <your .csv / .txt / .json file>
```

**Supported formats:**
- **CSV**: First column is used (header row skipped)
- **TXT**: One feedback item per line
- **JSON**: List of strings `["text1", "text2"]`

---

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

---

## ⚙️ NLP Pipeline

| Step | Module | Technique |
|------|--------|-----------|
| Preprocessing | `preprocessor.py` | Tokenization, stopword removal, lemmatization |
| Sentiment | `sentiment.py` | TextBlob polarity & subjectivity scoring |
| Theme Extraction | `theme_extractor.py` | TF-IDF, n-gram frequency analysis |
| Insight Generation | `insight_generator.py` | Rule-based recommendations & alerts |
| Visualization | `visualizer.py` | Matplotlib pie/bar/histogram, WordCloud |

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11, Flask 3.0
- **NLP**: NLTK, TextBlob, scikit-learn
- **Visualization**: Matplotlib, WordCloud
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Gunicorn (WSGI server)
