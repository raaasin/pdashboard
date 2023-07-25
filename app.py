import requests
import re
from bs4 import BeautifulSoup
from flask import Flask, render_template
import threading
import time

app = Flask(__name__)

def codechef():
    urll = 'https://www.codechef.com/users/raasin'
    # Your codechef function
    response = requests.get(urll)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rating_element = soup.find('div', class_='rating-number')
        if rating_element:
            rating = rating_element.get_text().strip()
            print("Rating:", rating)
        else:
            print("Rating information not found on the page.")
        fully_solved_element = soup.find('h5', text=re.compile(r'Fully Solved \(\d+\)'))
        if fully_solved_element:
            fully_solved = re.search(r'Fully Solved \((\d+)\)', fully_solved_element.text).group(1)
            print("Fully Solved:", fully_solved)
        else:
            print("Fully solved information not found on the page.")
        highest_rating_element = soup.find('small', text=re.compile(r'Highest Rating \d+'))
        if highest_rating_element:
            highest_rating = re.search(r'Highest Rating (\d+)', highest_rating_element.text).group(1)
            print("Highest Rating:", highest_rating)
        else:
            print("Highest rating information not found on the page.")

        with open('templates/codechef.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        current_rating_element = soup.find('g', transform='translate(247.5,48)')
        highest_rating_element = soup.find('g', transform='translate(412.5,48)')
        problems_solved = soup.find('g', transform='translate(82.5,48)')
        if current_rating_element and highest_rating_element and problems_solved:
            current_rating_text = current_rating_element.find('text')
            highest_rating_text = highest_rating_element.find('text')
            problems_solved_text = problems_solved.find('text')
            if current_rating_text and highest_rating_text and problems_solved_text:
                current_rating_text.string = rating
                highest_rating_text.string = highest_rating
                problems_solved_text.string = fully_solved

        with open('templates/codechef.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

    else:
        print("Failed to retrieve data from CodeChef.")

def gitupdate(totalcontrib, currentstreak, streakrange, longeststreak, longestrange):
    # Your gitupdate function
    url = 'https://camo.githubusercontent.com/988eae0cabe627f25d27443aedf176fbfd283b04a06fb6e3479de60e8239d40a/68747470733a2f2f6769746875622d726561646d652d73747265616b2d73746174732e6865726f6b756170702e636f6d2f3f757365723d7261616173696e267468656d653d746f6b796f6e6967687426686964655f626f726465723d74727565'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        total_contributions_element = soup.find('g', transform='translate(82.5,48)')
        current_streak = soup.find('g', transform='translate(247.5,48)')
        longest_streak_element = soup.find('g', transform='translate(412.5,48)')
        if current_streak and total_contributions_element and longest_streak_element:
            tc = total_contributions_element.find('text')
            cs = current_streak.find('text')
            lse = longest_streak_element.find('text')
            if tc and cs and lse:
                totalcontrib = tc.string
                currentstreak = cs.string
                longeststreak = lse.string

        else:
            print('Failed to retrieve data from GitHub.')

        with open('templates/github.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        totalcontrib_element = soup.find('g', transform='translate(82.5,48)')
        currentstreak_element = soup.find('g', transform='translate(247.5,48)')
        longeststreak_element = soup.find('g', transform='translate(412.5,48)')
        if totalcontrib_element and currentstreak_element and longeststreak_element:
            totalcontrib_text = totalcontrib_element.find('text')
            currentstreak_text = currentstreak_element.find('text')
            longeststreak_text = longeststreak_element.find('text')
            if totalcontrib_text and currentstreak_text and longeststreak_text:
                totalcontrib_text.string = totalcontrib
                currentstreak_text.string = currentstreak
                longeststreak_text.string = longeststreak

        with open('templates/github.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

    else:
        print("Failed to retrieve data from GitHub.")

def update_data():
    while True:
        codechef()
        gitupdate(totalcontrib=0, currentstreak=0, streakrange=0, longeststreak=0, longestrange=0)  # Provide actual values here
        time.sleep(20)

@app.route('/')
def dashboard():
    # Render your dashboard HTML here
    return render_template('index.html')

if __name__ == "__main__":
    # Start a background thread to update the data periodically
    background_thread = threading.Thread(target=update_data)
    background_thread.start()

    # Run the Flask app
    app.run()