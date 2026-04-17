# import pandas as pd
# import numpy as np
# import random

# np.random.seed(42)
# N = 3000

# # 🎓 College Tier
# TIER_BOOST = {"Tier 1": 1.3, "Tier 2": 1.1, "Tier 3": 0.9}
# TIERS = list(TIER_BOOST.keys())

# # 🧠 Skills categorized
# ADVANCED = {"DSA", "Machine Learning", "Deep Learning", "TensorFlow"}
# INTERMEDIATE = {"Python", "Java", "React", "AWS", "Docker"}
# BASIC = {"Excel", "SQL", "HTML/CSS", "JavaScript"}

# ALL_SKILLS = list(ADVANCED | INTERMEDIATE | BASIC)

# def generate_student():
#     tier = random.choice(TIERS)
#     cgpa = round(np.clip(np.random.normal(7.0, 1.2), 4.0, 10.0), 2)
#     internships = max(0, int(np.random.poisson(1.2)))
#     projects = max(0, int(np.random.poisson(3)))
#     backlogs = max(0, int(np.random.poisson(0.5 if cgpa > 7 else 1.2)))

#     # 🎯 Select skills
#     num_skills = random.randint(1, 5)
#     skills = random.sample(ALL_SKILLS, num_skills)

#     # Count skill types
#     advanced_count = len([s for s in skills if s in ADVANCED])
#     intermediate_count = len([s for s in skills if s in INTERMEDIATE])
#     basic_count = len([s for s in skills if s in BASIC])

#     # ───────── SALARY CALCULATION (FIXED LOGIC) ───────── #

#     salary = 2.5  # base

#     # 🔹 CGPA (strong impact)
#     salary += (cgpa - 5) * 1.5

#     # 🔹 Skills (quality-based)
#     salary += advanced_count * 3.0
#     salary += intermediate_count * 1.5
#     salary += basic_count * 0.5

#     # 🔹 Experience
#     salary += internships * 0.8
#     salary += projects * 0.2

#     # 🔻 Penalty
#     salary -= backlogs * 1.0

#     # 🔹 Tier boost (controlled)
#     # Apply tier boost ONLY if CGPA >= 6
#     if cgpa >= 6:
#         salary *= TIER_BOOST[tier]

#     # ❗ LOGIC RULES (VERY IMPORTANT)
    
#     # ❗ FINAL CGPA-BASED CAPS (STRICT CONTROL)
    
#     if cgpa < 6:
#         salary = min(salary, 5)

#     elif cgpa < 7:
#         salary = min(salary, 10)
    
#     elif cgpa < 8:
#         salary = min(salary, 14)
    
#     elif cgpa < 9:
#         salary = min(salary, 20)
        
    
#     # ❗ SKILL-BASED CEILING (FINAL REALISM FIX)

# # If no advanced skills → limit high packages
#     if advanced_count == 0:
#         salary = min(salary, 12)

# # If only basic skills → stricter cap
#     if advanced_count == 0 and intermediate_count == 0:
#         salary = min(salary, 8)
#     # Small randomness
#     salary += np.random.normal(0, 0.2)

#     salary = round(max(2.0, min(salary, 40.0)), 2)
    
#     # 🎯 Soft scaling for mid CGPA (7–8 range)
#     if 7 <= cgpa < 8:
#         salary *= np.random.uniform(0.85, 0.95)

#     return {
#         "college_tier": tier,
#         "cgpa": cgpa,
#         "internships": internships,
#         "projects": projects,
#         "backlogs": backlogs,
#         "skills": ", ".join(skills),
#         "advanced_skills": advanced_count,
#         "intermediate_skills": intermediate_count,
#         "basic_skills": basic_count,
#         "salary_lpa": salary
#     }

# # 🚀 Generate dataset
# data = pd.DataFrame([generate_student() for _ in range(N)])

# # 💾 Save to CSV
# data.to_csv("student_salary_dataset.csv", index=False)

