import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import pymssql

from config import database
from config import username
from config import password
from config import server

try:
    conn = pymssql.connect(server, username, password, database)

    cursor = conn.cursor()
    querycoverage = '''
    select AVG(DataValue) as DataValue, IndicatorLabel, GroupLabel, AgeLabel, SexLabel, RaceLabel, EducationLabel, StateLabel
    from InsuranceCoverage
    inner join Indicator on Indicator.IndicatorID = InsuranceCoverage.IndicatorID
    inner join [Group] on [Group].GroupID = InsuranceCoverage.GroupID
    left join Age on Age.AgeID = InsuranceCoverage.AgeID
    left join Sex on Sex.SexID = InsuranceCoverage.SexID
    left join Race on Race.RaceID = InsuranceCoverage.RaceID
    left join Education on Education.EducationID = InsuranceCoverage.EducationID
    left join [State] on [State].StateID = InsuranceCoverage.StateID
    inner join Week on Week.WeekID = InsuranceCoverage.WeekID
    group by IndicatorLabel, GroupLabel, AgeLabel, SexLabel, RaceLabel, EducationLabel, StateLabel
    order by DataValue desc
    '''
    dfcoverage = pd.read_sql(querycoverage, conn)

    querycosts = '''Select I.ChargeID, I.ChargeValue, I.AgeID, A.AgeLabel, I.ChildrenID, C.ChildrenLabel, I.RegionID, 
    R.RegionLabel, I.SexID, S.SexLabel, I.SmokerID, Sm.SmokerLabel, I.BMI from InsuranceCharges I
    inner join Age A on I.AgeID = A.AgeID
    inner join Children C on  I.ChildrenID = C.ChildrenID
    inner join Region R on  I.RegionID = R.RegionID
    inner join Sex S on  I.SexID = S.SexID
    inner join Smoker Sm on  I.SmokerID = Sm.SmokerID
    '''
    dfcosts = pd.read_sql(querycosts, conn)

    querycosts2 = '''Select avg(I.ChargeValue) as ChargeValue, C.ChildrenLabel 
    from InsuranceCharges I
    inner join Children C on  I.ChildrenID = C.ChildrenID
    group by C.ChildrenLabel
    '''

    querysahie = '''
    select *
    from SAHIE
    left join Income on Income.IncomeID = SAHIE.IncomeID
    left join State on State.StateID = SAHIE.StateID
    left join Age on Age.AgeID = SAHIE.AgeID
    left join Sex on Sex.SexID = SAHIE.SexID
    left join Race on Race.RaceID = SAHIE.RaceID
    left join Geocat on Geocat.GeoID = SAHIE.GeoID
    '''
    dfsahie = pd.read_sql(querysahie, conn)

except Exception as e:
    print(e)

dfcoverage2 = dfcoverage[['IndicatorLabel','DataValue', 'EducationLabel']]
#print(df2)
figcoverage = px.bar(dfcoverage2, x='EducationLabel', y='DataValue', color='IndicatorLabel', title='Education vs Insured Status', 
labels={'EducationLabel':'Highest Obtained Education', 'DataValue':'Percentage Insured'}, barmode='group')

dfcoverage3 = dfcoverage[['IndicatorLabel','DataValue', 'SexLabel']]
figcoverage2 = px.bar(dfcoverage3, x='SexLabel', y='DataValue', color='IndicatorLabel', 
title='Sex vs Insured Status', barmode='group', height=400, width=1000)

dfcoverage4 = dfcoverage[dfcoverage['IndicatorLabel'] == 'Uninsured at the Time of Interview']
dfcoverage4 = dfcoverage4[['IndicatorLabel','DataValue', 'StateLabel']]
dfcoverage4 = dfcoverage4.head(10)
figcoverage3 = px.bar(dfcoverage4, x='StateLabel', y='DataValue', color='IndicatorLabel', 
title='Top 5 States by Percentage Uninsured', barmode='group', range_y=(0,25), height=400, width=1000)

dfcoverage5 = dfcoverage[dfcoverage['IndicatorLabel'] == 'Uninsured at the Time of Interview']
dfcoverage5 = dfcoverage5[['IndicatorLabel','DataValue', 'StateLabel']]
dfcoverage5 = dfcoverage5.tail(6)
figcoverage4 = px.bar(dfcoverage5, x='StateLabel', y='DataValue', color='IndicatorLabel', 
title='Bottom 5 States by Percentage Uninsured', barmode='group', range_y=(0,25), height=400, width=1000)

#########################################################################################################

