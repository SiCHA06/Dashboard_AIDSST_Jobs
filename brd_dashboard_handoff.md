# Business Requirements Document (BRD) & Handoff Prompt

**Target System:** Antigravity (Dashboard Generation Agent)
**Project Name:** AI & Data Science Workforce vs Job Market Dashboard
**Tech Stack:** Python (Backend & Logic), Plotly Dash (Frontend & Interactivity), Pandas (Data Manipulation)

## 1. Project Objective
Create an interactive dashboard using **Python and Plotly Dash** to answer two primary business questions:
1. What is the supply of graduates and what skills did they learn?
2. What is the market demand for jobs and what skills are required?

The dashboard must evaluate the "Skill Mismatch" between educational supply and industry demand.

## 2. Technical & Architectural Constraints
- **Framework:** Use `Dash` by Plotly for the web application layout and callback logic.
- **Visualizations:** Use `plotly.express` (px) and `plotly.graph_objects` (go).
- **Interactivity (CRITICAL):** Implement Cross-Filtering. Every chart within a tab must be interconnected. Clicking on a data point in one chart (e.g., clicking on a specific Degree Program) must update all other charts in that same tab via Dash `@app.callback`.
- **Data Handling:** Generate mock data using `pandas.DataFrame` that strictly follows the schemas provided below to ensure the code is fully runnable out-of-the-box.

## 3. UI/UX & Tab Structure

The application must be structured using `dcc.Tabs` containing 3 main tabs:

### Tab 1: Education Supply & Learned Skills (ปริมาณคนที่จบ และ skills ที่เรียนมา)
**Objective:** Visualize the university output and curriculum alignment.
**Required Components:**
1. **Graduates over Time (Bar/Line Chart):** Show degree programs (AI, Data Science, Statistics) and the number of graduates produced per year. (Allows filtering by program).
2. **Mandatory Core Courses (Horizontal Bar Chart or Data Table):** List of mandatory courses relevant to the field for the selected degree programs.
3. **Employment Rate Timeline (Stacked Bar or Line Chart):** Show the number/percentage of graduates employed in Year 1, Year 2, and Year 3 post-graduation.
4. **Tuition Fees (Bar Chart):** Compare the tuition fees across different degree programs.

### Tab 2: Market Demand & Required Skills (ปริมาณงานที่จ้าง และ skills ที่ต้องการ)
**Objective:** Visualize current job market demands.
**Required Components:**
1. **Job Vacancies (Time Series or KPI Cards + Bar Chart):** Volume of open positions grouped by role (AI Engineer, Data Scientist, Statistician).
2. **Top Required Skills (Word Cloud or Horizontal Bar Chart):** Frequency of skills mentioned in job descriptions (e.g., Python, SQL, AWS, PyTorch).
3. **Top Hiring Companies (Tree Map or Bar Chart):** Distribution of job openings across top companies/industries.
4. **Salary by Experience Level (Box Plot or Grouped Bar Chart):** Salary ranges categorized by experience level (Entry, Mid, Senior).

### Tab 3: Skill Mismatch Analysis (วิเคราะห์ Skill Mismatch)
**Objective:** Compare Tab 1 and Tab 2 data to find gaps.
**Required Components:**
1. **Learned vs. Required Skills Gap (Radar Chart OR Diverging Bar Chart):** 
   - Overlay the frequency of skills taught in universities (Supply) vs. the frequency of skills demanded by employers (Demand).
   - *Logic:* Highlight skills with high demand but low academic focus (The Deficit Gap), and skills with high academic focus but low demand (The Surplus Gap).

## 4. Mock Data Schema Guidelines

Please construct `pandas` DataFrames using these conceptual schemas to make the dashboard functional:

**Schema: Education (df_edu)**
- `Year` (int: 2020-2026)
- `Degree_Program` (str: B.Sc. Data Science, M.Sc. AI, B.Sc. Statistics)
- `Graduates_Count` (int)
- `Tuition_Fee_USD` (float)
- `Employed_Year_1` (int), `Employed_Year_2` (int), `Employed_Year_3` (int)

**Schema: Courses & Learned Skills (df_learned_skills)**
- `Degree_Program` (str)
- `Course_Name` (str)
- `Skill_Taught` (str: Python, R, ML, Stats, SQL)
- `Weight_in_Curriculum` (float)

**Schema: Job Market & Demand (df_jobs)**
- `Job_Role` (str: Data Scientist, AI Engineer, Statistician)
- `Company_Name` (str)
- `Experience_Level` (str: Entry, Mid, Senior)
- `Salary_USD` (float)
- `Vacancies_Count` (int)
- `Required_Skills` (list or comma-separated string)

## 5. Execution Command for Antigravity
Using the requirements and mock schemas above, write the complete, single-file `app.py` Python script using Dash and Plotly. Ensure all callbacks for cross-filtering within tabs are implemented and functioning with the generated mock data.