# print("✅ Dataset created successfully!")
# print("📁 File saved as: student_salary_dataset.csv")
# print(data.head())












# import pandas as pd
# import numpy as np
# import random

# np.random.seed(42)
# N = 5000

# # ─── CONFIG ─────────────────────────────────────────────
# TIER_BOOST = {"Tier 1": 1.25, "Tier 2": 1.08, "Tier 3": 0.90}
# TIER_WEIGHTS = [0.20, 0.45, 0.35]
# TIERS = list(TIER_BOOST.keys())

# ADVANCED = {"DSA", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"}
# INTERMEDIATE = {"Python", "Java", "React", "AWS", "Docker", "Node.js", "Django"}
# BASIC = {"Excel", "SQL", "HTML/CSS", "JavaScript", "Git", "Linux"}
# ALL_SKILLS = list(ADVANCED | INTERMEDIATE | BASIC)

# JOB_ROLES = {
#     "Data Scientist":    {"min_cgpa": 7.0, "skills": {"Machine Learning","Deep Learning","Python","TensorFlow"}, "band": (8, 22)},
#     "Software Engineer": {"min_cgpa": 6.0, "skills": {"DSA","Python","Java","React"},                           "band": (5, 20)},
#     "ML Engineer":       {"min_cgpa": 7.5, "skills": {"Machine Learning","Deep Learning","TensorFlow","Python"},"band": (10, 28)},
#     "Web Developer":     {"min_cgpa": 5.5, "skills": {"React","JavaScript","HTML/CSS"},                         "band": (4, 14)},
#     "Data Analyst":      {"min_cgpa": 6.0, "skills": {"SQL","Excel","Python"},                                  "band": (4, 12)},
#     "DevOps Engineer":   {"min_cgpa": 6.5, "skills": {"Docker","AWS","Linux"},                                  "band": (7, 18)},
#     "Backend Developer": {"min_cgpa": 6.0, "skills": {"Java","Python","Docker","SQL"},                          "band": (5, 16)},
#     "Junior Developer":  {"min_cgpa": 4.0, "skills": {"Python","JavaScript"},                                   "band": (3, 8)},
# }

# # ─── FUNCTIONS ─────────────────────────────────────────

# def assign_job_role(skills, cgpa):
#     candidates = []
#     for role, info in JOB_ROLES.items():
#         if cgpa < info["min_cgpa"]:
#             continue
#         if cgpa >= 7.5 and role == "Junior Developer":
#             continue
#         overlap = len(set(skills) & info["skills"])
#         candidates.append((role, overlap))

#     if not candidates:
#         return "Junior Developer"
    
#     candidates.sort(key=lambda x: x[1] + random.uniform(-0.3, 0.3), reverse=True)
#     return candidates[0][0]


# def generate_aptitude(cgpa, advanced_count):
#     score = cgpa * 7 + advanced_count * 4 + np.random.normal(0, 5)
#     return round(np.clip(score, 10, 100), 1)


# def apply_cgpa_cap(salary, cgpa):
#     caps = [
#         (5.5, 4.5),
#         (6.0, 6.0),
#         (7.0, 10.0),
#         (8.0, 16.0),
#         (9.0, 24.0),
#     ]
#     for threshold, cap in caps:
#         if cgpa < threshold:
#             return min(salary, cap)
#     return salary


# def apply_skill_cap(salary, adv, inter):
#     if adv == 0:
#         salary = min(salary, 13)
#     if adv == 0 and inter == 0:
#         salary = min(salary, 8)
#     return salary


# def apply_tier_boost(salary, tier, cgpa):
#     if cgpa >= 6:
#         return salary * TIER_BOOST[tier]
#     return salary


# def calculate_salary(cgpa, adv, inter, basic,
#                      internships, projects,
#                      aptitude, backlogs,
#                      tier, band):

#     salary = 2.5