agedf = dfcosts[['ChargeValue', 'AgeID', 'AgeLabel', 'SmokerLabel']]
agedf = agedf.sort_values('AgeLabel')
figcosts = px.scatter(agedf, x='AgeLabel', y='ChargeValue', color='SmokerLabel', 
title='Age vs Health Costs', labels={'AgeLabel':'Age', 'ChargeValue':'Health Costs'}, height=400, width=800)

bmiDF = dfcosts[['ChargeValue', 'BMI', 'SmokerLabel']]
figcosts2 = px.scatter(bmiDF, x='BMI', y='ChargeValue', color='SmokerLabel', title='Body Mass Index (BMI) vs Health Costs', 
labels={'BMI':'Body Mass Index (BMI)', 'ChargeValue':'Health Costs'}, height=400, width=800)

childDf = pd.read_sql(querycosts2, conn)
figcosts3 = px.bar(childDf, x='ChildrenLabel', y='ChargeValue', title='Number of Children vs Average Health Costs', 
labels={'ChargeValue':'Average Health Costs', 'ChildrenLabel':'Number of Children'}, height=400, width=800)

regiondf = dfcosts[['ChargeValue', 'RegionID', 'RegionLabel']]
regiondf = regiondf.sort_values('RegionID')
figcosts4 = px.histogram(regiondf, x='RegionLabel', y='ChargeValue', 
labels={'ChargeValue':'Health Costs', 'RegionLabel':'Region'}, title='Total Health Costs per Region', height=400, width=800)

sexdf = dfcosts[['ChargeValue', 'SexID', 'SexLabel']]
figcosts5 = px.box(sexdf, x='SexLabel', y='ChargeValue', 
labels={'ChargeValue':'Health Costs', 'SexLabel':'Sex'}, title='Sex vs Health Costs', height=800, width=800)

smokerdf = dfcosts[['ChargeValue', 'SmokerID', 'SmokerLabel']]
smokerdf = smokerdf.sort_values('SmokerLabel')
figcosts6 = px.box(smokerdf, x='SmokerLabel', y='ChargeValue', 
labels={'ChargeValue':'Health Costs', 'SmokerLabel':'Smoker Status'}, title='Smoking Status vs Health Costs', height=800, width=800)

########################################################################################################

sahie_income = dfsahie
sahie_income = sahie_income[['IncomeLabel', 'Percent_of_Demographic_Insured_by_Income_Category']]
sahie_income = sahie_income.groupby('IncomeLabel')['Percent_of_Demographic_Insured_by_Income_Category'].mean().reset_index(name='Mean Percentage Insured').sort_values('Mean Percentage Insured')
sahie_income = sahie_income[sahie_income['IncomeLabel'] != 'Between 138% - 400% of poverty'].rename(columns={'IncomeLabel':'Income Category'})
figsahie = px.bar(sahie_income, x='Income Category', y='Mean Percentage Insured', title='Percentage Insured by Income Category')

sahie_states = dfsahie.loc[
    (dfsahie['IncomeLabel'] == 'At or below 138% of poverty') &
    (dfsahie['AgeLabel'] == 'Under 65 years') &
    (dfsahie['GeoCategory'] == 'State geographic identifier') &
    (dfsahie['SexLabel'] == 'both sexes') &
    (dfsahie['RaceLabel'] == 'All races')
]
sahie_states = sahie_states[['StateLabel', 'Percent_of_Demographic_Insured_by_Income_Category']].sort_values('Percent_of_Demographic_Insured_by_Income_Category')
sahie_states = sahie_states.rename(columns={'StateLabel':'State', 'Percent_of_Demographic_Insured_by_Income_Category':'Percentage Insured'})

least_insured = sahie_states.head(5)
figsahie2 = px.bar(least_insured, x='State', y='Percentage Insured', 
title='Bottom 5 States by Percentage of Low Income Category Insured')

most_insured = sahie_states.sort_values('Percentage Insured', ascending=False).head(5)
figsahie3 = px.bar(most_insured, x='State', y='Percentage Insured', 
title='Top 5 States by Percentage of Low Income Category Insured')

least_group = dfsahie.loc[
    (dfsahie['GeoCategory'] == 'State geographic identifier')&
    (dfsahie['IncomeLabel'] != 'All income levels') &
    (dfsahie['IncomeLabel'] != 'Between 138% - 400% of poverty') &
    (dfsahie['AgeLabel'] != 'Under 65 years') &
    (dfsahie['SexLabel'] != 'both sexes') &
    (dfsahie['RaceLabel'] == 'All races')
]
least_group = least_group.groupby(by=['SexLabel','AgeLabel','IncomeLabel']).mean().reset_index()
least_group = least_group.sort_values('Percent_of_Demographic_Uninsured_by_Income_Category', ascending=False).drop(columns=['CountyID','SAHIEID','Total_Percent_of_Demographic_Uninsured','Total_Percent_of_Demographic_Insured','Percent_of_Demographic_Insured_by_Income_Category'])
least_group = least_group.rename(columns={'IncomeLabel':'Income Level', 'Percent_of_Demographic_Uninsured_by_Income_Category':'Mean Percentage Uninsured'})
least_group['Demographic'] = least_group['SexLabel'] + ', ' + least_group['AgeLabel'] + ', ' + least_group['Income Level']
figsahie4 = px.bar(least_group.head(10), x='Demographic', y='Mean Percentage Uninsured')

