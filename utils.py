import requests
import fitz  # PyMuPDF

# 🔹 Ollama query
def query(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )
    data = response.json()
    return data.get("response", "")


# 🔹 RULE-BASED KEYWORD EXTRACTION (NO AI)
def keyword(jd):
    jd = jd.lower()

    skills = [
        "python", "java", "c++", "javascript",
        "html", "css", "react",
        "django", "flask",
        "mysql", "mongodb", "sql",
        "rest api", "git", "aws",
        "data structures", "algorithms",
        "web development", "backend development",
        "system design"
    ]

    keywords = []

    for skill in skills:
        if skill in jd:
            keywords.append(skill)

    return keywords


# 🔹 EXTRACT TEXT FROM PDF
def extract_text(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text.lower()


# 🔹 SYNONYMS (SMART MATCHING)
synonyms = {
    "web development": ["html", "css", "javascript", "react"],
    "backend development": ["api", "server", "database"],
    "rest api": ["api", "rest"],
    "databases": ["mysql", "mongodb", "sql"],
}
# 🔹 FINAL ANALYSIS
def analyze(resume_text, keywords):
    matched = []
    missing = []
    total = 0
    score = 0
    for i in range(len(keywords)):
        word = keywords[i]
        weight = 2 if i < 5 else 1
        total += weight
        words = word.split()
        # exact match
        if word in resume_text:
            matched.append(word)
            score += weight
        # synonym match
        elif word in synonyms:
            if any(s in resume_text for s in synonyms[word]):
                matched.append(word)
                score += weight
            else:
                missing.append(word)
        # strict partial match
        elif all(w in resume_text for w in words):
            matched.append(word)
            score += weight
        else:
            missing.append(word)
    # base score
    score = int((score / total) * 100) if total > 0 else 0
    # bonus
    action = ["developed", "built", "implemented", "designed"]
    for a in action:
        if a in resume_text:
            score += 2
    # penalties
    if "experience" not in resume_text:
        score -= 10
    if "skills" not in resume_text:
        score -= 5
    # clamp (VERY IMPORTANT)
    score = max(0, min(score, 100))
    return score, matched, missing