from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)


@app.route('/')
def cricbay():
    html_text = requests.get('https://sports.ndtv.com/cricket/live-scores').text
    soup = BeautifulSoup(html_text, "html.parser")
    sect = soup.find_all('div', class_='sp-scr_wrp vevent')
    section = sect[0]
    current_block = section.find('div', class_='scr_inf-wrp')
    current = current_block.find('div', class_='scr_dt-red').text
    teams_block = section.find_all('div', class_='scr_tm-wrp')
    team_a = teams_block[0].text
    team_b = teams_block[1].text
    text_only = section.find_all('div', class_='scr_txt-ony')
    team_a_score = 'Not Avaialable'
    team_b_score = 'Not Avaialable'
    link = "https://sports.ndtv.com/" + section.find('a',class_='scr_ful-sbr-txt').get('href')
    if 'Yet' in team_a:
        ind = team_a.index('Yet')
        team_a = team_a[:-(len(team_a) - ind)]
        team_a_score = 'Yet to Bat'
    else:
        if 'Not Avaialable' not in team_a:
            ind = 0
            for j, c in enumerate(team_a):
                if c.isdigit():
                    ind = j
                    break
            team_a_score = team_a[ind:]
            team_a = team_a[:-(len(team_a) - ind)]
    if 'Yet' in team_b:
        ind = team_b.index('Yet')
        team_b = team_b[:-(len(team_b) - ind)]
        team_b_score = 'Yet to Bat'
    else:
        if 'Not Available' not in team_b:
            ind = 0
            for j, c in enumerate(team_b):
                if c.isdigit():
                    ind = j
                    break
            team_b_score = team_b[ind:]
            team_b = team_b[:-(len(team_b) - ind)]
    description = text_only[0].text
    location = text_only[-1].text
    try:
        status = section.find('div', class_='scr-inf_lt').text
    except:
        status = 'Not Available'
    result = {
        "Author" : "Prem",
        "Description" : description,
        "Location" : location,
        "Current" : current,
        "Status" : status,
        "Team A" : team_a,
        "Team A Score" : team_a_score,
        "Team B" : team_b,
        "Team B Score" : team_b_score,
        "Full Scoreboard" : link,
        "Thanks" : "NDTV Sports"
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)