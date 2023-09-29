import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    source = requests.get("https://www.imdb.com/chart/top/", headers=headers)
    source.raise_for_status()
    soup = BeautifulSoup(source.text, "html.parser")

    movies = soup.find("ul", class_="ipc-metadata-list").find_all("li")

    data = []

    for movie in movies:
        _rank_and_name = movie.find("div", class_="ipc-title").a.text
        rank = _rank_and_name.split(".")[0]
        name = _rank_and_name.split(".")[1]
        year = (
            movie.find("div", class_="sc-4dcdad14-7")
            .find("span", class_="sc-4dcdad14-8")
            .text
        )
        rating = re.search(
            r"\d+\.\d+",
            movie.find("span", class_="sc-4dcdad14-1")
            .find("span", class_="ipc-rating-star")
            .text,
        ).group()

        data.append([rank, name, year, rating])
        
    # Create a DataFrame
    df = pd.DataFrame(data, columns=["Rank", "Name", "Year", "Rating"])
    
    # Save the DataFrame to an Excel file
    df.to_excel("movie_data.xlsx", index=False)
    print("Successfully written into excel file!")

except Exception as e:
    print(e)
