"""
test_api.py — Run this to test your Flask API without a browser.
Make sure app.py is running first (python app.py), then run this file.
"""
import requests
import json

BASE = "http://localhost:5000"

def test(name, payload, expect_role=None, salary_min=None, salary_max=None):
    r = requests.post(f"{BASE}/predict", json=payload)
    d = r.json()
    salary = d.get('predicted_salary_lpa', 0)
    role   = d.get('predicted_role', '')
    top    = d.get('top_roles', [])
    imps   = d.get('improvements', [])

    role_ok   = (expect_role is None) or (role in expect_role)
    salary_ok = (salary_min is None) or (salary_min <= salary <= salary_max)
    status    = "PASS" if (role_ok and salary_ok) else "FAIL"

    print(f"[{status}] {name}")
    print(f"       Role: {role}  |  Salary: {salary} LPA")
    print(f"       Top-3: {[(t['role'], t['confidence']) for t in top[:2]]}")
    print(f"       Improvements ({len(imps)}): {[i['message'][:50] for i in imps[:2]]}")
    print()

print("=" * 60)
print("  API TESTS")
print("=" * 60)
print()

# Test 1
test("Strong ML student",
    {"college_tier":"Tier 1","cgpa":9.0,"internships":2,"github_projects":4,
     "backlogs":0,"hackathons":3,"certifications":4,"aptitude_score":85.0,
     "skills":["Machine Learning","Deep Learning","TensorFlow","Python"]},
    expect_role=["ML Engineer","Data Scientist"], salary_min=18, salary_max=40)

# Test 2
test("Web developer",
    {"college_tier":"Tier 2","cgpa":7.0,"internships":1,"github_projects":2,
     "backlogs":0,"hackathons":1,"certifications":2,"aptitude_score":55.0,
     "skills":["React","JavaScript","HTML/CSS","Node.js"]},
    expect_role=["Web Developer"], salary_min=5, salary_max=14)

# Test 3 — validation error
print("Testing validation (empty skills list):")
r = requests.post(f"{BASE}/predict", json={
    "college_tier":"Tier 2","cgpa":7.0,"internships":1,"github_projects":2,
    "backlogs":0,"hackathons":1,"certifications":2,"aptitude_score":55.0,
    "skills":[]
})
print(f"  Status: {r.status_code}  |  Response: {r.json()}")
print()

print("=" * 60)
print("  Health check:")
r = requests.get(f"{BASE}/health")
print(f"  {r.json()}")
print("=" * 60)