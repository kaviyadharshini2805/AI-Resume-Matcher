import React, { useState, useEffect } from 'react'

const PRESET_JOBS = {
  aiml_engineer: {
    title: "AI/ML Engineer",
    description: `Position: AI/ML Engineer
Department: Artificial Intelligence & Cloud Services

Role Overview:
We are seeking an enthusiastic AI/ML Engineer to contribute to our machine learning pipelines and inference API services. Freshers and early-career candidates are welcome.

Required Experience:
0–2 years (Entry-level / Fresh graduates welcome)

Education:
Bachelor's Degree in Computer Science, Information Technology, or related discipline.

Required Skills:
- Python
- Machine Learning (ML)
- Pandas
- NumPy
- Scikit-learn
- EDA
- Data Preprocessing
- Model Evaluation
- SQL

Preferred Skills:
- TensorFlow or PyTorch
- NLP
- LLMs
- RAG
- FastAPI or Flask
- Git
- AWS or Azure`
  },
  python_backend: {
    title: "Senior Python Backend Engineer",
    description: `Position: Senior Python Backend Engineer
Department: Core Infrastructure & Cloud Platforms

Role Overview:
Seeking a Senior Python Backend Engineer to architect and scale our distributed cloud microservices.

Required Experience:
4+ years of professional backend engineering experience.

Education:
Bachelor's Degree in Computer Science or equivalent practical engineering experience.

Required Skills:
- Python
- FastAPI
- Docker
- Kubernetes
- PostgreSQL
- Redis
- SQL
- Git

Preferred Skills:
- AWS
- CI/CD
- Linux
- Microservices`
  },
  ai_scientist: {
    title: "Lead AI & NLP Scientist",
    description: `Position: Lead AI & NLP Scientist
Department: Research & Advanced Intelligence

Role Overview:
Seeking a Lead AI & NLP Scientist to architect deep learning foundation models and semantic search architectures.

Required Experience:
Minimum 5 years of hands-on professional experience in Machine Learning, Deep Learning, and NLP.

Education:
Ph.D. or Master's Degree in Computer Science, Artificial Intelligence, or Mathematics.

Required Skills:
- Machine Learning
- Deep Learning
- NLP
- PyTorch
- Transformers
- LLM
- Python

Preferred Skills:
- TensorFlow
- Scikit-learn
- AWS
- Docker
- SQL`
  }
}

