import streamlit as st 
import numpy as np 
import pandas as pd 
import base64
import seaborn as sb
import matplotlib.pyplot as plt
import streamlit.components.v1 as stc
import codecs

st.title('NBA Player Stats Explorers')

st.markdown("""
This app performs simple webscriping of NBA player stats data

* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/leagues/NBA_2020_per_game.html) 

* **Glossary:** List of glossay informations
""")
html_file = codecs.open('glossary.html','r')
page = html_file.read()
stc.html(page,width=500,height=200,scrolling=True)

# Create a sidebar menu for a web
st.sidebar.header('User Input feature: ')
# Sidebar year select
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1980,2020))))

# Webscriping data from html page
@st.cache 
def load_data(year):
	url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
	html = pd.read_html(url, header = 0)
	df = html[0]
	raw = df.drop(df[df.Age == 'Age'].index) #Delete the header row of the table
	player_stats = raw.drop(['Rk'], axis = 1)
	return player_stats
player_stats = load_data(selected_year)

# Sidebar team select
sorted_unique_team = sorted(player_stats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
selected_pos = st.sidebar.multiselect("Position", unique_pos, unique_pos)

# Filtering data
df_selected_team = player_stats[(player_stats.Tm.isin(selected_team) & player_stats.Pos.isin(selected_pos))]

st.header('Display Player stats of selected team: ')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + 'row and ' + str(df_selected_team.shape[1]) + 'column.')
st.dataframe(df_selected_team)

# Download NBA player stats data 
def file_download(df):
	csv = df.to_csv(index = False)
	b64 = base64.b64encode(csv.encode()).decode() # String to bite convertion
	href = f'<a href="data:file/csv;base64,{b64}" download="player_stars.csv">Download CSV file</a>'
	return href 

st.markdown(file_download(df_selected_team), unsafe_allow_html = True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
	st.header('Intercorrelation Matrix Heatmap: ')
	df_selected_team.to_csv('ouput.csv', index = False)
	df = pd.read_csv('/Users/york/Tensor1/Sublime_Project/Strealit_App/Bassketball_data_analysis/output.csv')

	corr = df.corr()
	mask = np.zeros_like(corr)
	mask[np.triu_indices_from(mask)] = True
	with sns.axes_style("white"):
		f, ax = plt.subplots(figsize = (7, 5))
		ax = sns.heatmap(corr, mask = mask, vmax = 1, square = True)
	st.pyplot()