#     salary += (cgpa - 5) * 1.6
#     salary += adv * 3.2
#     salary += inter * 1.4
#     salary += basic * 0.4

#     salary += internships * 1.0
#     salary += projects * 0.25
#     salary += (aptitude / 100) * 3.0

#     salary -= backlogs * 1.2
#     salary = apply_tier_boost(salary, tier, cgpa)
#     salary = apply_cgpa_cap(salary, cgpa)
#     salary = apply_skill_cap(salary, adv, inter)
#     if ADVANCED == 0 and INTERMEDIATE == 0:
#         salary *= 0.85
#     salary = max(band[0] * 0.7, min(salary, band[1] * 1.1))

#     salary += np.random.normal(0, 0.3)

#     return round(max(2.0, min(salary, 45.0)), 2)


# def generate_student():
#     tier = random.choices(TIERS, weights=TIER_WEIGHTS)[0]
#     cgpa = round(np.clip(np.random.normal(7, 1.2), 4, 10), 2)

#     internships = int(np.random.poisson(1))
#     projects = int(np.random.poisson(2))
#     backlogs = int(np.random.poisson(0.5 if cgpa > 7 else 1))

#     num_skills = random.randint(1, min(6, int(cgpa // 2) + 2))
#     skills = random.sample(ALL_SKILLS, num_skills)

#     adv = len(set(skills) & ADVANCED)
#     inter = len(set(skills) & INTERMEDIATE)
#     basic = len(set(skills) & BASIC)

#     aptitude = generate_aptitude(cgpa, adv)
#     role = assign_job_role(skills, cgpa)
#     band = JOB_ROLES[role]["band"]

#     salary = calculate_salary(
#         cgpa, adv, inter, basic,
#         internships, projects,
#         aptitude, backlogs,
#         tier, band
#     )

#     return {
#         "college_tier": tier,
#         "cgpa": cgpa,
#         "internships": internships,
#         "projects": projects,
#         "backlogs": backlogs,
#         "skills": ", ".join(skills),
#         "advanced_skills": adv,
#         "intermediate_skills": inter,
#         "basic_skills": basic,
#         "aptitude_score": aptitude,
#         "job_role": role,
#         "salary_lpa": salary
#     }


# # ─── GENERATE DATASET ─────────────────────────────────

# data = pd.DataFrame([generate_student() for _ in range(N)])

# data.to_csv("student_salary_dataset.csv", index=False)

# print("✅ Dataset generated successfully!")
# print("📁 File saved as: student_salary_dataset.csv")
# print(data.head())










import pandas as pd
import numpy as np
import random

np.random.seed(42)
N = 5000

# ─── CONFIG ─────────────────────────────────────────────
TIER_BOOST = {"Tier 1": 1.25, "Tier 2": 1.08, "Tier 3": 0.90}
TIER_WEIGHTS = [0.20, 0.45, 0.35]
TIERS = list(TIER_BOOST.keys())

