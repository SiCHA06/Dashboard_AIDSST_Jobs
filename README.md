# AI & Data Science Job Market Dashboard

## Project Objective
Generate a responsive, interactive dashboard to visualize the global landscape of AI, Data Science, and Statistics professionals. The dashboard addresses two primary business questions:
1. What is the supply of graduates and what skills did they learn?
2. What is the market demand for jobs and what skills are required?

Ultimately, the dashboard evaluates the "Skill Mismatch" between educational supply and industry demand.

## Data Sources & Mock Data
The dashboard utilizes data modeled after real-world open data sources:
- **Education & Graduate Statistics:** Stanford AI Index Report, NCES IPEDS.
- **Salaries, Jobs, and Top Companies:** Kaggle datasets for Data Science Salaries and Job Postings.
- **Required Skills:** Lightcast Open Skills Taxonomy.

## Technical Stack & Architecture
- **Backend & Logic:** Python
- **Frontend & Interactivity:** Plotly Dash
- **Data Manipulation:** Pandas
- **Visualizations:** plotly.express (px) and plotly.graph_objects (go)

## Features
- **Cross-Filtering Interactivity:** Every chart within a tab is interconnected.
- **Global Filters:** Country, Role, and Experience Level selectors.
- **KPI Cards:** Average Starting Salary, Total Graduates, Top Hiring Industry.
- **Tabbed Interface:**
  1. **Education Supply & Learned Skills:** Visualizes university output, curriculum alignment, employment rates, and tuition fees.
  2. **Market Demand & Required Skills:** Visualizes job vacancies, top required skills, top hiring companies, and salary by experience.
  3. **Skill Mismatch Analysis:** Compares learned vs. required skills to find deficit and surplus gaps.

## Constraints & Styling
- Dark mode theme with a Cyber/Tech aesthetic (Teal, Neon Blue, Purple accents).
- Responsive design that collapses gracefully on mobile devices.
- Detailed tooltips on hover.
