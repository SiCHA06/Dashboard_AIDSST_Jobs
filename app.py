import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- MOCK DATA GENERATION ---
np.random.seed(42)

# df_edu
years = list(range(2020, 2027))
degree_programs = ['B.Sc. Data Science', 'M.Sc. AI', 'B.Sc. Statistics']
edu_data = []
for year in years:
    for prog in degree_programs:
        edu_data.append({
            'Year': year,
            'Degree_Program': prog,
            'Graduates_Count': np.random.randint(500, 3000),
            'Tuition_Fee_USD': np.random.randint(10000, 50000),
            'Employed_Year_1': np.random.randint(400, 2500),
            'Employed_Year_2': np.random.randint(450, 2800),
            'Employed_Year_3': np.random.randint(480, 2900)
        })
df_edu = pd.DataFrame(edu_data)

# df_learned_skills
learned_skills_data = [
    {'Degree_Program': 'B.Sc. Data Science', 'Course_Name': 'Intro to Data Science', 'Skill_Taught': 'Python', 'Weight_in_Curriculum': 0.8},
    {'Degree_Program': 'B.Sc. Data Science', 'Course_Name': 'Database Systems', 'Skill_Taught': 'SQL', 'Weight_in_Curriculum': 0.7},
    {'Degree_Program': 'B.Sc. Data Science', 'Course_Name': 'Machine Learning', 'Skill_Taught': 'ML', 'Weight_in_Curriculum': 0.9},
    {'Degree_Program': 'M.Sc. AI', 'Course_Name': 'Deep Learning', 'Skill_Taught': 'PyTorch', 'Weight_in_Curriculum': 0.9},
    {'Degree_Program': 'M.Sc. AI', 'Course_Name': 'AI Ethics', 'Skill_Taught': 'Ethics', 'Weight_in_Curriculum': 0.4},
    {'Degree_Program': 'M.Sc. AI', 'Course_Name': 'Computer Vision', 'Skill_Taught': 'Python', 'Weight_in_Curriculum': 0.8},
    {'Degree_Program': 'B.Sc. Statistics', 'Course_Name': 'Probability', 'Skill_Taught': 'Stats', 'Weight_in_Curriculum': 0.9},
    {'Degree_Program': 'B.Sc. Statistics', 'Course_Name': 'Statistical Computing', 'Skill_Taught': 'R', 'Weight_in_Curriculum': 0.8},
]
df_learned_skills = pd.DataFrame(learned_skills_data)

# df_jobs
job_roles = ['Data Scientist', 'AI Engineer', 'Statistician']
companies = ['TechCorp', 'DataSys', 'AI_Labs', 'StatSolutions', 'FinTech_Global']
exp_levels = ['Entry', 'Mid', 'Senior']
skills_list = ['Python', 'SQL', 'ML', 'PyTorch', 'Stats', 'R', 'AWS', 'GCP']

job_data = []
for i in range(200):
    role = np.random.choice(job_roles)
    job_data.append({
        'Job_Role': role,
        'Company_Name': np.random.choice(companies),
        'Experience_Level': np.random.choice(exp_levels),
        'Salary_USD': np.random.randint(60000, 200000),
        'Vacancies_Count': np.random.randint(1, 50),
        'Required_Skills': ", ".join(np.random.choice(skills_list, 3, replace=False))
    })
df_jobs = pd.DataFrame(job_data)

# --- APP SETUP ---
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Colors (Cyber/Tech)
COLORS = {
    'bg': '#0f172a',
    'text': '#e2e8f0',
    'accent_teal': '#14b8a6',
    'accent_blue': '#3b82f6',
    'accent_purple': '#8b5cf6',
    'panel_bg': '#1e293b'
}

