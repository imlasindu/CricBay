from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)


@app.route('/')
def cricbay():
    html_text = requests.get('https://sports.ndtv.com/cricket/live-scores').text
    soup = BeautifulSoup(html_text, "html.parser")
    sect = soup.find_all('div',class_='sp-scr_wrp')
    section = sect[0]
    description = section.find('span',class_='description').text
    location = section.find('span',class_='location').text
    time = section.find('div',class_='scr_dt-red').text
    link = "https://sports.ndtv.com/" + section.find('a',class_='scr_ful-sbr-txt').get('href')
    toss = ''
    team1_name = ''
    team1_score = ''
    team2_name = ''
    team2_score = ''
    try:
        toss = section.find('div',class_="scr_dt-red @*scr-inf_tx*@").text
        block = section.find_all('div',class_='scr_tm-wrp')
        team1_block = block[0]
        team1_name = team1_block.find('div',class_='scr_tm-nm').text
        team1_score = team1_block.find('span',class_='scr_tm-run').text
        team2_block = block[1]
        team2_name = team2_block.find('div',class_='scr_tm-nm').text
        team2_score = team2_block.find('span',class_='scr_tm-run').text
    except:
        print("Some Error Found")
    result = {
        "Author" : "Prem",
        "Description" : description,
        "Location" : location,
        "Toss" : toss,
        "Status" : time,
        "Team A" : team1_name,
        "Team A Score" : team1_score,
        "Team B" : team2_name,
        "Team B Score" : team2_score,
        "Full Scoreboard" : link,
        "Thanks" : "NDTV Sports"
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)