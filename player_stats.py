import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Premier League Player Stats Explorer')

st.markdown("""
This app performs webscraping of Premier League player stats
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Football-reference.com](https://www.fbref.com/)
* Send feedback [here](https://forms.gle/gZiJrreEoNPVdh7L9)
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Season', list(((f'{i-1}-{i}' for i in range(2021,2010,-1)))))


years = {
    '2020':'https://widgets.sports-reference.com/wg.fcgi?css=1&site=fb&url=%2Fen%2Fcomps%2F9%2F10728%2Fstats%2F2020-2021-Premier-League-Stats&div=div_stats_standard',
    '2019':'https://widgets.sports-reference.com/wg.fcgi?css=1&site=fb&url=%2Fen%2Fcomps%2F9%2F3232%2Fstats%2F2019-2020-Premier-League-Stats&div=div_stats_standard',
    '2018':'https://widgets.sports-reference.com/wg.fcgi?css=1&site=fb&url=%2Fen%2Fcomps%2F9%2F1889%2Fstats%2F2018-2019-Premier-League-Stats&div=div_stats_standard',
    '2017':'https://widgets.sports-reference.com/wg.fcgi?css=1&site=fb&url=%2Fen%2Fcomps%2F9%2F1631%2Fstats%2F2017-2018-Premier-League-Stats&div=div_stats_standard',
    '2016':'https://widgets.sports-reference.com/wg.fcgi?css=1&site=fb&url=%2Fen%2Fcomps%2F9%2F1526%2Fstats%2F2016-2017-Premier-League-Stats&div=div_stats_standard',
    '2015':'https://widgets.sports-reference.com/wg.fcgi?css=1&site=fb&url=%2Fen%2Fcomps%2F9%2F733%2Fstats%2F2014-2015-Premier-League-Stats&div=div_stats_standard',
    '2014':'https://widgets.sports-reference.com/wg.fcgi?css=1&site=fb&url=%2Fen%2Fcomps%2F9%2F733%2Fstats%2F2014-2015-Premier-League-Stats&div=div_stats_standard',
    '2013':'https://widgets.sports-reference.com/wg.fcgi?css=1&site=fb&url=%2Fen%2Fcomps%2F9%2F669%2Fstats%2F2013-2014-Premier-League-Stats&div=div_stats_standard',
    '2012':'https://widgets.sports-reference.com/wg.fcgi?css=1&site=fb&url=%2Fen%2Fcomps%2F9%2F602%2Fstats%2F2012-2013-Premier-League-Stats&div=div_stats_standard',
    '2011':'https://widgets.sports-reference.com/wg.fcgi?css=1&site=fb&url=%2Fen%2Fcomps%2F9%2F534%2Fstats%2F2011-2012-Premier-League-Stats&div=div_stats_standard',
    '2010':'https://widgets.sports-reference.com/wg.fcgi?css=1&site=fb&url=%2Fen%2Fcomps%2F9%2F467%2Fstats%2F2010-2011-Premier-League-Stats&div=div_stats_standard'
}

@st.cache
def load_data(year):
    url = years[year[:year.index('-')]]
    html = pd.read_html(url)
    df = html[0]
    df = df.drop(['Per 90 Minutes'], axis=1)
    df.columns = df.columns.map(lambda x : x[1])
    index_names = df[df['Player']=='Player'].index
    raw = df.drop(labels=index_names,axis=0)
    raw = raw.reset_index()
    raw = raw.drop(['index'],axis=1)
    raw['Nation'] = raw['Nation'].apply(lambda x: (x.split(' '))[-1])
    raw = raw.drop(['Matches'],axis=1)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats

playerstats = load_data(selected_year)


sorted_unique_team = sorted(playerstats['Squad'].unique())
selected_team = st.sidebar.multiselect('Club', sorted_unique_team, sorted_unique_team, help='Select the clubs to display players\' stats')

unique_pos = sorted(playerstats['Pos'].unique())
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos, help='Select positions to display players\' stats')

df_selected_team = playerstats[(playerstats['Squad'].isin(selected_team)) & (playerstats['Pos'].isin(selected_pos))]

st.header('Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

help_text = 'Pos: \n GK - Goalkeepers'

if st.button('Glossary'):
    st.info(''' **Pos:** GK - Goalkeepers
DF - Defenders
MF - Midfielders
FW - Forwards
FB - Fullbacks
LB - Left Backs
RB - Right Backs
CB - Center Backs
DM - Defensive Midfielders
CM - Central Midfielders
LM - Left Midfielders
RM - Right Midfielders
WM - Wide Midfielders
LW - Left Wingers
RW - Right Wingers
AM - Attacking Midfielders

**MP:** Matches Played. Matches Played by the player or squad

**Starts:** Starts. Game or games started by player

**Min:** Minutes played.

**90s:** Number of 90s played. Minutes played divided by 90

**Gls:** Goals. Goals scored or allowed

**Ast:** Assists.

**G-PK:** Non-Penalty Goals.

**PK:** Penalty Kicks Made.

**PKatt:** Penalty Kicks Attempted.

**CrdY:** Yellow Cards.

**CrdR:** Red Cards.

**xG:** Expected Goals. xG totals include penalty kicks, but do not include penalty shootouts (unless otherwise noted).

**npxG:** Non-Penalty Expected Goals.

**xA:** xG Assisted. xG which follows a pass that assists a shot

**npxG+xA:** Non-Penalty Expected Goals plus xG Assisted. xG totals include penalty kicks, but do not include penalty shootouts (unless otherwise noted).


''')


def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

st.set_option('deprecation.showPyplotGlobalUse', False)

if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    st.write('An Intercorrelation Heatmap is a graphical representation of a correlation matrix representing correlation between different variables. ')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    c = df.corr()
    mask = np.zeros_like(c)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(5, 5))
        ax = sns.heatmap(c, mask=mask, vmax=1, square=True, cmap='Blues')
    st.pyplot()