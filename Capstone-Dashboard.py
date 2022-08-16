from sre_parse import State
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import pymssql

# from config import database
# from config import username
# from config import password
# from config import server

# try:
#     conn = pymssql.connect(server, username, password, database)

#     cursor = conn.cursor()
#     query = '''
#     select AVG(DataValue) as DataValue, IndicatorLabel, GroupLabel, AgeLabel, SexLabel, RaceLabel, EducationLabel, StateLabel
#     from InsuranceCoverage
#     inner join Indicator on Indicator.IndicatorID = InsuranceCoverage.IndicatorID
#     inner join [Group] on [Group].GroupID = InsuranceCoverage.GroupID
#     left join Age on Age.AgeID = InsuranceCoverage.AgeID
#     left join Sex on Sex.SexID = InsuranceCoverage.SexID
#     left join Race on Race.RaceID = InsuranceCoverage.RaceID
#     left join Education on Education.EducationID = InsuranceCoverage.EducationID
#     left join [State] on [State].StateID = InsuranceCoverage.StateID
#     inner join Week on Week.WeekID = InsuranceCoverage.WeekID
#     group by IndicatorLabel, GroupLabel, AgeLabel, SexLabel, RaceLabel, EducationLabel, StateLabel
#     '''
#     df = pd.read_sql(query, conn)
# except Exception as e:
#     print(e)

# print(df.info())

# df2 = df[[]]
# print(df2)

# fig = px.scatter(df2, x='', y='', title='')

# df3 = df[[]]
# fig2 = px.scater(df3, x='', y='', title='')

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
        html.H2('Sidebar', className='display-4'),
        html.Hr(),
        html.P(
            'A sidebar with collapsible navigation links', className='lead'
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
        [State(f"submenu-{i}-collapse", "is_open")],
    )(toggle_collapse)

    app.callback(
        Output(f"submenu-{i}", "className"),
        [Input(f"submenu-{i}-collapse", "is_open")],
    )(set_navitem_class)

@app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname in ['/', '/health-costs/1']:
        return html.P("this is the health costs by demographics page")
    elif pathname == '/health-costs/2':
        return html.P("this is the ML model page")
    elif pathname == '/insured-status/1':
        return html.P("this is the insured status by demographics page")
    elif pathname == '/insured-status/2':
        return html.P('this is the insured status by income page')
    return dbc.Jumbotron(
        [
            html.H1("404: Not Found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized")
        ]
    )

if __name__ == '__main__':
    app.run_server(port=8888, debug=True)