# Semantic Resume Analyzer

AI-powered ATS Resume Analyzer that compares a resume against a job description using **semantic similarity (transformer embeddings)** and **keyword matching (TF-IDF)**.

---

## 🚀 Features

* 📄 Upload resumes in **PDF**, **DOCX**, or **TXT** format
* 🧠 Compute semantic similarity using `all-MiniLM-L6-v2`
* 🔍 Extract important keywords from the job description
* ❌ Identify missing keywords in the resume
* 📊 Generate:

  * Semantic Match Score
  * Keyword Match Percentage
  * Fit Level (Strong / Moderate / Low)
  * Personalized recommendations
* 🌐 Interactive web interface built with Flask and Bootstrap

---

## 🖼️ Demo

### Input

* Upload your resume
* Paste a job description

### Output

* Semantic Match Score (e.g., 87.4%)
* Keyword Match Score (e.g., 76.2%)
* Missing Keywords
* ATS Optimization Recommendations

---

## 🏗️ Tech Stack

### Backend

* Python
* Flask
* Sentence Transformers
* spaCy
* Scikit-learn
* PyMuPDF
* python-docx

### Frontend

* HTML
* CSS
* Bootstrap 5

### NLP Models

* `all-MiniLM-L6-v2`
* `en_core_web_sm`

---

## 📂 Project Structure

```text
semantic-resume-analyzer/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── templates/
│   └── index.html
└── static/
    └── style.css
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/semantic-resume-analyzer.git
cd semantic-resume-analyzer
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

---

## ▶️ Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## 📦 requirements.txt

```txt
Flask
sentence-transformers
scikit-learn
python-docx
PyMuPDF
spacy
torch
```

---

## 🧠 How It Works

### 1. Resume Parsing

The uploaded resume is converted to plain text.

### 2. Text Cleaning

Text is normalized by removing extra spaces and converting to lowercase.

### 3. Semantic Similarity

The resume and job description are embedded using Sentence Transformers.

### 4. Keyword Matching

TF-IDF extracts the most relevant job description keywords and checks which are present in the resume.

### 5. Final Analysis

The system returns:

* Match score
* Keyword coverage
* Missing keywords
* Fit level
* Actionable recommendations

---

## 📊 Example Output

```json
{
  "match_score": 86.74,
  "keyword_match": 78.95,
  "fit_level": "Strong Fit",
  "missing_keywords": [
    "docker",
    "kubernetes",
    "aws"
  ],
  "recommendation": "Consider adding relevant keywords like: aws, docker, kubernetes."
}
```

---

## 🎯 Use Cases

* ATS optimization
* Resume tailoring for specific job descriptions
* Career coaching tools
* Recruitment and HR screening
* NLP and semantic similarity demos

---

## 📈 Future Enhancements

* PDF report generation
* Authentication and user dashboards
* Resume section-level analysis
* Skill taxonomy matching
* Multi-language support
* Cloud deployment
* Docker support

---

## 🌍 Deployment Options

* Render
* Railway
* Docker
* AWS Elastic Beanstalk
* Azure App Service

---

## 🧪 API Usage

### Endpoint

```http
POST /analyze_resume
```

### Form Data

| Field           | Type | Description             |
| --------------- | ---- | ----------------------- |
| file            | File | Resume (PDF, DOCX, TXT) |
| job_description | Text | Job description         |

### Response

JSON containing match score, keyword match, missing keywords, fit level, and recommendation.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Nikhil Dasari**

* GitHub: [https://github.com/your-username](https://github.com/your-username)
* LinkedIn: [https://www.linkedin.com/in/your-profile](https://www.linkedin.com/in/your-profile)

---

## ⭐ Support

If you found this project useful, please consider giving it a star on GitHub.

---

## 🏷️ GitHub Topics

```text
python flask nlp machine-learning sentence-transformers semantic-similarity spacy scikit-learn ats resume-analyzer
```

---

## 💡 Project Summary

Semantic Resume Analyzer is an end-to-end NLP application that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) using transformer embeddings and keyword analysis.
