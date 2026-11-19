# Resume Matcher AI – Intelligence Suite
### AI-Powered Recruitment | Resume Parsing | NLP | Candidate Intelligence

---

## 📌 About the Project

**Resume Matcher AI** is an AI-powered recruitment intelligence platform designed to automate resume screening, evaluate candidate-job compatibility, and generate evidence-based candidate rankings.

The platform processes multiple resumes in PDF, DOCX, and TXT formats, extracts relevant candidate information, and compares it against job descriptions using Natural Language Processing (NLP) and a five-component weighted scoring engine.

It provides recruiters with structured candidate profiles, compatibility scores, skill-gap analysis, and explainable selection reasoning to support informed hiring decisions.

---

## ✨ Key Features

- **Multi-Resume Processing:** Upload and analyze multiple resumes simultaneously across PDF, DOCX, and TXT formats.
- **Intelligent Resume Parsing:** Extracts technical skills, educational qualifications, professional experience, and project information.
- **Candidate Ranking:** Automatically ranks applicants based on their overall compatibility scores.
- **Weighted Matching Engine:** Evaluates candidates across five dimensions: technical skills, semantic similarity, experience, education, and projects.
- **Explainable AI:** Generates selection reasoning highlighting candidate strengths, missing qualifications, and comparative advantages.
- **Skill Gap Analysis:** Identifies exact skill matches, missing requirements, and transferable skills.
- **Evidence-Based Evaluation:** Connects extracted information to resume content instead of assuming or inventing credentials.
- **Candidate Analytics:** Provides detailed score breakdowns, ranking insights, and candidate evaluation history.
- **Responsible AI:** Supports human-in-the-loop recruitment without intentionally using protected demographic characteristics in scoring.

---

## 🛠️ Skills & Tools

- **Programming Languages:** Python | JavaScript
- **AI & Natural Language Processing:** Natural Language Processing (NLP) | TF-IDF | Cosine Similarity | Text Preprocessing | Semantic Matching
- **Data Processing & Validation:** Pandas | Pydantic | Document Parsing | Data Extraction
- **Frameworks & Tools:** FastAPI | React 18 | Vite | REST APIs | Pytest | Swagger UI
- **Document Processing:** PDF | DOCX | TXT

---

## ⚙️ Matching Algorithm

The platform evaluates candidates using a five-component weighted scoring methodology.

| Evaluation Component | Weight |
| :--- | :---: |
| Technical Skills Match | 35% |
| Semantic & Contextual Similarity | 25% |
| Relevant Experience & Tenure | 20% |
| Academic Qualifications | 10% |
| Project Portfolio & Evidence | 10% |
| **Total** | **100%** |

### Overall Compatibility Score:

$$\text{Overall Score} = (\text{Skills} \times 0.35) + (\text{Semantic Similarity} \times 0.25) + (\text{Experience} \times 0.20) + (\text{Education} \times 0.10) + (\text{Projects} \times 0.10)$$

*Each component is normalized to a 0–100 scale before calculating the final score.*

---

## 📁 Project Architecture

```
ai-resume-matcher/
│
├── backend/
│   ├── api/                      # REST API endpoints
│   ├── parser/                   # Resume document parsing
│   ├── nlp/                      # Text preprocessing
│   ├── matching/                 # Scoring and ranking engine
│   ├── database/                 # Data models and storage
│   ├── config.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── index.css
│       └── main.jsx
│
├── sample_data/
│   ├── resumes/
│   └── job_descriptions/
│
├── tests/
│   ├── test_accuracy.py
│   ├── test_api.py
│   ├── test_matching.py
│   ├── test_parser.py
│   ├── test_regression.py
│   └── test_scenarios.py
│
├── MATCHING_ALGORITHM.md
├── TESTING.md
├── INTERVIEW_PREPARATION.md
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

### 1. Clone the Repository
```bash
git clone https://github.com/kaviyadharshini2805/ai-resume-matcher.git
cd ai-resume-matcher
```

### 2. Backend Setup
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Frontend Setup
Open another terminal:
```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

### 4. Access the Application
- **Frontend:** http://127.0.0.1:5173
- **Backend:** http://127.0.0.1:8000
- **API Documentation:** http://127.0.0.1:8000/docs

---

## 🧪 Testing

The project includes an automated Pytest suite covering resume extraction, NLP matching, candidate ranking, API integration, and regression scenarios.

Run the tests:
```bash
python -m pytest tests/ -v
```

---

## 🎯 Current Focus

- Evidence-based resume parsing and information extraction.
- NLP-powered candidate-job compatibility evaluation.
- Explainable candidate ranking and selection reasoning.
- Reliable batch processing and document validation.
- Responsible AI and transparent recruitment workflows.
- Improving matching accuracy and evaluation reliability.

---

## 🔮 Limitations & Future Enhancements

- OCR integration for scanned resumes.
- Transformer-based semantic embeddings.
- PostgreSQL or SQLite integration for persistent storage.
- Recruiter authentication and role-based access control.
- Advanced candidate analytics and reporting.
- Fairness evaluation and scoring calibration.

---

## 📬 Connect

- **Developer:** Kaviyadharshini M
- **GitHub:** [kaviyadharshini2805](https://github.com/kaviyadharshini2805)
- **Project:** [Resume Matcher AI – Intelligence Suite](https://github.com/kaviyadharshini2805/ai-resume-matcher)

> *"Turning resumes into insights. Making recruitment more intelligent."*
