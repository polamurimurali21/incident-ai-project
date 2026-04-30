# 🚀 AI Incident Resolution System

## 📌 Overview
This project is an AI-powered incident management system built using Python and FastAPI.  
It analyzes production issues and provides root cause, fix suggestions, and severity.

---

## 🔧 Features
- Accepts incident issues via API  
- AI-based root cause analysis  
- Suggests fix and severity  
- Stores incidents in SQLite database  
- Detects similar issues to avoid duplication  

---

## 🛠️ Tech Stack
- Python  
- FastAPI  
- SQLite  
- HuggingFace (Free AI Model)  
- Git & GitHub  

---

## ▶️ How to Run

```bash
pip install fastapi uvicorn requests
python -m uvicorn main:app --reload

[Open API Docs](http://127.0.0.1:8000/docs)

API Endpoints
POST /incident

Analyze issue

GET /history

Get all past incidents

```json
{
  "issue": "Payment API failed",
  "root_cause": "Timeout issue",
  "fix": "Retry mechanism",
  "severity": "High"
}