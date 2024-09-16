import requests # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import matplotlib.pyplot as plt # type: ignore

#This will send an HTTP get request to the website containing the data we need
soccerurl = "https://www.marca.com/en/football/champions-league/winners.html"
response = requests.get(soccerurl)

#Parse the HTML content of the webpage using Beautiful Soup. This allows us to navigate through the HTML structure to search for specific elements and extract data more easily. 
soup = BeautifulSoup(response.content, "html.parser")

#Find the table containg the data. Searches for '<table>' element with the class "ue-table-record".When found, it is assigned to the variable 'table' allowing us to access the tables content.
table = soup.find("table", {"class": "ue-table-record"})

#extract the data from the table
UCLwinners = []

#Iterate through each row of the table, skipping the header row which has an index of 0.
for row in table.find_all("tr")[1:]:
    #find all table data (columns) within the row
    columns = row.find_all("td")

    #Checks if the row contains enough columns
    if len(columns) >= 2:
        #Extract the text from the second column (index 1), which contains the name of the teams that have won the competition.
        winners = columns[1].text.strip()
        #Append the winner's name to the list of winners.
        UCLwinners.append(winners)
    else:
        #This will handle the situation if there are no rows without enough columns
        print("Skipping row:", row)

#Count the number of wins for each team.
from collections import Counter
win_counts = Counter(UCLwinners)

#UPDATED CODE TO FIX ERROR
#Combine "Inter" and "Inter Milan" into one team.
inter_variations = ["Inter", "Inter Milan"] #List of variation for the team name
inter_milan_count = 0                         #Initialize count for Inter Milan
for team in list(win_counts.keys()):           #Loop through each team in the dictionary of win counts
    for variation in inter_variations:         #Check each variation to see if it's part of the current team's name
        if variation in team:
            inter_milan_count += win_counts[team]  #If a variaiton is found in the team's name, add its count to Inter Milan count
            del win_counts[team]  #Delete the original team entry to combine it with "Inter Milan"
            break                 #Break the loop to avoid double-counting if both "Inter" and "Inter Milan" are in the team name

win_counts["Inter Milan"] = inter_milan_count #Update the count for "Inter Milan" with the combined total

# Sort the win_counts dictionary by values in descending order
sorted_win_counts = dict(sorted(win_counts.items(), key=lambda item: item[1], reverse=True))

# Extract teams and the amount of times they won the competition from the sorted dictionary
teams = list(sorted_win_counts.keys())
titles = list(sorted_win_counts.values())

# Define a dictionary mapping each team to a specific hex color value
team_colors = {
    'Real Madrid': '#FCBF00', 
    'Milan': '#b52e2b',      
    'Bayern Munchen': '#DC052D', 
    'Liverpool': '#C8102E',     
    'Barcelona': '#A50044',     
    'Ajax': '#D2122E',          
    'Manchester U.': '#DA291C',  
    'Inter Milan': '#010E80',   
    'Juventus': '#000000',      
    'Nottingam F.': '#DD0000',  
    'Porto': '#00428C',         
    'Chelsea': '#034694',       
    'Marseilles': '#2FAEE0',     
    'Borussia D.': '#F8D503',  
    'Feyenoord': '#ae9962',     
    'Benfica': '#ED1C24',       
    'PSV': '#F00000', 
    'Steaua B.': '#132e52',   
    'Hamburg': '#0A3F86',
    'Aston Villa': '#670E36',
    'Celitc Glasg.': '#018749',
    'Manchester City': '#6CABDD',
    'Red Star': '#D50032' 
}

# This next portion of code will be used to visualize the data.
plt.figure(figsize=(10, 8))

# Plot bars with assigned colors
for i, team in enumerate(teams):
    plt.barh(team, titles[i], color=team_colors.get(team, '#999999'))  

plt.xlabel('Number of UEFA Champions League Titles')  # Label for the x-axis
plt.ylabel('Team')  # Label for y-axis
plt.title('UEFA Champion League Titles Won by Team')  # Title of the plot
plt.gca().invert_yaxis()  # Invert the y-axis to display the team with the most titles on top
plt.show()  # Used to execute final plot
