# Matching & Ranking Algorithm Documentation
## Resume Matcher AI – Intelligence Suite

---

## 1. Overview & Core Philosophy

The **Resume Matcher AI** engine evaluates candidate resumes against job descriptions through an **evidence-based, 5-component weighted architecture**. Unlike naive keyword counters that treat any mention of a word as full qualification, this engine:

1. **Distinguishes exact matches from related skills** (e.g. Flask is recognized as related to FastAPI, but is never falsely reported as an exact match).
2. **Maintains strict evidence tracking**, recording the exact resume sentence or line that supports each claimed skill.
3. **Separates internship tenure from full-time professional experience**, ensuring academic project duration or university enrollment is never counted as professional employment.
4. **Validates educational qualifications against explicit resume text**, prohibiting the fabrication of degrees (e.g. bachelor's degrees never trigger an assumed master's degree).
5. **Generates an executive ranking and top-candidate selection rationale** for HR administrators evaluating applicant batches.

---

## 2. 5-Component Normalized Scoring Formula

Every candidate is evaluated across five distinct dimensions, each normalized to a standard **0–100 scale**. The composite compatibility score is computed as follows:

$$\text{Overall Score} = (\text{Skills} \times 0.35) + (\text{Semantic Similarity} \times 0.25) + (\text{Experience} \times 0.20) + (\text{Education} \times 0.10) + (\text{Projects} \times 0.10)$$

### Weight Configuration Table

| Component | Weight | Metric Basis | Normalized Scale |
| :--- | :---: | :--- | :---: |
| **Technical Skills Match** | **35%** | Exact match ratio of mandatory required (85% weight) and preferred skills (15% weight) | 0–100 |
| **Semantic & Contextual Similarity** | **25%** | TF-IDF Cosine Similarity between candidate text and job description | 0–100 |
| **Relevant Experience & Tenure** | **20%** | Comparative assessment of candidate professional tenure / internship against stated JD criteria | 0–100 |
| **Academic Qualifications** | **10%** | Explicit degree level alignment (Ph.D., Master's, Bachelor's) vs role education target | 0–100 |
| **Project Portfolio & Evidence** | **10%** | Count of documented practical projects and verified skill implementation evidence | 0–100 |

---

## 3. Component Details & Mathematical Formulations

### Component 1: Technical Skills Match (35%)
- **Extraction:** Skills are detected using strict word-boundary regular expressions across canonical taxonomies (Programming Languages, Machine Learning, Deep Learning, NLP & Generative AI, Backend Frameworks, Databases, Cloud & DevOps).
- **Separation:** Job requirements are split into **Required (Mandatory)** and **Preferred (Optional)** buckets based on section headings.
- **Formula:**
  $$\text{Skills Score} = \left( \frac{|\text{Matched}_{\text{req}}|}{|\text{Total}_{\text{req}}|} \times 0.85 + \frac{|\text{Matched}_{\text{pref}}|}{|\text{Total}_{\text{pref}}|} \times 0.15 \right) \times 100$$
- **Related Skills Map:** If a candidate has `Flask` and the job requests `FastAPI`, the engine tags `Flask` as a *related transferable skill* under `related_skills`, providing transparency without falsely marking `FastAPI` as matched.

### Component 2: Semantic Similarity (25%)
- **Text Vectorization:** Evaluates global semantic alignment using TF-IDF (Term Frequency - Inverse Document Frequency) with sublinear term frequency scaling and n-gram representations.
- **Cosine Similarity:**
  $$\text{Cosine Similarity}(u, v) = \frac{u \cdot v}{\|u\|_2 \|v\|_2}$$
- **Normalization:** In resume-to-job matching, a dense 400-word resume against an 80-word JD yields raw cosine similarities between 0.05 and 0.45. To normalize this onto a meaningful 0–100 scale:
  $$\text{Semantic Score} = \min\left( \frac{\text{Cosine Similarity}}{0.38} \times 100, 100.0 \right)$$

### Component 3: Relevant Experience (20%)
- **Duration Parsing:** Extracts employment intervals (`Month Year – Month Year`, `Month Year – Present`, or `Year – Year`).
- **Interval Merging:** Overlapping employment dates are merged to prevent double-counting.
- **Internship Isolation:** Lines containing internship or trainee keywords are sequestered into `internship_months` and never added to `professional_years`.
- **Comparative Logic:**
  - *Fresher / Entry-Level JD (0–2 years):* Candidates with 3-month internships or 0–2 years receive full score (90–100%).
  - *Senior JD (4+ or 5+ years):* Candidates lacking professional tenure receive a scaled proportional score (15–40%), explicitly surfacing an experience mismatch.

### Component 4: Education & Qualifications (10%)
- **Degree Detection:** Strict boundary identification of Ph.D., Master's (M.Tech, M.E., M.S., MBA), and Bachelor's (B.E., B.Tech, B.S., B.Sc).
- **Scoring:**
  - Exceeds target (e.g. Ph.D. for Bachelor's role): 100%.
  - Meets target (e.g. B.E. for Bachelor's role): 100%.
  - Partial match (e.g. Bachelor's for Ph.D. role): 45–70%.
  - Unspecified / Non-degree bootcamp only: 35–50%.

### Component 5: Projects & Portfolio Evidence (10%)
- **Project Extraction:** Parses dedicated project titles, descriptions, and technology associations.
- **Alignment:** Verifies whether candidate projects demonstrate practical application of the target job skills.
  - $\ge 3$ documented projects with $\ge 2$ target skills: 95%.
  - $\ge 1$ documented project: 75–90%.
  - Work-experience skill mentions without dedicated portfolio: 65–70%.
  - No project portfolio: 40%.

---

## 4. Multi-Resume Ranking & Top Candidate Rationale

When evaluating an applicant batch, the engine:

1. **Sorts all candidates** in descending order of composite `Overall Score`.
2. **Assigns explicit ranks** (`#1`, `#2`, `#3` ...).
3. **Formulates an Executive Selection Rationale** for Rank #1:
   - **Composite Score Leader:** Explains the numerical margin and balance across all 5 components.
   - **Core Technical Match:** Lists verified skills with supporting resume evidence.
   - **Experience & Education Fit:** Validates alignment with the specific JD tenure and degree criteria.
   - **Comparative Edge Over Runners-Up:** Explicitly identifies what the #1 candidate possesses that #2 and #3 lack (e.g., missing mandatory skills, tenure deficits).

---

## 5. Ethical Guidelines & Assumptions

- **Zero Hallucination:** The system never guesses or assumes missing information; if a field is absent, it reports `"Not specified in resume"`.
- **Protected Characteristics Shield:** Candidate ranking does not consider age, gender, race, religion, nationality, or photographs.
- **Human-in-the-Loop:** All automated evaluations serve as decision-support intelligence for HR professionals, not autonomous hiring gates.