# Layout
app.layout = html.Div(style={'backgroundColor': COLORS['bg'], 'color': COLORS['text'], 'minHeight': '100vh', 'fontFamily': 'sans-serif', 'padding': '20px'}, children=[
    html.H1("AI & Data Science Job Market Dashboard", style={'textAlign': 'center', 'color': COLORS['accent_teal']}),
    
    # Global Filters & KPIs
    html.Div([
        html.Div([
            html.Label("Role Filter:"),
            dcc.Dropdown(
                id='global-role-filter',
                options=[{'label': r, 'value': r} for r in job_roles],
                value=job_roles,
                multi=True,
                style={'color': '#000'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '20px'}),
        
        html.Div([
            html.Label("Experience Filter:"),
            dcc.Dropdown(
                id='global-exp-filter',
                options=[{'label': e, 'value': e} for e in exp_levels],
                value=exp_levels,
                multi=True,
                style={'color': '#000'}
            )
        ], style={'width': '30%', 'display': 'inline-block'})
    ], style={'marginBottom': '30px', 'backgroundColor': COLORS['panel_bg'], 'padding': '20px', 'borderRadius': '10px'}),
    
    html.Div(id='kpi-cards', style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '30px'}),
    
    dcc.Tabs(id="tabs-main", value='tab-1', children=[
        dcc.Tab(label='Education Supply', value='tab-1', style={'backgroundColor': COLORS['panel_bg']}, selected_style={'backgroundColor': COLORS['accent_teal']}),
        dcc.Tab(label='Market Demand', value='tab-2', style={'backgroundColor': COLORS['panel_bg']}, selected_style={'backgroundColor': COLORS['accent_teal']}),
        dcc.Tab(label='Skill Mismatch', value='tab-3', style={'backgroundColor': COLORS['panel_bg']}, selected_style={'backgroundColor': COLORS['accent_teal']}),
    ]),
    html.Div(id='tabs-content')
])

# Callbacks
@app.callback(
    Output('kpi-cards', 'children'),
    [Input('global-role-filter', 'value'),
     Input('global-exp-filter', 'value')]
)
def update_kpis(roles, exps):
    dff_jobs = df_jobs[df_jobs['Job_Role'].isin(roles) & df_jobs['Experience_Level'].isin(exps)]
    avg_salary_en = dff_jobs[dff_jobs['Experience_Level'] == 'Entry']['Salary_USD'].mean()
    total_graduates = df_edu[df_edu['Year'] == 2026]['Graduates_Count'].sum()
    top_industry = dff_jobs.groupby('Company_Name')['Vacancies_Count'].sum().idxmax() if not dff_jobs.empty else "N/A"
    
    card_style = {'backgroundColor': COLORS['panel_bg'], 'padding': '20px', 'borderRadius': '10px', 'width': '30%', 'textAlign': 'center', 'border': f'1px solid {COLORS["accent_blue"]}'}
    
    return [
        html.Div([html.H3("Avg Starting Salary (Entry)"), html.H2(f"${avg_salary_en:,.0f}" if not pd.isna(avg_salary_en) else "N/A", style={'color': COLORS['accent_teal']})], style=card_style),
        html.Div([html.H3("Total Graduates (2026)"), html.H2(f"{total_graduates:,}", style={'color': COLORS['accent_purple']})], style=card_style),
        html.Div([html.H3("Top Hiring Company"), html.H2(f"{top_industry}", style={'color': COLORS['accent_blue']})], style=card_style),
    ]

@app.callback(Output('tabs-content', 'children'),
              Input('tabs-main', 'value'),
              Input('global-role-filter', 'value'),
              Input('global-exp-filter', 'value'))
def render_content(tab, roles, exps):
    layout_style = {'backgroundColor': COLORS['bg'], 'plot_bgcolor': COLORS['bg'], 'paper_bgcolor': COLORS['panel_bg'], 'font': {'color': COLORS['text']}}
    
    if tab == 'tab-1':
        fig_grads = px.bar(df_edu, x='Year', y='Graduates_Count', color='Degree_Program', barmode='group', title="Graduates over Time")
        fig_grads.update_layout(**layout_style)
        
        fig_tuition = px.bar(df_edu.groupby('Degree_Program')['Tuition_Fee_USD'].mean().reset_index(), x='Degree_Program', y='Tuition_Fee_USD', title="Avg Tuition Fees")
        fig_tuition.update_layout(**layout_style)
        
        return html.Div([
            html.Div([dcc.Graph(figure=fig_grads)], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(figure=fig_tuition)], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ], style={'paddingTop': '20px'})
        
    elif tab == 'tab-2':
        dff_jobs = df_jobs[df_jobs['Job_Role'].isin(roles) & df_jobs['Experience_Level'].isin(exps)]
        
        fig_salary = px.box(dff_jobs, x='Experience_Level', y='Salary_USD', color='Job_Role', title="Salary by Experience Level")
        fig_salary.update_layout(**layout_style)
        
        vacancies = dff_jobs.groupby('Job_Role')['Vacancies_Count'].sum().reset_index()
        fig_vacancies = px.bar(vacancies, x='Job_Role', y='Vacancies_Count', title="Job Vacancies")
        fig_vacancies.update_layout(**layout_style)
        
        return html.Div([
            html.Div([dcc.Graph(figure=fig_salary)], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(figure=fig_vacancies)], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ], style={'paddingTop': '20px'})
        
    elif tab == 'tab-3':
        # Skill Mismatch Logic
        taught_skills = df_learned_skills.groupby('Skill_Taught')['Weight_in_Curriculum'].sum().reset_index()
        taught_skills.rename(columns={'Weight_in_Curriculum': 'Supply'}, inplace=True)
        
        dff_jobs = df_jobs[df_jobs['Job_Role'].isin(roles)]
        all_req_skills = []
        for s in dff_jobs['Required_Skills']:
            all_req_skills.extend([x.strip() for x in s.split(',')])
        req_skills_series = pd.Series(all_req_skills).value_counts().reset_index()
        req_skills_series.columns = ['Skill_Taught', 'Demand']
        
        mismatch_df = pd.merge(taught_skills, req_skills_series, on='Skill_Taught', how='outer').fillna(0)
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=mismatch_df['Supply']/mismatch_df['Supply'].max(), theta=mismatch_df['Skill_Taught'], fill='toself', name='Supply (Taught)'))
        fig_radar.add_trace(go.Scatterpolar(r=mismatch_df['Demand']/mismatch_df['Demand'].max(), theta=mismatch_df['Skill_Taught'], fill='toself', name='Demand (Required)'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True, title="Skill Mismatch (Normalized)", **layout_style)
        
        return html.Div([dcc.Graph(figure=fig_radar)], style={'paddingTop': '20px'})

if __name__ == '__main__':
    app.run(debug=True)
