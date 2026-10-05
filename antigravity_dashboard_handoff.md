# Handoff Document: AI & Data Science Job Market Dashboard

**Target System:** Antigravity (Dashboard Generation Agent)
**Project Name:** Global Data Market Insights Dashboard
**Objective:** Generate a responsive, interactive dashboard to visualize the global landscape of AI, Data Science, and Statistics professionals, including education, salaries, top companies, and required skills.

## 1. System Prompt & Persona

Act as an Expert Frontend Engineer and UI/UX Designer specializing in data visualization. Use this handoff document to generate a fully functional dashboard layout. Ensure the design is modern, accessible, and highly interactive.

## 2. Open Data Sources & Schema Structure

The dashboard will ingest and visualize data based on the following real-world Open Data sources. Assume the data streams are pre-cleaned and available in the provided JSON/API structures.

### 2.1 Education & Graduate Statistics
* **Sources:**
  * **Stanford AI Index Report:** Global dataset on AI/CS graduates, hiring trends, and regional breakdowns. ([View Source](https://github.com/stanford-hai/ai-index))
  * **NCES IPEDS:** US government education data tracking degree completions (CIP: 30.70 Data Science, 11.0102 AI, 27.05 Statistics). ([View Source](https://nces.ed.gov/ipeds/use-the-data))
* **Schema (Mock):** `{ "year", "degree", "field" (AI, Data Science, Stats), "country", "total_graduates" }`

### 2.2 Salaries, Jobs, and Top Companies
* **Sources:**
  * **Salaries for Data Science Jobs (Kaggle):** Global compensation data categorized by experience levels (EN=Entry, MI=Mid, SE=Senior, EX=Executive). ([View Source](https://www.kaggle.com/datasets/adilshamim8/salaries-for-data-science-jobs))
  * **Data Science Job Postings (Kaggle):** Scraped job listings detailing active hiring companies and industries. ([View Source](https://www.kaggle.com/datasets/slmsshk/data-science-job-postings))
* **Salary Schema (Mock):** `{ "job_title", "experience_level" (EN, MI, SE, EX), "salary_usd", "company_location" }`
* **Company Schema (Mock):** `{ "company_name", "industry", "job_openings_count" }`

### 2.3 Required Skills in Job Applications
* **Source:**
  * **Lightcast Open Skills Taxonomy:** Open dataset of categorized technical skills extracted from millions of global job descriptions. ([View Source](https://lightcast.io/open-skills))
* **Skills Schema (Mock):** `{ "skill_name", "category", "frequency_in_job_posts" }`

## 3. Dashboard Layout & UI Components

### 3.1 Global Filters (Top Bar)

* **Country Selector:** Dropdown (Default: Global / All)
* **Role Selector:** Dropdown (AI Engineer, Data Scientist, Statistician)
* **Experience Level:** Multi-select Toggle (Entry-level, Mid-level, Senior, Executive)

### 3.2 Key Performance Indicators (KPI Cards - Top Row)

* **Average Starting Salary:** Focus on `experience_level = 'EN'`. (e.g., "$85,000 / year")
* **Total Graduates (Current Year):** Aggregated from `education_data`.
* **Top Hiring Industry:** The industry with the most job openings.

### 3.3 Main Visualization Panels

*Please implement the following charts using your native charting libraries (e.g., Recharts, Chart.js, or Antigravity's default).*

**Panel A: Salary by Experience Level (Bar Chart)**
* X-Axis: Experience Levels (Entry, Mid, Senior)
* Y-Axis: Average Salary (USD)
* Grouping: Job Titles (AI vs Data Science vs Stats)

**Panel B: Most Demanded Skills (Horizontal Bar Chart or Word Cloud)**
* Top 10 skills from `skills_data`.
* X-Axis: Frequency / Mention count in job applications.
* Y-Axis: Skill Name (Python, SQL, Machine Learning, etc.)

**Panel C: Global Graduate Distribution (Choropleth Map or Pie Chart)**
* Displaying the volume of graduates mapped by Country.

**Panel D: Top Hiring Companies (Data Table or List)**
* Columns: Company Name, Industry, Active Job Openings.
* Sorted by: `job_openings_count` (Descending).

## 4. Technical Constraints & Styling

* **Theme:** Dark mode by default with a toggle for Light mode.
* **Color Palette:** Cyber/Tech aesthetic (Teal, Neon Blue, Purple accents for data points).
* **Responsiveness:** Must collapse gracefully on mobile devices (stack panels vertically).
* **Interactivity:** Hovering over charts should display detailed tooltips.

## 5. Execution Command

Proceed to generate the dashboard code (React/Next.js/Tailwind, or your specified framework) based strictly on the parameters defined in this document. Incorporate mock data that reflects the realities of the provided Open Data sources.