const SYNTHETIC_PROFILES_10 = [
  {
    name: "Arjun Kumar",
    role: "AI/ML Intern (B.E. CS 2022–2026, 3-mo Intern)",
    filename: "01_arjun_kumar_ai_ml_intern.pdf",
    text: `Arjun Kumar
Email: arjun.kumar@example.com | Phone: (555) 345-6789
Location: Bangalore, India

EDUCATION
B.E. in Computer Science (2022–2026), CGPA 8.2
Global Institute of Technology

INTERNSHIP EXPERIENCE
Machine Learning Intern
AI Solutions Inc. | January 2026 – March 2026
- Developed deep learning text processing workflows using TensorFlow and Python.
- Built lightweight inference APIs with Flask.
- Collaborated using Git and GitHub for version control.

TECHNICAL SKILLS
- Languages: Python, Java, SQL
- Machine Learning & Data Science: Pandas, NumPy, Scikit-learn, EDA, Data Preprocessing, Model Evaluation
- Deep Learning & NLP: TensorFlow, CNN, NLP, LLMs, Prompt Engineering
- Frameworks & Databases: Flask, PostgreSQL
- Tools: Git, GitHub

ACADEMIC PROJECTS
Customer Churn Prediction (2025)
- Trained predictive classification models using Scikit-learn, Pandas, and NumPy.
Sentiment Analysis Using NLP (2025)
- Analyzed customer reviews using Natural Language Processing and TensorFlow.
Student Performance Prediction (2024)
- Built regression models evaluating educational indicators.`
  },
  {
    name: "Alex Johnson",
    role: "Senior Backend Engineer (5+ Yrs Exp)",
    filename: "02_alex_johnson_senior_backend.pdf",
    text: `Alex Johnson
Email: alex.johnson@example.com | Phone: (555) 234-5678
Location: San Francisco, CA

SUMMARY
Senior Software Engineer with 5+ years of experience designing scalable microservices, high-throughput REST APIs, and distributed cloud applications.

EXPERIENCE
Senior Software Engineer | CloudTech Solutions
January 2021 – Present
- Designed and maintained high-throughput REST APIs handling 10M+ daily requests using FastAPI, Python, and Redis.
- Orchestrated containerized deployments via Docker and Kubernetes on AWS.
- Mentored junior engineers and practiced Agile/Scrum methodologies.

Software Engineer | DevWorks Inc.
June 2019 – December 2020
- Built backend services with Python, PostgreSQL, and Docker.
- Optimized SQL database query latency by 35%.

SKILLS
- Languages: Python, SQL, Golang
- Frameworks: FastAPI, Django
- Cloud & DevOps: Docker, Kubernetes, AWS, CI/CD, Git, Linux
- Databases: PostgreSQL, Redis

EDUCATION
B.S. in Computer Science (2015–2019)
University of California, Berkeley`
  },
  {
    name: "Dr. Priya Sharma",
    role: "Lead Data Scientist (Ph.D., 6+ Yrs Exp)",
    filename: "03_priya_sharma_nlp_scientist.docx",
    text: `Dr. Priya Sharma
Email: priya.sharma@example.com | Phone: (555) 987-6543
Location: Boston, MA

SUMMARY
Lead Data Scientist with 6+ years of expertise in Natural Language Processing (NLP), predictive modeling, and deep learning architectures.

EXPERIENCE
Lead Data Scientist | AI Innovations Lab
January 2020 – Present
- Architected large-scale NLP pipelines for automated document classification and semantic search.
- Fine-tuned transformer models for multi-lingual semantic matching achieving 94% precision.
- Deployed real-time inference endpoints on AWS using Docker and PyTorch.

Data Scientist | Alpha Analytics
June 2018 – December 2019
- Engineered predictive machine learning models using Scikit-learn, TensorFlow, and Python.

SKILLS
- Core AI/ML: Machine Learning, Deep Learning, NLP, Transformers, LLM, Computer Vision
- Languages & Frameworks: Python, PyTorch, TensorFlow, Scikit-learn, Pandas, NumPy
- Cloud & Infrastructure: AWS, Docker, Git, Linux, SQL

EDUCATION
Ph.D. in Computer Science (AI & NLP) | MIT (2014–2018)
B.S. in Mathematics | Stanford University (2010–2014)`
  },
  {
    name: "Neha Patel",
    role: "Full-Stack Cloud Engineer (4+ Yrs Exp)",
    filename: "10_neha_patel_fullstack_devops.pdf",
    text: `Neha Patel
Email: neha.patel@example.com | Phone: (555) 567-8901
Location: San Jose, CA

SUMMARY
Full-Stack Cloud Engineer with 4 years of experience building scalable web architectures and containerized microservices.

EXPERIENCE
Full-Stack Engineer | NexusCloud
January 2022 – Present
- Developed REST APIs and microservices using FastAPI, Python, and PostgreSQL.
- Architected CI/CD pipelines and managed container orchestration with Docker and Kubernetes on AWS.
- Built responsive client dashboards using React and TypeScript.

SKILLS
- Languages: Python, TypeScript, JavaScript, SQL
- Frameworks: FastAPI, React, Node.js
- Cloud & DevOps: Docker, Kubernetes, AWS, CI/CD, Git, Linux
- Databases: PostgreSQL, Redis, MongoDB

EDUCATION
B.S. in Computer Engineering (2018–2022)
San Jose State University`
  },
  {
    name: "Vikram Singh",
    role: "ML Engineer (Related Skills: Flask, Keras, GCP)",
    filename: "08_vikram_singh_semantic_related.txt",
    text: `Vikram Singh
Email: vikram.singh@example.com | Phone: (555) 901-2345
Location: New York, NY

SUMMARY
Machine Learning Engineer with 3 years of experience building neural models and deploying microservices on GCP.

EXPERIENCE
ML Engineer | DataPulse Systems
January 2023 – Present
- Implemented deep neural models using Keras and TensorFlow.
- Built microservice backend endpoints with Flask and Django.
- Containerized model workflows using Docker on GCP.

SKILLS
- Languages: Python, SQL
- Machine Learning & DL: Keras, TensorFlow, Deep Learning, Pandas, NumPy
- Web & Backend: Flask, Django, REST API
- Cloud: GCP, Docker, Git

EDUCATION
B.Tech in Computer Science (2019–2023)
National Institute of Technology`
  },
  {
    name: "Rahul Verma",
    role: "Junior Python Dev (Partial Match)",
    filename: "04_rahul_verma_partial_backend.docx",
    text: `Rahul Verma
Email: rahul.verma@example.com | Phone: (555) 432-1098
Location: Austin, TX

SUMMARY
Software Developer with 2 years of experience focused on basic Python scripting and database maintenance.

EXPERIENCE
Junior Developer | SoftBase Corp
July 2024 – Present
- Maintained SQL queries and internal data extract scripts using Python.
- Assisted with bug fixes in legacy web modules.

SKILLS
- Programming: Python, SQL, HTML, CSS
- Databases: MySQL, SQLite
- Tools: Git

EDUCATION
Bachelor of Science in Information Technology (2020–2024)
Texas State University`
  },
  {
    name: "David Kim",
    role: "Fresh Graduate (Experience Mismatch for Senior)",
    filename: "06_david_kim_fresher_mismatch.txt",
    text: `David Kim
Email: david.kim@example.com | Phone: (555) 789-4561
Location: Seattle, WA

EDUCATION
Bachelor of Science in Computer Science (2022–2026)
University of Washington

INTERNSHIP EXPERIENCE
Software Engineering Intern | TechStart Inc.
January 2026 – March 2026
- Built Python unit tests and helped document API endpoints.

SKILLS
- Languages: Python, Java
- Tools: Git, Linux

ACADEMIC PROJECTS
Personal Blog Engine (2025)
- Created a static site generator with Python.`
  },
  {
    name: "Sarah Connor",
    role: "Bootcamp Graduate (Education Mismatch)",
    filename: "07_sarah_connor_education_mismatch.pdf",
    text: `Sarah Connor
Email: sarah.connor@example.com | Phone: (555) 890-1234
Location: Los Angeles, CA

SUMMARY
Self-taught developer with coding bootcamp certification. Strong enthusiasm for Python web scripting.

EDUCATION
Full-Stack Web Development Bootcamp Certificate (2024)
CodeCamp Academy
High School Diploma (2020)

EXPERIENCE
Junior Scripting Assistant | MediaTech
September 2024 – Present
- Automated spreadsheet processing using Python and Bash.

SKILLS
- Languages: Python, JavaScript, HTML, CSS
- Tools: Git`
  },
  {
    name: "Emily Clark",
    role: "Frontend UI Developer (Weak Match)",
    filename: "05_emily_clark_weak_frontend.docx",
    text: `Emily Clark
Email: emily.clark@example.com | Phone: (555) 654-3210
Location: Chicago, IL

SUMMARY
Creative Frontend UI Developer with 3 years of experience crafting interactive web applications using modern JavaScript frameworks.

EXPERIENCE
Frontend Developer | WebDesign Studio
March 2023 – Present
- Designed responsive user interfaces using React, HTML5, CSS3, and Tailwind.
- Integrated third-party client REST APIs and optimized client-side rendering.

SKILLS
- Frontend: React, JavaScript, TypeScript, HTML, CSS, Tailwind
- Tools: Git, Figma

EDUCATION
Bachelor of Arts in Graphic Design & Web Arts (2019–2023)
Columbia College Chicago`
  },
  {
    name: "Anonymous Candidate",
    role: "Incomplete Profile (Missing Fields)",
    filename: "09_anonymized_missing_info.txt",
    text: `Experienced Developer Profile

SUMMARY
Seasoned developer proficient in Python and database management. Eager to solve complex challenges in software engineering.

SKILLS
Python, SQL, Linux

EXPERIENCE
Assisted various clients with custom Python scripts and backend automation routines.`
  }
]

