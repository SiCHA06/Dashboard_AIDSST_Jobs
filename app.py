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

# df_jobs (REAL DATA from ds_salaries.csv)
url = "https://raw.githubusercontent.com/arminnorouzi/sparkml/main/Data/ds_salaries.csv"
real_df = pd.read_csv(url)

# Map and clean
real_df['Experience_Level'] = real_df['experience_level'].map({'EN': 'Entry', 'MI': 'Mid', 'SE': 'Senior', 'EX': 'Executive'})
real_df.rename(columns={'job_title': 'Job_Role', 'salary_in_usd': 'Salary_USD', 'company_location': 'Company_Name'}, inplace=True)

# Generate realistic mock required skills based on Job Role since they are missing from the raw CSV
skills_list = ['Python', 'SQL', 'ML', 'PyTorch', 'Stats', 'R', 'AWS', 'GCP', 'Tableau', 'Excel']
real_df['Required_Skills'] = [", ".join(np.random.choice(skills_list, 3, replace=False)) for _ in range(len(real_df))]
real_df['Vacancies_Count'] = 1

df_jobs = real_df[['Job_Role', 'Company_Name', 'Experience_Level', 'Salary_USD', 'Vacancies_Count', 'Required_Skills']].dropna()

# Keep top 10 roles to avoid UI clutter
job_roles = df_jobs['Job_Role'].value_counts().nlargest(10).index.tolist()
df_jobs = df_jobs[df_jobs['Job_Role'].isin(job_roles)]

exp_levels = df_jobs['Experience_Level'].unique().tolist()

# --- APP SETUP ---
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Colors (Cyber/Tech) based on Style Guide
COLORS = {
    'bg': '#12131F',
    'sidebar_bg': '#0B0C15',
    'panel_bg': '#1C1D2D',
    'text': '#FFFFFF',
    'text_muted': '#8C8E9F',
    'accent_magenta': '#C738FF',
    'accent_cyan': '#00E5FF',
}

def apply_neon_theme(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text_muted'], family='Inter, sans-serif'),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=True, gridcolor='#28293D', gridwidth=1, zeroline=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor='#28293D', gridwidth=1, zeroline=False, showline=False)
    )
    return fig

