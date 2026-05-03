from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from predictor import predict_student
import traceback

app = Flask(__name__)
CORS(app)

# ── Page routes (serve HTML) ──────────────────────────────────────────────────
@app.route('/')
def index():
    """Student form page"""
    return render_template('index.html')

@app.route('/result')
def result():
    """Result dashboard page"""
    return render_template('result.html')

# ── API routes (JSON) ─────────────────────────────────────────────────────────
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "running"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        required = ['college_tier', 'cgpa', 'internships', 'github_projects',
                    'backlogs', 'hackathons', 'certifications',
                    'aptitude_score', 'skills']
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        if data['college_tier'] not in ['Tier 1', 'Tier 2', 'Tier 3']:
            return jsonify({"error": "college_tier must be Tier 1, Tier 2, or Tier 3"}), 400
        if not (4.0 <= float(data['cgpa']) <= 10.0):
            return jsonify({"error": "CGPA must be between 4.0 and 10.0"}), 400
        if not isinstance(data['skills'], list) or len(data['skills']) == 0:
            return jsonify({"error": "Select at least one skill"}), 400

        result = predict_student(
            college_tier    = data['college_tier'],
            cgpa            = float(data['cgpa']),
            internships     = int(data['internships']),
            github_projects = int(data['github_projects']),
            backlogs        = int(data['backlogs']),
            hackathons      = int(data['hackathons']),
            certifications  = int(data['certifications']),
            aptitude_score  = float(data['aptitude_score']),
            skills          = data['skills']
        )
        return jsonify(result), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("JobGenie running → http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)