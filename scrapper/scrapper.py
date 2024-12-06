from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


def get_today_movies(web_driver, page_url) -> list:
    web_driver.get(page_url)
    WebDriverWait(web_driver, 10)
    wait = WebDriverWait(web_driver, 10)
    movie_columns = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "col-12.col-md-6.col-lg-4.float-left")))
    movie_links = []

    for col in movie_columns:
        try:
            link = col.find_element(By.TAG_NAME, 'a').get_attribute("href")
            movie_links.append(link)
        except:
            print("Error fetching link for this column")
            continue

    return movie_links


def get_movie_info(web_driver, link):
    print(f"This is the movie's link {link}")

    mov = {
        'Title': "empty",
        "Director": "empty",
        "Link": link
    }
    return mov


if __name__ == '__main__':
    url = "https://www.cinetecanacional.net/sedes/cartelera.php?cinemaId=003&dia=2024-12-06#gsc.tab=0"

    driver = Firefox()
    try:
        links_list = get_today_movies(driver, url)
    except:
        driver.quit()
        print("Couldn't get today's movies. Finishing program")
        exit(1)

    print(links_list)
    movies = []
    for mov_link in links_list:
        movies.append(get_movie_info(driver, mov_link))

    print(movies)
    driver.quit()

    print("Goodbye!")
