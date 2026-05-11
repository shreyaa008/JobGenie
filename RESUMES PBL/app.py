import os
import shutil

import joblib
import pandas as pd
from flask import Flask, render_template, request

from config import (
    NER_MODEL_PATH,
    RANKING_MODEL_PATH,
    FEATURE_COLS_PATH,
    SCALER_PATH,
    UPLOADS_DIR,
)
from utils.parser import load_ner_model, parse_resume
from utils.ranker import rank_uploaded_resumes

app = Flask(__name__)

# ── Load all models once at startup ──────────────────────────────────────────

nlp, use_ner        = load_ner_model(NER_MODEL_PATH)
model               = joblib.load(RANKING_MODEL_PATH)
scaler              = joblib.load(SCALER_PATH)
feature_cols        = joblib.load(FEATURE_COLS_PATH)

print("All models loaded")

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/screen", methods=["POST"])
def screen():

    # ── Read and validate form inputs ─────────────────────────────────────────
    try:
        min_exp = float(request.form.get("min_exp", 0))
    except (ValueError, TypeError):
        min_exp = 0.0

    try:
        min_salary = float(request.form.get("min_salary", 0))
    except (ValueError, TypeError):
        min_salary = 0.0

    try:
        max_salary = float(request.form.get("max_salary", 10000000))
    except (ValueError, TypeError):
        max_salary = 10000000.0

    try:
        top_n = int(request.form.get("top_n", 5))
        top_n = max(1, min(top_n, 50))
    except (ValueError, TypeError):
        top_n = 5

    if min_salary > max_salary:
        min_salary, max_salary = max_salary, min_salary

    skills_raw     = request.form.get("skills", "")
    required_skills = [s.strip() for s in skills_raw.split(",") if s.strip()]

    # ── Save and parse uploaded PDFs ──────────────────────────────────────────
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    uploaded_files = request.files.getlist("resumes")
    parsed_list    = []

    for pdf_file in uploaded_files:
        if pdf_file and pdf_file.filename.endswith(".pdf"):
            save_path = os.path.join(UPLOADS_DIR, pdf_file.filename)
            try:
                pdf_file.save(save_path)
                parsed = parse_resume(save_path, nlp, use_ner)
                if parsed:
                    parsed_list.append(parsed)
            except Exception as e:
                print(f"  Could not process {pdf_file.filename}: {e}")

    # Clean uploads folder after parsing
    try:
        shutil.rmtree(UPLOADS_DIR)
    except Exception:
        pass

    # ── Auto-detect skills if none provided ───────────────────────────────────
    if not required_skills and parsed_list:
        all_skills = []
        for p in parsed_list:
            all_skills.extend(p.get("skills", []))
        required_skills = list(dict.fromkeys(all_skills))

    # ── Rank resumes ──────────────────────────────────────────────────────────
    ranked = []
    if parsed_list:
        all_ranked = rank_uploaded_resumes(
            parsed_list, required_skills, model, scaler, feature_cols
        )
        # Apply experience filter and take top N
        ranked = [
            r for r in all_ranked
            if r["experience"] >= min_exp
        ][:top_n]

        # Re-rank after filter
        for i, r in enumerate(ranked, 1):
            r["rank"] = i

    return render_template(
        "results.html",
        ranked          = ranked,
        required_skills = required_skills,
        min_exp         = min_exp,
        min_salary      = int(min_salary),
        max_salary      = int(max_salary),
        top_n           = top_n,
        total_uploaded  = len(parsed_list),
        use_ner         = use_ner,
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)