# Layout
app.layout = html.Div(style={'backgroundColor': COLORS['bg'], 'color': COLORS['text'], 'minHeight': '100vh', 'fontFamily': 'Inter, sans-serif', 'padding': '20px'}, children=[
    html.H1("AI & Data Science Job Market Dashboard", style={'textAlign': 'center', 'color': COLORS['text'], 'marginBottom': '30px'}),
    
    # Global Filters & KPIs
    html.Div([
        html.Div([
            html.Label("Role Filter:", style={'color': COLORS['text_muted']}),
            dcc.Dropdown(
                id='global-role-filter',
                options=[{'label': r, 'value': r} for r in job_roles],
                value=job_roles,
                multi=True,
                style={'color': '#000'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '20px'}),
        
        html.Div([
            html.Label("Experience Filter:", style={'color': COLORS['text_muted']}),
            dcc.Dropdown(
                id='global-exp-filter',
                options=[{'label': e, 'value': e} for e in exp_levels],
                value=exp_levels,
                multi=True,
                style={'color': '#000'}
            )
        ], style={'width': '30%', 'display': 'inline-block'})
    ], style={'marginBottom': '30px', 'backgroundColor': COLORS['sidebar_bg'], 'padding': '20px', 'borderRadius': '16px', 'boxShadow': '0px 8px 24px rgba(0, 0, 0, 0.2)'}),
    
    html.Div(id='kpi-cards', style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '30px'}),
    
    dcc.Tabs(id="tabs-main", value='tab-1', children=[
        dcc.Tab(label='Education Supply', value='tab-1', style={'backgroundColor': COLORS['panel_bg'], 'color': COLORS['text_muted'], 'border': 'none'}, selected_style={'backgroundColor': COLORS['panel_bg'], 'color': COLORS['accent_magenta'], 'borderTop': f'4px solid {COLORS["accent_magenta"]}'}),
        dcc.Tab(label='Market Demand', value='tab-2', style={'backgroundColor': COLORS['panel_bg'], 'color': COLORS['text_muted'], 'border': 'none'}, selected_style={'backgroundColor': COLORS['panel_bg'], 'color': COLORS['accent_magenta'], 'borderTop': f'4px solid {COLORS["accent_magenta"]}'}),
        dcc.Tab(label='Skill Mismatch', value='tab-3', style={'backgroundColor': COLORS['panel_bg'], 'color': COLORS['text_muted'], 'border': 'none'}, selected_style={'backgroundColor': COLORS['panel_bg'], 'color': COLORS['accent_magenta'], 'borderTop': f'4px solid {COLORS["accent_magenta"]}'}),
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
    
    card_base = {
        'borderRadius': '16px',
        'padding': '20px',
        'width': '30%',
        'textAlign': 'center',
        'boxShadow': '0px 8px 24px rgba(0, 0, 0, 0.2)',
        'border': 'none',
        'color': '#FFFFFF'
    }
    
    card1 = {**card_base, 'background': 'linear-gradient(135deg, #FF6BFF 0%, #C738FF 100%)'}
    card2 = {**card_base, 'background': 'linear-gradient(135deg, #00E5FF 0%, #0088FF 100%)'}
    card3 = {**card_base, 'background': 'linear-gradient(135deg, #FF6BFF 0%, #C738FF 100%)'}
    
    return [
        html.Div([html.H3("Avg Starting Salary (Entry)", style={'color': '#FFFFFF'}), html.H2(f"${avg_salary_en:,.0f}" if not pd.isna(avg_salary_en) else "N/A")], style=card1),
        html.Div([html.H3("Total Graduates (2026)", style={'color': '#FFFFFF'}), html.H2(f"{total_graduates:,}")], style=card2),
        html.Div([html.H3("Top Hiring Company", style={'color': '#FFFFFF'}), html.H2(f"{top_industry}")], style=card3),
    ]

@app.callback(Output('tabs-content', 'children'),
              Input('tabs-main', 'value'),
              Input('global-role-filter', 'value'),
              Input('global-exp-filter', 'value'))
def render_content(tab, roles, exps):
    card_container = {'backgroundColor': COLORS['panel_bg'], 'borderRadius': '16px', 'padding': '20px', 'boxShadow': '0px 8px 24px rgba(0, 0, 0, 0.2)', 'border': 'none'}
    
    if tab == 'tab-1':
        fig_grads = px.bar(df_edu, x='Year', y='Graduates_Count', color='Degree_Program', barmode='group', title="Graduates over Time")
        fig_grads.update_traces(marker_line_width=0, opacity=0.8)
        fig_grads = apply_neon_theme(fig_grads)
        
        fig_tuition = px.bar(df_edu.groupby('Degree_Program')['Tuition_Fee_USD'].mean().reset_index(), x='Degree_Program', y='Tuition_Fee_USD', title="Avg Tuition Fees")
        fig_tuition.update_traces(marker_color=COLORS['accent_cyan'], marker_line_width=0, opacity=0.8)
        fig_tuition = apply_neon_theme(fig_tuition)
        
        return html.Div([
            html.Div([dcc.Graph(figure=fig_grads)], style={**card_container, 'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(figure=fig_tuition)], style={**card_container, 'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ], style={'paddingTop': '20px'})
        
    elif tab == 'tab-2':
        dff_jobs = df_jobs[df_jobs['Job_Role'].isin(roles) & df_jobs['Experience_Level'].isin(exps)]
        
        fig_salary = px.box(dff_jobs, x='Experience_Level', y='Salary_USD', color='Job_Role', title="Salary by Experience Level")
        fig_salary = apply_neon_theme(fig_salary)
        
        vacancies = dff_jobs.groupby('Job_Role')['Vacancies_Count'].sum().reset_index()
        fig_vacancies = px.bar(vacancies, x='Job_Role', y='Vacancies_Count', title="Job Vacancies")
        fig_vacancies.update_traces(marker_color=COLORS['accent_cyan'], marker_line_width=0, opacity=0.8)
        fig_vacancies = apply_neon_theme(fig_vacancies)
        
        return html.Div([
            html.Div([dcc.Graph(figure=fig_salary)], style={**card_container, 'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(figure=fig_vacancies)], style={**card_container, 'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ], style={'paddingTop': '20px'})
        
    elif tab == 'tab-3':
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
        fig_radar.add_trace(go.Scatterpolar(r=mismatch_df['Supply']/mismatch_df['Supply'].max(), theta=mismatch_df['Skill_Taught'], fill='toself', name='Supply (Taught)', fillcolor='rgba(199, 56, 255, 0.2)', line=dict(color=COLORS['accent_magenta'], width=2)))
        fig_radar.add_trace(go.Scatterpolar(r=mismatch_df['Demand']/mismatch_df['Demand'].max(), theta=mismatch_df['Skill_Taught'], fill='toself', name='Demand (Required)', fillcolor='rgba(0, 229, 255, 0.2)', line=dict(color=COLORS['accent_cyan'], width=2)))
        
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, gridcolor='#28293D'), angularaxis=dict(gridcolor='#28293D', linecolor='#28293D')), showlegend=True, title="Skill Mismatch (Normalized)")
        fig_radar = apply_neon_theme(fig_radar)
        
        return html.Div([dcc.Graph(figure=fig_radar)], style={**card_container, 'paddingTop': '20px'})

if __name__ == '__main__':
    app.run(debug=True)
