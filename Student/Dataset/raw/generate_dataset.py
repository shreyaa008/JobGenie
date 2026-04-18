import pandas as pd
import numpy as np
import random

np.random.seed(42)
N = 5000

# ─── CONFIG ─────────────────────────────────────────────

# FIX 1: Widened tier gap so Tier 1 >> Tier 2 >> Tier 3 (was too close before)
TIER_BOOST = {"Tier 1": 1.55, "Tier 2": 1.10, "Tier 3": 0.80}
TIER_WEIGHTS = [0.20, 0.45, 0.35]
TIERS = list(TIER_BOOST.keys())

ADVANCED     = {"DSA", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"}
INTERMEDIATE = {"Python", "Java", "React", "AWS", "Docker", "Node.js", "Django"}
BASIC        = {"Excel", "SQL", "HTML/CSS", "JavaScript", "Git", "Linux"}
ALL_SKILLS   = list(ADVANCED | INTERMEDIATE | BASIC)

JOB_ROLES = {
    "Data Scientist":    {"min_cgpa": 7.0, "skills": {"Machine Learning","Deep Learning","Python","TensorFlow"}, "band": (8, 22)},
    "Software Engineer": {"min_cgpa": 6.0, "skills": {"DSA","Python","Java","React"},                           "band": (5, 20)},
    "ML Engineer":       {"min_cgpa": 7.5, "skills": {"Machine Learning","Deep Learning","TensorFlow","Python"}, "band": (10, 28)},
    "Web Developer":     {"min_cgpa": 5.5, "skills": {"React","JavaScript","HTML/CSS"},                         "band": (4, 14)},
    "Data Analyst":      {"min_cgpa": 6.0, "skills": {"SQL","Excel","Python"},                                  "band": (4, 12)},
    "DevOps Engineer":   {"min_cgpa": 6.5, "skills": {"Docker","AWS","Linux"},                                  "band": (7, 18)},
    "Backend Developer": {"min_cgpa": 6.0, "skills": {"Java","Python","Docker","SQL"},                          "band": (5, 16)},
    "Junior Developer":  {"min_cgpa": 4.0, "skills": {"Python","JavaScript"},                                   "band": (3, 8)},
}

# ─── FUNCTIONS ─────────────────────────────────────────

def assign_job_role(skills, cgpa, adv_count):
    # Force ML roles if strong advanced skills
    if adv_count >= 2 and cgpa >= 6.5:
        return random.choice(["ML Engineer", "Data Scientist"])

    candidates = []
    for role, info in JOB_ROLES.items():
        if cgpa < info["min_cgpa"]:
            continue
        if cgpa >= 7.5 and role == "Junior Developer":
            continue

        overlap = len(set(skills) & info["skills"])
        candidates.append((role, overlap))

    if not candidates:
        return "Junior Developer"

    candidates.sort(key=lambda x: (x[1], cgpa), reverse=True)
    return candidates[0][0]


def generate_aptitude(cgpa, adv):
    score = cgpa * 7 + adv * 4 + np.random.normal(0, 5)
    return round(np.clip(score, 10, 100), 1)


def apply_cgpa_cap(salary, cgpa):
    caps = [(5.5, 4.5), (6.0, 6.0), (7.0, 10.0), (8.0, 16.0), (9.0, 24.0)]
    for t, cap in caps:
        if cgpa < t:
            return min(salary, cap)
    return salary


def apply_skill_cap(salary, adv, inter):
    if adv == 0:
        salary = min(salary, 13)
    if adv == 0 and inter == 0:
        salary = min(salary, 8)
    return salary


def apply_tier_boost(salary, tier, cgpa):
    if cgpa >= 6:
        return salary * TIER_BOOST[tier]
    return salary


def calculate_salary(cgpa, adv, inter, basic,
                     internships, github_projects,
                     aptitude, backlogs,
                     hackathons, certifications,        # FIX 2: added new params
                     tier, band):

    salary = 2.5

    # Core academics
    salary += (cgpa - 5) * 1.6
    salary += adv   * 3.2
    salary += inter * 1.4
    salary += basic * 0.4

    # Experience
    project_score = min(github_projects * 0.8, 3)      # renamed projects → github_projects
    salary += internships * 1.0
    salary += project_score

    # Aptitude
    salary += (aptitude / 100) * 3.0

    # FIX 3: hackathons & certifications now affect salary
    salary += hackathons     * 0.5
    salary += certifications * 0.4

    # Backlog penalty
    salary -= backlogs * random.uniform(0.7, 1.2)

    # High CGPA bonus
    if cgpa > 8.5:
        salary += random.uniform(2, 4)

    # Modular rules
    salary = apply_tier_boost(salary, tier, cgpa)
    salary = apply_cgpa_cap(salary, cgpa)
    salary = apply_skill_cap(salary, adv, inter)

    # Skill weakness penalty
    if adv == 0:
        salary *= 0.8

    # Role band
    salary = max(band[0] * 0.7, min(salary, band[1] * 1.1))

    salary += np.random.normal(0, 0.3)

    return round(max(2.0, min(salary, 45.0)), 2)


def generate_student():
    tier = random.choices(TIERS, weights=TIER_WEIGHTS)[0]
    cgpa = round(np.clip(np.random.normal(7, 1.2), 4, 10), 2)

    internships     = int(np.random.poisson(1))
    github_projects = int(np.random.poisson(2))              # FIX 2: renamed from projects
    backlogs        = int(np.random.poisson(0.5 if cgpa > 7 else 1))

    # FIX 2: three new columns added
    hackathons      = int(np.clip(np.random.poisson(1.5), 0, 8))
    certifications  = int(np.clip(np.random.poisson(2),   0, 8))

    num_skills = random.randint(1, min(6, int(cgpa // 2) + 2))
    skills     = random.sample(ALL_SKILLS, num_skills)

    adv   = len(set(skills) & ADVANCED)
    inter = len(set(skills) & INTERMEDIATE)
    basic = len(set(skills) & BASIC)

    aptitude = generate_aptitude(cgpa, adv)
    role     = assign_job_role(skills, cgpa, adv)
    band     = JOB_ROLES[role]["band"]

    salary = calculate_salary(
        cgpa, adv, inter, basic,
        internships, github_projects,
        aptitude, backlogs,
        hackathons, certifications,                          # FIX 2: passed to salary calc
        tier, band
    )

    return {
        "college_tier":      tier,
        "cgpa":              cgpa,
        "internships":       internships,
        "github_projects":   github_projects,                # FIX 2: renamed column
        "backlogs":          backlogs,
        "hackathons":        hackathons,                     # FIX 2: new column
        "certifications":    certifications,                 # FIX 2: new column
        "skills":            ", ".join(skills),
        "advanced_skills":   adv,
        "intermediate_skills": inter,
        "basic_skills":      basic,
        "aptitude_score":    aptitude,
        "job_role":          role,
        "salary_lpa":        salary
    }


# ─── GENERATE DATASET ──────────────────────────────────

data = pd.DataFrame([generate_student() for _ in range(N)])

data.to_csv("student_salary_dataset.csv", index=False)

print("✅ Dataset generated successfully!")
print(data.head())