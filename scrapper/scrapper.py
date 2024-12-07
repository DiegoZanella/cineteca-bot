from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Movie import Movie


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
    web_driver.get(link)
    film_id = link.split('?')[1].split('&')[0].split('=')[1]

    # To get the img link
    img_element = (web_driver.find_element(By.CLASS_NAME, "col-12.col-md-4.float-left")
                   .find_element(By.CLASS_NAME, "img-fluid"))
    img_link = img_element.get_attribute("src")

    # To get the movie info
    info_element = web_driver.find_element(By.CLASS_NAME, "col-12.col-md-5.float-left")
    header_element = info_element.find_elements(By.CLASS_NAME, "lh-1.small")
    header_items = header_element[0].text.strip('()').split(',')
    title = header_items[0]
    # print(f"Header items: {header_items}")
    # print(f"Title: {title}")
    duration_item = header_items[-1].split(':')
    duration = duration_item[1].strip()

    # to get director
#    director = header_element[1].text.split(':')[1].strip()
    director_element = header_element[1]
    director_inner_html = director_element.get_attribute("innerHTML")
    director = director_inner_html.split("&nbsp")[1].strip().strip(";")

    # to get description
    description = info_element.find_element(By.CLASS_NAME, "lh-1.text-justify.small").text

    # to get timetables
    times_element = web_driver.find_element(By.CLASS_NAME, "col-12.col-md-3.float-left")
    days_elements = times_element.find_elements(By.TAG_NAME, 'span')
    days = [element.text for element in days_elements]
    times_links = times_element.find_elements(By.TAG_NAME, 'a')
    times = [element.text for element in times_links]
    time_tables = [x for x in zip(days, times)]

    movie = Movie(
        film_id=film_id,
        title=title,
        duration=duration,
        director=director,
        description=description,
        times=time_tables,
        img_link=img_link
    )

    return movie


def start_scrapper(date):
    url = f"https://www.cinetecanacional.net/sedes/cartelera.php?cinemaId=003&dia={date}#gsc.tab=0"

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

    driver.quit()

    return movies


if __name__ == '__main__':
    scrapper_output = start_scrapper("2021-07-20")
    for mov in scrapper_output:
        print(mov)
        print("-------------------------------")

    print("Goodbye!")