#Link to fontawesome to get chevron icons
FA = 'https://use.fontawesome.com/releases/v5.8.1/css/all.css'

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

#Style arguments of the sidebar

SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '16rem',
    'padding': '2rem 1rem',
    'background-color': '#f8f9fa',
}

#Styles for the main content
#Position it to the right of the sidebar and add padding
CONTENT_STYLE = {
    'margin-left': '18rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
}

submenu_1 = [
    html.Li(
        #use row and col components to position chevrons
        dbc.Row(
            [
                dbc.Col('Health Costs'),
                dbc.Col(
                    html.I(className='fas fa-chevron-right me-3'),
                    width='auto',
                ),
            ],
            className='my-1',
        ),
        style={'cursor': 'pointer'},
        id='submenu-1',
    ),
    #Use collapse component to hide and reveal the navigation links
    dbc.Collapse(
        [
            dbc.NavLink('Demographics', href='/health-costs/1'),
            dbc.NavLink('Predictive Model', href='/health-costs/2'),
        ],
        id='submenu-1-collapse',
    ),
]

submenu_2 = [
    html.Li(
        dbc.Row(
            [
                dbc.Col('Insured Status'),
                dbc.Col(
                    html.I(className='fas fa-chevron-right me-3'),
                    width='auto',
                ),
            ],
            className = 'my-1',
        ),
        style={'cursor': 'pointer'},
        id='submenu-2',
    ),
    dbc.Collapse(
        [
            dbc.NavLink('Demographics', href='/insured-status/1'),
            dbc.NavLink('Income Category', href='/insured-status/2'),
        ],
        id='submenu-2-collapse',
    ),
]

sidebar = html.Div(
    [
        html.H2('Health Insurance Data', className='display-4'),
        html.Hr(),
        html.P(
            'Visualizations with data pertaining to health insurance', className='lead'
        ),
        dbc.Nav(submenu_1 + submenu_2, vertical=True),
    ],
    style=SIDEBAR_STYLE,
    id='sidebar',
)

content = html.Div(id='page-content', style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id='url'), sidebar, content])

#Toggle the is_open property of each collapse
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

#Applies the "open" class to rotate the chevron
def set_navitem_class(is_open):
    if is_open:
        return "open"
    return ""

for i in [1,2]:
    app.callback(
        Output(f"submenu-{i}-collapse", "is_open"),
        [Input(f"submenu-{i}", "n_clicks")],
        [State(f"submenu-{i}-collapse", "is_open")]
    )(toggle_collapse)

    app.callback(
        Output(f"submenu-{i}", "className"),
        [Input(f"submenu-{i}-collapse", "is_open")],
    )(set_navitem_class)

@app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname in ['/', '/health-costs/1']:
        return dcc.Graph(
            id='Health Costs',
            figure=figcosts), dcc.Graph(
                id='Health Costs', 
                figure=figcosts2), dcc.Graph(
                    id='Health Costs', 
                    figure=figcosts3), dcc.Graph(
                        id='Health Costs', 
                        figure=figcosts4), dcc.Graph(
                            id='Health Costs', 
                            figure=figcosts5), dcc.Graph(
                                id='Health Costs', 
                                figure=figcosts6)
    elif pathname == '/health-costs/2':
        return html.P("this is the ML model page")
    elif pathname == '/insured-status/1':
        return dcc.Graph(
            id='Insured Status',
            figure=figcoverage), dcc.Graph(
                id='Insured Status', 
                figure=figcoverage2), dcc.Graph(
                    id='Insured Status', 
                    figure=figcoverage3), dcc.Graph(
                        id='Insured Status', 
                        figure=figcoverage4)
    elif pathname == '/insured-status/2':
        return dcc.Graph(
            id='Insured Status Income',
            figure=figsahie), dcc.Graph(
                id='Insured Status Income', 
                figure=figsahie2), dcc.Graph(
                    id='Insured Status Income', 
                    figure=figsahie3), dcc.Graph(
                        id='Insured Status Income', 
                        figure=figsahie4)
    return dbc.Jumbotron(
        [
            html.H1("404: Not Found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized")
        ]
    )

if __name__ == '__main__':
    app.run_server(port=8888, debug=True)