from fastapi import FastAPI
import requests
import sqlite3
import json

app = FastAPI()

# 🗄️ Database setup
conn = sqlite3.connect("incidents.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue TEXT,
    root_cause TEXT,
    fix TEXT,
    severity TEXT
)
""")
conn.commit()


# 🏠 Home API
@app.get("/")
def home():
    return {"message": "Incident AI Running 🚀"}


# 🤖 AI function
def analyze_issue(issue):
    url = "https://api-inference.huggingface.co/models/google/flan-t5-base"

    payload = {
        "inputs": f"""
        You are a senior support engineer.

        Analyze this issue: {issue}

        Respond ONLY in JSON like this:
        {{
          "root_cause": "...",
          "fix": "...",
          "severity": "Low/Medium/High"
        }}
        """
    }

    response = requests.post(url, json=payload)

    try:
        result = response.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "")
        return ""
    except:
        return ""


# 🧠 Format output
def format_output(text):
    try:
        data = json.loads(text)

        return (
            data.get("root_cause", "Not identified"),
            data.get("fix", "Not identified"),
            data.get("severity", "Medium")
        )
    except:
        return ("Not identified", "Not identified", "Medium")


# 🔍 Similar issue check
def find_similar_issue(issue):
    cursor.execute("SELECT issue, root_cause, fix, severity FROM incidents")
    data = cursor.fetchall()

    for row in data:
        if issue.lower() in row[0].lower():
            return {
                "matched_issue": row[0],
                "root_cause": row[1],
                "fix": row[2],
                "severity": row[3]
            }
    return None


# 🚀 Main API
@app.post("/incident")
def create_incident(issue: str):
    try:
        # 🔍 Check similar issue first
        similar = find_similar_issue(issue)

        if similar:
            return {
                "message": "Similar issue found",
                "data": similar
            }

        # 🤖 AI analysis
        ai_text = analyze_issue(issue)
        root, fix, severity = format_output(ai_text)

        # fallback (AI fail అయితే)
        if root == "Not identified":
            root = "Possible timeout or network issue"
            fix = "Check API logs, retry mechanism, server status"
            severity = "High"

        # 💾 Save to DB
        cursor.execute(
            "INSERT INTO incidents (issue, root_cause, fix, severity) VALUES (?, ?, ?, ?)",
            (issue, root, fix, severity)
        )
        conn.commit()

        return {
            "issue": issue,
            "root_cause": root,
            "fix": fix,
            "severity": severity
        }

    except Exception as e:
        return {"error": str(e)}


# 📜 History API
@app.get("/history")
def get_history():
    cursor.execute("SELECT * FROM incidents")
    data = cursor.fetchall()

    return {"history": data}