ADVANCED = {"DSA", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"}
INTERMEDIATE = {"Python", "Java", "React", "AWS", "Docker", "Node.js", "Django"}
BASIC = {"Excel", "SQL", "HTML/CSS", "JavaScript", "Git", "Linux"}
ALL_SKILLS = list(ADVANCED | INTERMEDIATE | BASIC)

JOB_ROLES = {
    "Data Scientist":    {"min_cgpa": 7.0, "skills": {"Machine Learning","Deep Learning","Python","TensorFlow"}, "band": (8, 22)},
    "Software Engineer": {"min_cgpa": 6.0, "skills": {"DSA","Python","Java","React"}, "band": (5, 20)},
    "ML Engineer":       {"min_cgpa": 7.5, "skills": {"Machine Learning","Deep Learning","TensorFlow","Python"}, "band": (10, 28)},
    "Web Developer":     {"min_cgpa": 5.5, "skills": {"React","JavaScript","HTML/CSS"}, "band": (4, 14)},
    "Data Analyst":      {"min_cgpa": 6.0, "skills": {"SQL","Excel","Python"}, "band": (4, 12)},
    "DevOps Engineer":   {"min_cgpa": 6.5, "skills": {"Docker","AWS","Linux"}, "band": (7, 18)},
    "Backend Developer": {"min_cgpa": 6.0, "skills": {"Java","Python","Docker","SQL"}, "band": (5, 16)},
    "Junior Developer":  {"min_cgpa": 4.0, "skills": {"Python","JavaScript"}, "band": (3, 8)},
}

# ─── FUNCTIONS ─────────────────────────────────────────

def assign_job_role(skills, cgpa, adv_count):
    # 🔥 Force ML roles if strong advanced skills
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

    # include CGPA in decision
    candidates.sort(key=lambda x: (x[1], cgpa), reverse=True)
    return candidates[0][0]


def generate_aptitude(cgpa, adv):
    score = cgpa * 7 + adv * 4 + np.random.normal(0, 5)
    return round(np.clip(score, 10, 100), 1)


def apply_cgpa_cap(salary, cgpa):
    caps = [(5.5,4.5),(6.0,6.0),(7.0,10.0),(8.0,16.0),(9.0,24.0)]
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
                     internships, projects,
                     aptitude, backlogs,
                     tier, band):

    salary = 2.5

    # core
    salary += (cgpa - 5) * 1.6
    salary += adv * 3.2
    salary += inter * 1.4
    salary += basic * 0.4

    # experience (capped projects)
    project_score = min(projects * 0.8, 3)
    salary += internships * 1.0
    salary += project_score

    # aptitude
    salary += (aptitude / 100) * 3.0

    # backlog penalty (stronger)
    salary -= backlogs * random.uniform(0.7, 1.2)

    # high CGPA bonus
    if cgpa > 8.5:
        salary += random.uniform(2, 4)

    # modular rules
    salary = apply_tier_boost(salary, tier, cgpa)
    salary = apply_cgpa_cap(salary, cgpa)
    salary = apply_skill_cap(salary, adv, inter)

    # 🔥 skill weakness penalty
    if adv == 0:
        salary *= 0.8

    # role band
    salary = max(band[0]*0.7, min(salary, band[1]*1.1))

    salary += np.random.normal(0, 0.3)

    return round(max(2.0, min(salary, 45.0)), 2)


def generate_student():
    tier = random.choices(TIERS, weights=TIER_WEIGHTS)[0]
    cgpa = round(np.clip(np.random.normal(7,1.2),4,10),2)

    internships = int(np.random.poisson(1))
    projects = int(np.random.poisson(2))
    backlogs = int(np.random.poisson(0.5 if cgpa>7 else 1))

    num_skills = random.randint(1, min(6,int(cgpa//2)+2))
    skills = random.sample(ALL_SKILLS, num_skills)

    adv = len(set(skills) & ADVANCED)
    inter = len(set(skills) & INTERMEDIATE)
    basic = len(set(skills) & BASIC)

    aptitude = generate_aptitude(cgpa, adv)
    role = assign_job_role(skills, cgpa, adv)
    band = JOB_ROLES[role]["band"]

    salary = calculate_salary(
        cgpa, adv, inter, basic,
        internships, projects,
        aptitude, backlogs,
        tier, band
    )

    return {
        "college_tier": tier,
        "cgpa": cgpa,
        "internships": internships,
        "projects": projects,
        "backlogs": backlogs,
        "skills": ", ".join(skills),
        "advanced_skills": adv,
        "intermediate_skills": inter,
        "basic_skills": basic,
        "aptitude_score": aptitude,
        "job_role": role,
        "salary_lpa": salary
    }


# ─── GENERATE DATASET ─────────────────────────────────

data = pd.DataFrame([generate_student() for _ in range(N)])

data.to_csv("student_salary_dataset.csv", index=False)

print("✅ Dataset generated successfully!")
print(data.head())