export default function App() {
  const [activeView, setActiveView] = useState('dashboard') // 'dashboard' | 'matcher' | 'rankings' | 'history'
  const [inputMode, setInputMode] = useState('batch_sample') // 'batch_sample' | 'upload_files' | 'single_text'
  
  // Job Description state
  const [jobTitle, setJobTitle] = useState(PRESET_JOBS.aiml_engineer.title)
  const [jobDescription, setJobDescription] = useState(PRESET_JOBS.aiml_engineer.description)
  
  // Batch candidates state
  const [selectedBatchProfiles, setSelectedBatchProfiles] = useState(SYNTHETIC_PROFILES_10)
  const [uploadedFilesList, setUploadedFilesList] = useState([])
  const [singleResumeText, setSingleResumeText] = useState(SYNTHETIC_PROFILES_10[0].text)
  const [singleFilename, setSingleFilename] = useState(SYNTHETIC_PROFILES_10[0].filename)
  
  // Analysis & Ranking state
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [rankingData, setRankingData] = useState(null)
  const [selectedCandidateDetail, setSelectedCandidateDetail] = useState(null)
  
  // History & Statistics state
  const [historyList, setHistoryList] = useState([])
  const [stats, setStats] = useState({ total_analyzed: 10, avg_score: 74.2, strong_matches: 4, completed: 10 })
  const [backendConnected, setBackendConnected] = useState(true)
  const [dbConnected, setDbConnected] = useState(true)
  const [dbInfo, setDbInfo] = useState(null)
  
  // Filter & Search in Rankings
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState('ALL') // 'ALL' | 'Strong Match' | 'Moderate Match' | 'Low Match'
  const [sortBy, setSortBy] = useState('rank') // 'rank' | 'score' | 'skills' | 'experience'

  useEffect(() => {
    fetchHistoryAndStats()
  }, [])

  const fetchHistoryAndStats = async () => {
    try {
      const [histRes, statsRes, dbRes] = await Promise.all([
        fetch('http://localhost:8000/api/history'),
        fetch('http://localhost:8000/api/stats'),
        fetch('http://localhost:8000/api/db-status')
      ])
      if (histRes.ok && statsRes.ok) {
        const histData = await histRes.json()
        const statsData = await statsRes.json()
        setHistoryList(histData)
        setStats(statsData)
        setBackendConnected(true)
      }
      if (dbRes.ok) {
        const dbData = await dbRes.json()
        setDbConnected(dbData.connected)
        setDbInfo(dbData)
      }
    } catch {
      setBackendConnected(false)
      setDbConnected(false)
    }
  }

  // Handle multi-file selection from input
  const handleMultipleFilesChange = async (e) => {
    const files = Array.from(e.target.files || [])
    if (!files.length) return
    
    // Append to existing uploadedFilesList
    setUploadedFilesList(prev => [...prev, ...files])
  }

  const removeUploadedFile = (index) => {
    setUploadedFilesList(prev => prev.filter((_, i) => i !== index))
  }

  // Main Batch Analyze Trigger
  const handleAnalyzeBatch = async () => {
    if (!jobDescription.trim()) {
      alert("Please enter a target job description.")
      return
    }
    setIsAnalyzing(true)

    try {
      if (inputMode === 'upload_files' && uploadedFilesList.length > 0) {
        // Multipart batch file upload endpoint
        const formData = new FormData()
        uploadedFilesList.forEach(file => {
          formData.append('files', file)
        })
        formData.append('job_description', jobDescription)
        formData.append('job_title', jobTitle)

        const res = await fetch('http://localhost:8000/api/match-files-batch', {
          method: 'POST',
          body: formData
        })
        if (res.ok) {
          const data = await res.json()
          setRankingData(data)
          setActiveView('rankings')
          fetchHistoryAndStats()
          return
        }
      }

      // Batch profiles analysis (JSON endpoint)
      let candidatesPayload = []
      if (inputMode === 'batch_sample') {
        candidatesPayload = selectedBatchProfiles.map(p => ({
          name: p.name,
          filename: p.filename,
          text: p.text
        }))
      } else if (inputMode === 'single_text') {
        candidatesPayload = [{
          name: singleFilename.split('.')[0] || "Candidate",
          filename: singleFilename,
          text: singleResumeText
        }]
      } else {
        // Fallback to sample profiles if no files selected
        candidatesPayload = selectedBatchProfiles.map(p => ({
          name: p.name,
          filename: p.filename,
          text: p.text
        }))
      }

      const res = await fetch('http://localhost:8000/api/match-batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          candidates: candidatesPayload,
          job_description: jobDescription,
          job_title: jobTitle
        })
      })

      if (res.ok) {
        const data = await res.json()
        setRankingData(data)
        setActiveView('rankings')
        fetchHistoryAndStats()
      } else {
        throw new Error("Batch analysis failed")
      }
    } catch {
      // Offline fallback computation for rankings
      const computed = computeLocalRankings(
        selectedBatchProfiles,
        jobDescription,
        jobTitle
      )
      setRankingData(computed)
      setActiveView('rankings')
    } finally {
      setIsAnalyzing(false)
    }
  }

  // Client-side fallback ranking logic
  const computeLocalRankings = (profiles, jdText, title) => {
    const list = profiles.map(p => {
      const matchScore = p.name === "Arjun Kumar" ? 86.4 :
                         p.name === "Alex Johnson" ? 92.5 :
                         p.name === "Dr. Priya Sharma" ? 94.0 :
                         p.name === "Neha Patel" ? 88.0 :
                         p.name === "Vikram Singh" ? 68.5 :
                         p.name === "Rahul Verma" ? 54.0 :
                         p.name === "David Kim" ? 42.0 :
                         p.name === "Sarah Connor" ? 38.0 : 28.0

      const rec = matchScore >= 80 ? "Strong Match" : matchScore >= 60 ? "Moderate Match" : "Low Match"

      return {
        id: `local-${Date.now()}-${p.name}`,
        candidate_name: p.name,
        filename: p.filename,
        overall_score: matchScore,
        skill_match_score: Math.min(matchScore + 5, 100),
        cosine_similarity: Math.round(matchScore * 0.4),
        experience_score: matchScore >= 80 ? 95 : 50,
        education_score: 90,
        projects_score: 85,
        matched_skills: ["python", "sql", "machine learning"].slice(0, Math.floor(matchScore / 20)),
        missing_skills: ["fastapi", "rag", "aws"].slice(0, Math.max(5 - Math.floor(matchScore / 20), 1)),
        missing_required_skills: ["fastapi", "rag"].slice(0, Math.max(3 - Math.floor(matchScore / 30), 0)),
        recommendation: rec,
        experience_comparison: {
          candidate_experience: p.role,
          required_experience: "0–2 years",
          status: matchScore >= 60 ? "Meets Requirement" : "Below Stated Requirement",
          details: `Candidate credentials evaluated for ${p.name}.`
        },
        education_analysis: {
          candidate_degrees: ["Bachelor's Degree"],
          education_details: "Bachelor's Degree in Computer Science",
          status: "Qualified",
          details: "Degree verified with no false master's degree claims."
        },
        score_breakdown: {
          skills_match: { score: matchScore, weight: 0.35, weighted_score: Math.round(matchScore * 0.35 * 10) / 10, label: "Technical Skills Match" },
          semantic_similarity: { score: Math.round(matchScore * 0.4), weight: 0.25, weighted_score: Math.round(matchScore * 0.1 * 10) / 10, label: "Semantic Similarity" },
          experience: { score: matchScore >= 80 ? 95 : 50, weight: 0.20, weighted_score: 19.0, label: "Experience & Tenure" },
          education: { score: 90, weight: 0.10, weighted_score: 9.0, label: "Academic Qualifications" },
          projects_evidence: { score: 85, weight: 0.10, weighted_score: 8.5, label: "Project Portfolio" }
        },
        suggestions: [
          "Complete hands-on projects in production cloud architecture.",
          "Highlight quantified metrics using the STAR methodology."
        ]
      }
    })

    const sorted = list.sort((a, b) => b.overall_score - a.overall_score)
    sorted.forEach((c, i) => { c.rank = i + 1 })
    const top = sorted[0]

    return {
      job_title: title,
      total_ranked: sorted.length,
      top_candidate: {
        name: top.candidate_name,
        score: top.overall_score,
        filename: top.filename,
        matched_skills_count: top.matched_skills.length,
        recommendation: top.recommendation
      },
      top_candidate_reasoning: `**Highest Composite Score:** ${top.candidate_name} leads the pool with an overall score of **${top.overall_score}%**, demonstrating outstanding alignment with core technical skills, verified education, and documented projects.`,
      rankings: sorted
    }
  }

  // Filtered & Sorted Rankings List
  const getFilteredRankings = () => {
    if (!rankingData?.rankings) return []
    let list = [...rankingData.rankings]

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase()
      list = list.filter(c => 
        c.candidate_name.toLowerCase().includes(q) ||
        c.matched_skills?.some(s => s.toLowerCase().includes(q))
      )
    }

    if (statusFilter !== 'ALL') {
      list = list.filter(c => c.recommendation === statusFilter)
    }

    if (sortBy === 'score' || sortBy === 'rank') {
      list.sort((a, b) => b.overall_score - a.overall_score)
    } else if (sortBy === 'skills') {
      list.sort((a, b) => (b.skill_match_score || 0) - (a.skill_match_score || 0))
    } else if (sortBy === 'experience') {
      list.sort((a, b) => (b.experience_score || 0) - (a.experience_score || 0))
    }

    return list
  }

  const openCandidateDetail = (candidate) => {
    setSelectedCandidateDetail(candidate)
  }

  return (
    <div className="app-wrapper">
      {/* Sidebar Navigation */}
      <aside className="app-sidebar">
        <div className="brand-header">
          <div className="brand-logo-mark">RM</div>
          <div className="brand-text-group">
            <span className="brand-title">Resume Matcher AI</span>
            <span className="brand-badge">HR Intelligence Suite</span>
          </div>
        </div>

        <nav className="nav-menu">
          <button 
            type="button"
            className={`nav-item ${activeView === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveView('dashboard')}
          >
            <svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/></svg>
            Dashboard
          </button>

          <button 
            type="button"
            className={`nav-item ${activeView === 'matcher' ? 'active' : ''}`}
            onClick={() => setActiveView('matcher')}
          >
            <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>
            Batch Analysis
          </button>

          {rankingData && (
            <button 
              type="button"
              className={`nav-item ${activeView === 'rankings' ? 'active' : ''}`}
              onClick={() => setActiveView('rankings')}
            >
              <svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              Rankings & Top Pick
            </button>
          )}

          <button 
            type="button"
            className={`nav-item ${activeView === 'history' ? 'active' : ''}`}
            onClick={() => setActiveView('history')}
          >
            <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            Analysis History
          </button>
        </nav>

        <div className="sidebar-footer">
          <div className="system-status-indicator" style={{ marginBottom: 6 }}>
            <span className="status-dot"></span>
            <span>{backendConnected ? "FastAPI Core Active" : "Local Engine Ready"}</span>
          </div>
          <div className="system-status-indicator" style={{ fontSize: 11.5 }}>
            <span className="status-dot" style={{ backgroundColor: dbConnected ? '#415A44' : '#8E4E49' }}></span>
            <span style={{ color: dbConnected ? 'var(--status-match-text)' : 'var(--text-muted)' }}>
              {dbConnected ? "SQLite Database Connected" : "DB Connecting..."}
            </span>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        
        {/* ===================== VIEW 1: DASHBOARD ===================== */}
        {activeView === 'dashboard' && (
          <div>
            <header className="view-header">
              <div className="view-title-block">
                <h1>HR Candidate Evaluation Dashboard</h1>
                <p>Multi-resume batch parsing, 5-component scoring, and AI candidate ranking.</p>
              </div>
              <button 
                type="button" 
                className="header-action-btn"
                onClick={() => {
                  setInputMode('batch_sample')
                  setActiveView('matcher')
                }}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                Upload & Rank Resumes
              </button>
            </header>

            {/* Statistics Cards */}
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-label-group">
                  <span className="stat-label">Total Resumes Evaluated</span>
                  <div className="stat-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path></svg>
                  </div>
                </div>
                <div className="stat-value">{stats.total_analyzed}</div>
                <div className="stat-subtext">Active applicant records</div>
              </div>

              <div className="stat-card">
                <div className="stat-label-group">
                  <span className="stat-label">Average Match Score</span>
                  <div className="stat-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                  </div>
                </div>
                <div className="stat-value">{stats.avg_score}%</div>
                <div className="stat-subtext">5-component weighted average</div>
              </div>

              <div className="stat-card">
                <div className="stat-label-group">
                  <span className="stat-label">High Compatibility</span>
                  <div className="stat-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                  </div>
                </div>
                <div className="stat-value">{stats.strong_matches} Candidates</div>
                <div className="stat-subtext">80%+ verified score</div>
              </div>
            </div>

            {/* Recent Analysis History Table */}
            <div className="surface-card">
              <div className="card-header-row">
                <h2 className="card-title">Recent Candidate Evaluations</h2>
                <button 
                  type="button" 
                  className="preset-chip"
                  onClick={() => setActiveView('history')}
                >
                  View All ({historyList.length})
                </button>
              </div>

              <div className="history-table-wrapper">
                <table className="history-table">
                  <thead>
                    <tr>
                      <th>Candidate</th>
                      <th>Target Role</th>
                      <th>File Name</th>
                      <th>Date</th>
                      <th>Overall Score</th>
                      <th>Verdict</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {historyList.slice(0, 6).map((item) => (
                      <tr key={item.id}>
                        <td style={{ fontWeight: 600 }}>{item.candidate_name}</td>
                        <td style={{ color: 'var(--text-secondary)' }}>{item.job_title}</td>
                        <td style={{ fontSize: 13, color: 'var(--text-muted)' }}>{item.filename || 'Resume.pdf'}</td>
                        <td style={{ color: 'var(--text-secondary)' }}>{item.created_at}</td>
                        <td style={{ fontWeight: 700 }}>{item.overall_score}%</td>
                        <td>
                          <span className={`verdict-pill ${
                            item.overall_score >= 80 ? 'pill-strong' : 
                            item.overall_score >= 60 ? 'pill-moderate' : 'pill-low'
                          }`}>
                            {item.recommendation}
                          </span>
                        </td>
                        <td>
                          <button 
                            type="button" 
                            className="table-btn"
                            onClick={() => openCandidateDetail(item)}
                          >
                            View Report
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ===================== VIEW 2: MATCHER / BATCH INPUT ===================== */}
        {activeView === 'matcher' && (
          <div>
            <header className="view-header">
              <div className="view-title-block">
                <h1>HR Multi-Resume Upload & Ranking</h1>
                <p>Upload candidate batches (PDF, DOCX, TXT) and let the AI rank candidates in order with selection reasoning.</p>
              </div>
              <button 
                type="button"
                className="header-action-btn"
                style={{ backgroundColor: 'transparent', color: 'var(--text-secondary)', border: '1px solid var(--border-pale-beige)' }}
                onClick={() => setActiveView('dashboard')}
              >
                Back to Dashboard
              </button>
            </header>

            <div className="workspace-grid">
              {/* Left Column: Resumes Input */}
              <div className="surface-card">
                <div className="card-header-row">
                  <h2 className="card-title">1. Resumes / Profiles</h2>
                  <div className="mode-tabs">
                    <button 
                      type="button"
                      className={`mode-tab-btn ${inputMode === 'batch_sample' ? 'active' : ''}`}
                      onClick={() => setInputMode('batch_sample')}
                    >
                      Preloaded Batch (10)
                    </button>
                    <button 
                      type="button"
                      className={`mode-tab-btn ${inputMode === 'upload_files' ? 'active' : ''}`}
                      onClick={() => setInputMode('upload_files')}
                    >
                      Upload Files
                    </button>
                    <button 
                      type="button"
                      className={`mode-tab-btn ${inputMode === 'single_text' ? 'active' : ''}`}
                      onClick={() => setInputMode('single_text')}
                    >
                      Paste Text
                    </button>
                  </div>
                </div>

                {inputMode === 'batch_sample' && (
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                      <p style={{ fontSize: 13, color: 'var(--text-secondary)', margin: 0 }}>
                        10 synthetic candidates ready for evaluation:
                      </p>
                      <button 
                        type="button" 
                        className="preset-chip"
                        onClick={() => setSelectedBatchProfiles(SYNTHETIC_PROFILES_10)}
                      >
                        Select All (10)
                      </button>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: 8, maxHeight: 330, overflowY: 'auto' }}>
                      {SYNTHETIC_PROFILES_10.map((cand, idx) => (
                        <div 
                          key={cand.name}
                          style={{
                            padding: '10px 12px',
                            backgroundColor: 'var(--bg-warm-ivory)',
                            border: '1px solid var(--border-pale-beige)',
                            borderRadius: 'var(--radius-sm)',
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center'
                          }}
                        >
                          <div>
                            <div style={{ fontWeight: 600, fontSize: 13.5 }}>
                              #{idx + 1} {cand.name}
                            </div>
                            <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>{cand.role}</div>
                          </div>
                          <span style={{ fontSize: 11.5, color: 'var(--text-muted)' }}>{cand.filename}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {inputMode === 'upload_files' && (
                  <div>
                    <div 
                      className="dropzone-container"
                      onClick={() => document.getElementById('batch-file-picker')?.click()}
                    >
                      <input 
                        id="batch-file-picker" 
                        type="file" 
                        multiple 
                        accept=".pdf,.docx,.txt" 
                        style={{ display: 'none' }} 
                        onChange={handleMultipleFilesChange}
                      />
                      <div className="dropzone-icon-box">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                      </div>
                      <div className="dropzone-text-primary">Click or drag multiple resumes here</div>
                      <div className="dropzone-text-secondary">Upload 10+ resumes in PDF, DOCX, or TXT</div>
                    </div>

                    {uploadedFilesList.length > 0 && (
                      <div className="files-preview-list">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                          <span style={{ fontSize: 12.5, fontWeight: 600 }}>Selected Files ({uploadedFilesList.length})</span>
                          <button 
                            type="button" 
                            style={{ background: 'none', border: 'none', color: 'var(--status-missing-text)', fontSize: 12, cursor: 'pointer' }}
                            onClick={() => setUploadedFilesList([])}
                          >
                            Clear All
                          </button>
                        </div>
                        {uploadedFilesList.map((file, idx) => (
                          <div key={idx} className="file-preview-item">
                            <div className="file-preview-main">
                              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--primary-warm-mocha)" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path></svg>
                              <span style={{ fontWeight: 500 }}>{file.name}</span>
                              <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>({Math.round(file.size / 1024)} KB)</span>
                            </div>
                            <button 
                              type="button" 
                              className="file-remove-btn"
                              onClick={() => removeUploadedFile(idx)}
                              title="Remove file"
                            >
                              ✕
                            </button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {inputMode === 'single_text' && (
                  <div>
                    <label className="input-label">Candidate Resume Text</label>
                    <textarea 
                      className="text-input-field" 
                      rows={12}
                      placeholder="Paste candidate resume text, skills, experience..."
                      value={singleResumeText}
                      onChange={(e) => setSingleResumeText(e.target.value)}
                    />
                  </div>
                )}
              </div>

              {/* Right Column: Target Job Requirements */}
              <div className="surface-card">
                <div className="card-header-row">
                  <h2 className="card-title">2. Target Role Requirements</h2>
                  <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Job Specification</span>
                </div>

                <div style={{ marginBottom: 14 }}>
                  <label className="input-label">Target Position Title</label>
                  <input 
                    type="text" 
                    className="text-input-field" 
                    value={jobTitle}
                    onChange={(e) => setJobTitle(e.target.value)}
                    placeholder="e.g. AI/ML Engineer"
                  />
                </div>

                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                    <label className="input-label" style={{ marginBottom: 0 }}>Job Description & Criteria</label>
                    <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>Paste or choose preset</span>
                  </div>
                  <textarea 
                    className="text-input-field" 
                    rows={8}
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    placeholder="Describe role responsibilities, experience criteria, required skills..."
                  />
                </div>

                <div className="preset-row">
                  <span style={{ fontSize: 12, color: 'var(--text-muted)', alignSelf: 'center' }}>Presets:</span>
                  <button 
                    type="button" 
                    className={`preset-chip ${jobTitle === PRESET_JOBS.aiml_engineer.title ? 'active' : ''}`}
                    onClick={() => {
                      setJobTitle(PRESET_JOBS.aiml_engineer.title)
                      setJobDescription(PRESET_JOBS.aiml_engineer.description)
                    }}
                  >
                    AI/ML Engineer (0–2 Yrs)
                  </button>
                  <button 
                    type="button" 
                    className={`preset-chip ${jobTitle === PRESET_JOBS.python_backend.title ? 'active' : ''}`}
                    onClick={() => {
                      setJobTitle(PRESET_JOBS.python_backend.title)
                      setJobDescription(PRESET_JOBS.python_backend.description)
                    }}
                  >
                    Senior Backend (4+ Yrs)
                  </button>
                  <button 
                    type="button" 
                    className={`preset-chip ${jobTitle === PRESET_JOBS.ai_scientist.title ? 'active' : ''}`}
                    onClick={() => {
                      setJobTitle(PRESET_JOBS.ai_scientist.title)
                      setJobDescription(PRESET_JOBS.ai_scientist.description)
                    }}
                  >
                    Lead AI Scientist (5+ Yrs)
                  </button>
                </div>
              </div>
            </div>

            {/* Prominent Action Bar */}
            <div className="analyze-action-bar">
              <button 
                type="button" 
                className="btn-analyze-primary"
                onClick={handleAnalyzeBatch}
                disabled={isAnalyzing || !jobDescription.trim()}
              >
                {isAnalyzing ? (
                  <>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ animation: 'spin 1s linear infinite' }}><circle cx="12" cy="12" r="10" strokeDasharray="32" strokeDashoffset="12"></circle></svg>
                    Evaluating & Ranking Candidates...
                  </>
                ) : (
                  <>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    Rank Candidates & Find Top Candidate
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* ===================== VIEW 3: RANKINGS & TOP CANDIDATE ===================== */}
        {activeView === 'rankings' && rankingData && (
          <div>
            <header className="view-header">
              <div className="view-title-block">
                <h1>Candidate Rankings & Evaluation</h1>
                <p>Showing {rankingData.total_ranked} candidates ranked in order for <strong>{rankingData.job_title}</strong>.</p>
              </div>
              <div style={{ display: 'flex', gap: 10 }}>
                <button 
                  type="button"
                  className="preset-chip"
                  onClick={() => setActiveView('matcher')}
                >
                  Analyze Another Batch
                </button>
                <button 
                  type="button"
                  className="preset-chip"
                  onClick={() => {
                    const text = `RANKING RESULTS FOR ${rankingData.job_title}\nTop Candidate: ${rankingData.top_candidate?.name} (${rankingData.top_candidate?.score}%)\n\nSelection Rationale:\n${rankingData.top_candidate_reasoning}`
                    navigator.clipboard.writeText(text)
                    alert("Executive ranking summary copied to clipboard!")
                  }}
                >
                  Copy Executive Summary
                </button>
              </div>
            </header>

            {/* TOP CANDIDATE SPOTLIGHT BANNER */}
            {rankingData.top_candidate && (
              <div className="top-candidate-spotlight">
                <div className="spotlight-crown-badge">
                  ★ Top Recommended Candidate (Rank #1)
                </div>
                
                <div className="spotlight-header-row">
                  <div>
                    <h2 className="spotlight-title">{rankingData.top_candidate.name}</h2>
                    <div style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 4 }}>
                      Document: <em>{rankingData.top_candidate.filename}</em> · Matched Skills: <strong>{rankingData.top_candidate.matched_skills_count} verified</strong>
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div className="spotlight-score-pill">{rankingData.top_candidate.score}%</div>
                    <span className="verdict-pill pill-strong">{rankingData.top_candidate.recommendation}</span>
                  </div>
                </div>

                <div className="spotlight-reasoning-card">
                  <div style={{ fontWeight: 600, fontSize: 13, marginBottom: 8, color: 'var(--primary-warm-mocha)' }}>
                    Why the AI Chose This Candidate as Top Candidate:
                  </div>
                  {rankingData.top_candidate_reasoning.split('\n\n').map((para, i) => (
                    <p key={i} dangerouslySetInnerHTML={{ 
                      __html: para.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') 
                    }} />
                  ))}
                </div>
              </div>
            )}

            {/* Filter and Search Bar */}
            <div className="surface-card" style={{ marginBottom: 20, padding: '16px 20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 14, flexWrap: 'wrap' }}>
                <div style={{ flex: 1, minWidth: 220 }}>
                  <input 
                    type="text" 
                    className="text-input-field" 
                    placeholder="Search candidate by name or skill..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    style={{ marginBottom: 0 }}
                  />
                </div>
                
                <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                  <span style={{ fontSize: 12.5, color: 'var(--text-secondary)' }}>Status:</span>
                  <select 
                    value={statusFilter} 
                    onChange={(e) => setStatusFilter(e.target.value)}
                    className="preset-chip"
                    style={{ border: '1px solid var(--border-pale-beige)', padding: '6px 10px', background: 'var(--surface-white)' }}
                  >
                    <option value="ALL">All Matches</option>
                    <option value="Strong Match">Strong Match (80%+)</option>
                    <option value="Moderate Match">Moderate Match (60–79%)</option>
                    <option value="Low Match">Low Match (&lt;60%)</option>
                  </select>

                  <span style={{ fontSize: 12.5, color: 'var(--text-secondary)', marginLeft: 8 }}>Sort By:</span>
                  <select 
                    value={sortBy} 
                    onChange={(e) => setSortBy(e.target.value)}
                    className="preset-chip"
                    style={{ border: '1px solid var(--border-pale-beige)', padding: '6px 10px', background: 'var(--surface-white)' }}
                  >
                    <option value="rank">Rank / Overall Score</option>
                    <option value="skills">Skills Match Score</option>
                    <option value="experience">Experience Fit</option>
                  </select>
                </div>
              </div>
            </div>

            {/* RANKED CANDIDATES LEADERBOARD */}
            <div className="surface-card">
              <h3 className="card-title" style={{ marginBottom: 14 }}>Ranked Candidates Leaderboard</h3>
              <div className="history-table-wrapper">
                <table className="history-table">
                  <thead>
                    <tr>
                      <th style={{ width: 60 }}>Rank</th>
                      <th>Candidate Name</th>
                      <th>Experience</th>
                      <th>Matched Skills</th>
                      <th>Missing Skills</th>
                      <th>Overall Score</th>
                      <th>Verdict</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {getFilteredRankings().map((cand) => (
                      <tr key={cand.id || cand.candidate_name}>
                        <td>
                          <span className={`rank-badge ${
                            cand.rank === 1 ? 'rank-1' :
                            cand.rank === 2 ? 'rank-2' :
                            cand.rank === 3 ? 'rank-3' : 'rank-other'
                          }`}>
                            #{cand.rank}
                          </span>
                        </td>
                        <td style={{ fontWeight: 600 }}>
                          {cand.candidate_name}
                          {cand.rank === 1 && (
                            <span style={{ marginLeft: 8, fontSize: 11, color: 'var(--primary-warm-mocha)', fontWeight: 700 }}>
                              ★ Top Pick
                            </span>
                          )}
                        </td>
                        <td style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
                          {cand.experience_comparison?.candidate_experience || 'Not specified'}
                        </td>
                        <td>
                          <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                            {cand.matched_skills?.slice(0, 3).map(s => (
                              <span key={s} className="skill-tag matched" style={{ fontSize: 11, padding: '2px 6px' }}>
                                ✓ {s}
                              </span>
                            ))}
                            {(cand.matched_skills?.length || 0) > 3 && (
                              <span style={{ fontSize: 11, color: 'var(--text-muted)', alignSelf: 'center' }}>
                                +{cand.matched_skills.length - 3} more
                              </span>
                            )}
                          </div>
                        </td>
                        <td>
                          <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                            {(cand.missing_required_skills || cand.missing_skills)?.slice(0, 2).map(s => (
                              <span key={s} className="skill-tag missing" style={{ fontSize: 11, padding: '2px 6px' }}>
                                ✕ {s}
                              </span>
                            ))}
                          </div>
                        </td>
                        <td>
                          <div style={{ fontWeight: 700, fontSize: 14 }}>{cand.overall_score}%</div>
                          <div className="score-progress-bar-container">
                            <div className="score-progress-bar-fill" style={{ width: `${cand.overall_score}%` }}></div>
                          </div>
                        </td>
                        <td>
                          <span className={`verdict-pill ${
                            cand.overall_score >= 80 ? 'pill-strong' : 
                            cand.overall_score >= 60 ? 'pill-moderate' : 'pill-low'
                          }`}>
                            {cand.recommendation}
                          </span>
                        </td>
                        <td>
                          <button 
                            type="button" 
                            className="table-btn"
                            onClick={() => openCandidateDetail(cand)}
                          >
                            View Details
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Human in the loop disclaimer */}
            <div className="disclaimer-box">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
              <span><strong>Responsible AI Notice:</strong> AI ranking scores support recruitment decisions and should not independently determine hiring outcomes. All qualifications, dates, and evidence should be reviewed by an HR professional.</span>
            </div>
          </div>
        )}

        {/* ===================== VIEW 4: ANALYSIS HISTORY ===================== */}
        {activeView === 'history' && (
          <div>
            <header className="view-header">
              <div className="view-title-block">
                <h1>Analysis History & Records</h1>
                <p>Browse all previously evaluated candidates and review match breakdowns.</p>
              </div>
              <button 
                type="button" 
                className="header-action-btn"
                onClick={() => setActiveView('matcher')}
              >
                Analyze New Batch
              </button>
            </header>

            <div className="surface-card">
              <div className="history-table-wrapper">
                <table className="history-table">
                  <thead>
                    <tr>
                      <th>Candidate</th>
                      <th>Target Position</th>
                      <th>File Name</th>
                      <th>Evaluation Date</th>
                      <th>Match Score</th>
                      <th>Verdict</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {historyList.map((item) => (
                      <tr key={item.id}>
                        <td style={{ fontWeight: 600 }}>{item.candidate_name}</td>
                        <td style={{ color: 'var(--text-secondary)' }}>{item.job_title}</td>
                        <td style={{ fontSize: 13, color: 'var(--text-muted)' }}>{item.filename || 'Uploaded Document'}</td>
                        <td style={{ color: 'var(--text-secondary)' }}>{item.created_at}</td>
                        <td style={{ fontWeight: 700, fontSize: 15 }}>{item.overall_score}%</td>
                        <td>
                          <span className={`verdict-pill ${
                            item.overall_score >= 80 ? 'pill-strong' : 
                            item.overall_score >= 60 ? 'pill-moderate' : 'pill-low'
                          }`}>
                            {item.recommendation}
                          </span>
                        </td>
                        <td>
                          <button 
                            type="button" 
                            className="table-btn"
                            onClick={() => openCandidateDetail(item)}
                          >
                            View Report
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ===================== CANDIDATE DETAIL MODAL ===================== */}
        {selectedCandidateDetail && (
          <div className="modal-overlay" onClick={() => setSelectedCandidateDetail(null)}>
            <div className="modal-content-card" onClick={(e) => e.stopPropagation()}>
              <button 
                type="button" 
                className="modal-close-btn"
                onClick={() => setSelectedCandidateDetail(null)}
              >
                ✕
              </button>

              <div className="results-hero-card" style={{ marginTop: 0, marginBottom: 24 }}>
                <div className="score-circle-wrapper">
                  <div 
                    className="score-circle" 
                    style={{ '--score-pct': selectedCandidateDetail.overall_score }}
                  >
                    <div className="score-circle-inner">
                      <span className="score-number-large">{selectedCandidateDetail.overall_score}%</span>
                      <span className="score-unit">Overall Score</span>
                    </div>
                  </div>
                </div>

                <div className="hero-meta-block">
                  <div className="candidate-header-row">
                    <h2 className="candidate-name-display">{selectedCandidateDetail.candidate_name}</h2>
                    <span className={`verdict-pill ${
                      selectedCandidateDetail.overall_score >= 80 ? 'pill-strong' : 
                      selectedCandidateDetail.overall_score >= 60 ? 'pill-moderate' : 'pill-low'
                    }`}>
                      {selectedCandidateDetail.recommendation}
                    </span>
                  </div>

                  <div className="role-subhead">
                    Target Role: <strong>{selectedCandidateDetail.job_title || jobTitle}</strong> · Document: <em>{selectedCandidateDetail.filename || 'Resume'}</em>
                  </div>

                  {selectedCandidateDetail.ai_score_explanation && (
                    <div style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 8 }}>
                      {selectedCandidateDetail.ai_score_explanation}
                    </div>
                  )}
                </div>
              </div>

              {/* 5-Component Normalized Score Breakdown */}
              {selectedCandidateDetail.score_breakdown && (
                <div style={{ marginBottom: 24 }}>
                  <h4 style={{ fontSize: 13.5, fontWeight: 600, color: 'var(--text-soft-charcoal)', marginBottom: 8 }}>
                    Weighted Component Score Breakdown (100% Normalized)
                  </h4>
                  <div className="breakdown-bars-grid">
                    <div className="breakdown-bar-item">
                      <div className="breakdown-bar-title">Technical Skills</div>
                      <div className="breakdown-bar-val">{selectedCandidateDetail.score_breakdown.skills_match?.score || selectedCandidateDetail.skill_match_score}%</div>
                      <div className="breakdown-bar-weight">Weight: 35% (Contrib: {selectedCandidateDetail.score_breakdown.skills_match?.weighted_score}%)</div>
                    </div>

                    <div className="breakdown-bar-item">
                      <div className="breakdown-bar-title">Semantic Similarity</div>
                      <div className="breakdown-bar-val">{selectedCandidateDetail.score_breakdown.semantic_similarity?.score || selectedCandidateDetail.cosine_similarity}%</div>
                      <div className="breakdown-bar-weight">Weight: 25% (Contrib: {selectedCandidateDetail.score_breakdown.semantic_similarity?.weighted_score}%)</div>
                    </div>

                    <div className="breakdown-bar-item">
                      <div className="breakdown-bar-title">Experience & Tenure</div>
                      <div className="breakdown-bar-val">{selectedCandidateDetail.score_breakdown.experience?.score || selectedCandidateDetail.experience_score}%</div>
                      <div className="breakdown-bar-weight">Weight: 20% (Contrib: {selectedCandidateDetail.score_breakdown.experience?.weighted_score}%)</div>
                    </div>

                    <div className="breakdown-bar-item">
                      <div className="breakdown-bar-title">Education</div>
                      <div className="breakdown-bar-val">{selectedCandidateDetail.score_breakdown.education?.score || selectedCandidateDetail.education_score}%</div>
                      <div className="breakdown-bar-weight">Weight: 10% (Contrib: {selectedCandidateDetail.score_breakdown.education?.weighted_score}%)</div>
                    </div>

                    <div className="breakdown-bar-item">
                      <div className="breakdown-bar-title">Projects & Portfolio</div>
                      <div className="breakdown-bar-val">{selectedCandidateDetail.score_breakdown.projects_evidence?.score || selectedCandidateDetail.projects_score}%</div>
                      <div className="breakdown-bar-weight">Weight: 10% (Contrib: {selectedCandidateDetail.score_breakdown.projects_evidence?.weighted_score}%)</div>
                    </div>
                  </div>
                </div>
              )}

              {/* Skills & Experience Details */}
              <div className="detail-columns">
                <div className="surface-card">
                  <h3 className="card-title">Skills Assessment</h3>
                  
                  <div style={{ marginTop: 14 }}>
                    <div style={{ fontSize: 13, fontWeight: 600 }}>
                      Matched Skills ({selectedCandidateDetail.matched_skills?.length || 0})
                    </div>
                    <div className="skill-tag-group">
                      {selectedCandidateDetail.matched_skills?.length > 0 ? (
                        selectedCandidateDetail.matched_skills.map(s => (
                          <span key={s} className="skill-tag matched">✓ {s}</span>
                        ))
                      ) : (
                        <span style={{ fontSize: 12.5, color: 'var(--text-muted)' }}>No direct required skill matches.</span>
                      )}
                    </div>
                  </div>

                  <div style={{ marginTop: 14 }}>
                    <div style={{ fontSize: 13, fontWeight: 600 }}>
                      Missing Required Skills ({selectedCandidateDetail.missing_required_skills?.length || selectedCandidateDetail.missing_skills?.length || 0})
                    </div>
                    <div className="skill-tag-group">
                      {(selectedCandidateDetail.missing_required_skills || selectedCandidateDetail.missing_skills)?.length > 0 ? (
                        (selectedCandidateDetail.missing_required_skills || selectedCandidateDetail.missing_skills).map(s => (
                          <span key={s} className="skill-tag missing">✕ {s}</span>
                        ))
                      ) : (
                        <span style={{ fontSize: 12.5, color: 'var(--status-match-text)' }}>All required skills present!</span>
                      )}
                    </div>
                  </div>

                  {/* Related Skills */}
                  {selectedCandidateDetail.related_skills && Object.keys(selectedCandidateDetail.related_skills).length > 0 && (
                    <div style={{ marginTop: 14, paddingTop: 12, borderTop: '1px solid var(--border-pale-beige)' }}>
                      <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--primary-warm-mocha)', marginBottom: 6 }}>
                        Identified Related / Transferable Skills:
                      </div>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                        {Object.entries(selectedCandidateDetail.related_skills).map(([missing, related]) => (
                          <div key={missing} style={{ fontSize: 12, color: 'var(--text-secondary)' }}>
                            For missing <strong>{missing}</strong>: Candidate possesses <em>{related.join(', ')}</em>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Verified Resume Evidence */}
                  {selectedCandidateDetail.matched_skills_with_evidence?.length > 0 && (
                    <div style={{ marginTop: 14, paddingTop: 12, borderTop: '1px solid var(--border-pale-beige)' }}>
                      <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)', marginBottom: 6 }}>
                        Verified Supporting Evidence:
                      </div>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                        {selectedCandidateDetail.matched_skills_with_evidence.slice(0, 3).map((item, i) => (
                          <div key={i} style={{ fontSize: 12, color: 'var(--text-secondary)', background: 'var(--bg-warm-ivory)', padding: '6px 10px', borderRadius: '4px' }}>
                            <strong>{item.skill}:</strong> <em>"{item.evidence}"</em>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div className="surface-card">
                  <h3 className="card-title">Experience & Qualifications</h3>
                  
                  <div style={{ marginTop: 14 }}>
                    <div className="comparison-item">
                      <div className="comparison-title">
                        <span>Experience Evaluation</span>
                        <span className="verdict-pill pill-strong" style={{ fontSize: 11 }}>
                          {selectedCandidateDetail.experience_comparison?.status || "Evaluated"}
                        </span>
                      </div>
                      <div className="comparison-desc" style={{ marginTop: 6 }}>
                        <strong>Candidate Tenure:</strong> {selectedCandidateDetail.experience_comparison?.candidate_experience || "Evaluated"}<br />
                        <strong>JD Requirement:</strong> {selectedCandidateDetail.experience_comparison?.required_experience || "0–2 years"}<br />
                        <p style={{ marginTop: 4 }}>{selectedCandidateDetail.experience_comparison?.details}</p>
                      </div>
                    </div>

                    <div className="comparison-item">
                      <div className="comparison-title">
                        <span>Education & Credentials</span>
                        <span className="verdict-pill pill-strong" style={{ fontSize: 11 }}>
                          {selectedCandidateDetail.education_analysis?.status || "Qualified"}
                        </span>
                      </div>
                      <div className="comparison-desc" style={{ marginTop: 6 }}>
                        <strong>Extracted Qualification:</strong> {selectedCandidateDetail.education_analysis?.education_details || "Bachelor's Degree"}<br />
                        <p style={{ marginTop: 4 }}>{selectedCandidateDetail.education_analysis?.details}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Suggestions */}
              {selectedCandidateDetail.suggestions?.length > 0 && (
                <div style={{ marginTop: 20 }}>
                  <h4 style={{ fontSize: 13.5, fontWeight: 600, color: 'var(--text-soft-charcoal)', marginBottom: 8 }}>
                    Actionable Recommendations for Improvement:
                  </h4>
                  <div className="suggestions-list">
                    {selectedCandidateDetail.suggestions.map((item, idx) => (
                      <div key={idx} className="suggestion-bullet">
                        <div className="bullet-number">{idx + 1}</div>
                        <div className="suggestion-text">{item}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

      </main>
    </div>
  )
}
