import re
import time
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from bs4 import Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def outcome(result: str) -> float:
    """Compares two numbers in a result string separated by a hyphen.

    The function returns:
    - 1 if the number before the hyphen is greater than the number after the hyphen.
    - 0 if the number before the hyphen is less than the number after the hyphen.
    - 0.5 if the numbers are equal.

    Args:
        result: The result from the match in the format "X-Y".

    Returns:
        1, 0, or 0.5 based on the comparison.

    Raises:
        ValueError: If the result string is not in the expected format.
    """
    try:
        # Extract the numbers before and after the hyphen
        home_score, away_score = map(int, result.split("-"))
        if home_score > away_score:
            return 1.0
        elif home_score < away_score:
            return 0.0
        else:
            return 0.5
    except ValueError as e:
        # Handle invalid formats that cannot be split or converted to integers
        raise ValueError(
            "Result string must be in the format 'X-Y' where X and Y are integers."
        ) from e


def scrape_nifs_all(url: str) -> pd.DataFrame:
    """Scrapes fotball match data from a given NIFS URL and returns it as DataFrame.

    The function uses Selenium with a headless Chrome browser to load and render
    JavaScript-heavy webpages. It retrieves the page source after rendering, parses
    the HTML using BeautifulSoup, and extracts relevant match details, such as date,
    round, home and away teams, and the result. It then organizes the data into a
    Pandas DataFrame.

    Args:
        url: The URL of the NIFS webpage containing match data.

    Returns:
        A DataFrame containing the extracted match data with the following columns:
            - 'Date' (str): Match date in the format found on the website.
            - 'Round' (str): Match round extracted from the page.
            - 'HomeTeam' (str): Name of the home team.
            - 'AwayTeam' (str): Name of the away team.
            - 'Result' (str): Match result, typically in the form 'X-Y' or similar.
            - 'Outcome' (str): Derived column indicating the outcome of the match.
    """
    # 1) Set up Selenium with headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # If ChromeDriver is not in your PATH, specify the full path:
    # driver = webdriver.Chrome(executable_path="C:/path/to/chromedriver.exe", options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)

    # 2) Load the page and wait for JS to render
    driver.get(url)
    time.sleep(5)  # adjust if needed

    # 3) Grab the rendered HTML and quit the browser
    html = driver.page_source
    driver.quit()

    # 4) Parse with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find all the "en_kamp" divs, each representing one match row
    match_rows = soup.find_all("div", class_="en_kamp")

    data = []
    for row in match_rows:
        if isinstance(row, Tag):
            # Extract date from <div class="tid"> (often in an <a> tag)
            date_div = row.find("div", class_="tid")
            date_text = ""
            round_text = ""
            result_text = ""
            if date_div:
                date_link = date_div.find("a") if isinstance(date_div, Tag) else None
                date_text = date_link.get_text(strip=True) if date_link else ""

                if match := re.search(r"Runde\s+(\d+)", date_div.get_text(strip=True)):
                    round_text = match[1]

            # Extract the two teams from <div class="kamp"> elements
            # Typically one for home, one for away, in the same "en_kamp" block
            teams = row.find_all("div", class_="kamp")
            text = teams[0].get_text(strip=True)
            # 2) Replace any sequence of one or more whitespace characters (spaces, newlines, etc.) with a single space
            text = re.sub(r"\s+", " ", text)

            # 3) Split on the dash, allowing for optional spaces around it
            home_team, away_team = [part.strip() for part in re.split(r"\s*-\s*", text)]

            result_div = row.find("div", class_="res")
            if result_div:
                result_text = result_div.get_text(strip=True).split("(")[0]

            data.append(
                {
                    "Date": date_text,
                    "Round": round_text,
                    "HomeTeam": home_team,
                    "AwayTeam": away_team,
                    "Result": result_text,
                }
            )

    df_result = pd.DataFrame(data)
    df_result["Outcome"] = df_result["Result"].apply(outcome)
    return df_result


if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent.parent / "data"
    # Results from Norway soccer league, level 2, 2024
    url = "https://www.nifs.no/kamper.php?countryId=1&tournamentId=6&stageId=694962"
    df = scrape_nifs_all(url)
    df.to_csv(data_dir / "soccer_norway_level2_2024.csv", index=False)
