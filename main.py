import re
import json
import time

import bs4
import colorama
import requests
from colorama import Back, Fore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils import *

# Initialize Colorama
colorama.init(autoreset=True)

# Setup Selenium Webdriver
CHROMEDRIVER_PATH = r"./driver/chromedriver.exe"
options = Options()
options.add_argument('--headless=True')
# options.add_argument("start-maximized")

# Disable Warning, Error and Info logs
# Show only fatal errors
options.add_argument("--log-level=3")
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)

# Get upto which problem it is already scraped from track.conf file
completed_upto = read_tracker("track.conf")

# if the first question of the session is to be processed, then we need to set the "Sort by" option to "Most Votes"
# first_question_to_be_processed = True


def download(problem_num, url, title, solution_slug):
    print(Fore.BLACK + Back.CYAN + f"Fetching problem num " + Back.YELLOW + f" {problem_num} " + Back.CYAN + " with url " + Back.YELLOW + f" {url} ")
    print('\t', end='')

    try:
        ####################################################################
        # For obtaining the problem description
        ####################################################################
        driver.get(url)
        # Wait 10 secs or until div with class '_1l1MA' appears
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "_1l1MA"))
        )
        # Get current tab page source
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, "html.parser")
        tt = soup.find("div", {"class": "_1l1MA"}).get_text().splitlines()
        problem_statement_examples_contraints = ''
        for val in tt:
            problem_statement_examples_contraints += f'{val.lstrip().rstrip()} '

        assert problem_statement_examples_contraints != ''
        print(Back.LIGHTMAGENTA_EX + '   ', end='')



        ####################################################################
        # For obtaining the most voted solution link of the problem
        ####################################################################
        url = url + '/solutions'
        driver.get(url)
        
        try:
            element = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, "//button[.='Votes']"))
            )

        except:
            # wait for "Sort by" button to be clickable and then click it
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.='Sort by']"))
            )
            element.click()
        
            # wait for "Most Votes" button to be clickable and then click it
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[.="Most Votes"]'))
            )
            element.click()
        
            time.sleep(4)
        
        # wait for all solutions to be ordered in descending order of votes
        time.sleep(0.8)
        element = WebDriverWait(driver, 10).until(
            lambda x: x.find_element(By.XPATH, "//*[@class='relative flex w-full gap-4 px-5 py-3 transition-[background] duration-500']")
        )

        html = driver.page_source
        soup = bs4.BeautifulSoup(html, "html.parser")
        tt = soup.find_all("div", {"class": "relative flex w-full gap-4 px-5 py-3 transition-[background] duration-500"})

        for index, i in enumerate(tt):
            try:
                solution_slug = i.div.div.div.a['href']
                solution_page_link = f'https://leetcode.com{solution_slug}'
                print(Back.BLUE + '   ', end='')
                


                ####################################################################
                # For obtaining the content of the most voted solution of the problem
                ####################################################################
                url = solution_page_link
                driver.get(url)
                
                # Wait 10 secs or until div with class '_16yfq _2YoR3' appears
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "._16yfq._2YoR3"))
                )
                
                # Get current tab page source
                html = driver.page_source
                soup = bs4.BeautifulSoup(html, "html.parser")
                tt2 = soup.find("div", {"class": "_16yfq _2YoR3"})
                txt1 = tt2.get_text()
                txt1 = (''.join([i if ord(i) < 128 else ' ' for i in txt1])).splitlines()
                
                tt2 = soup.find_all("div", {"class": "mb-6 rounded-lg px-3 py-2.5 font-menlo text-sm bg-fill-3 dark:bg-dark-fill-3"})
                txt2 = []
                for element in tt2:
                    e1 = element.get_text()
                    e1 = (''.join([i if ord(i) < 128 else ' ' for i in e1])).splitlines()
                    txt2 = txt2 + e1

                solution_content = ''
                for text in txt1:
                    if text.lstrip().rstrip() == '' or (text in txt2 and text.lstrip().rstrip() != ''):
                        continue
                    solution_content += f'{text}~~'

                if (re.match(r'.*\svideo\s.*', solution_content)) or re.match(r'.*\svideo[^a-zA-Z0-9].*', solution_content):
                    author_id = soup.find("a", {"class": "no-underline text-label-2 dark:text-dark-label-2 text-xs overflow-hidden max-w-[100px] md:max-w-[200px] font-normal hover:text-blue-s dark:hover:text-dark-blue-s truncate"}).get_text()
                    raise Exception(f'{author_id} {solution_page_link}')
                
                if solution_content == '':
                    raise Exception(f'{solution_page_link} ==> content is empty')

                print(Fore.BLACK + Back.WHITE + f' {index+1} ', end='')

                return problem_statement_examples_contraints, solution_page_link, solution_content

            except Exception as ee:
                print(Back.RED + ' ^ ', end='')
                # print(Back.RED + f" Failed!!, Error =  {ee} ")
                continue


        print(Back.RED + f'\t==> cannot find any valid solution among first 15 solutions')
        return '', '', ''

    except Exception as e:
        # print(Back.RED + f" Failed Writing!!, Error = {e} ")
        print(Back.RED + ' X ')
        driver.quit()
        exit(0)


    
def main():
    # Leetcode API URL to get json of problems on algorithms categories
    ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"

    # Problem URL is of format ALGORITHMS_BASE_URL + question__title_slug
    # If question__title_slug = "two-sum" then URL is https://leetcode.com/problems/two-sum
    ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"

    # Load JSON from API
    algorithms_problems_json = requests.get(ALGORITHMS_ENDPOINT_URL).content
    algorithms_problems_json = json.loads(algorithms_problems_json)

    # List to store question_title_slug
    links = []
    for child in algorithms_problems_json["stat_status_pairs"]:
        # Only process free problems
        if not child["paid_only"]:
            question__title_slug = child["stat"]["question__title_slug"]
            question__article__slug = child["stat"]["question__article__slug"]
            question__title = child["stat"]["question__title"]
            frontend_question_id = child["stat"]["frontend_question_id"]
            difficulty = child["difficulty"]["level"]
            links.append((question__title_slug, difficulty, frontend_question_id, question__title, question__article__slug))

    # Sort by difficulty followed by problem id in ascending order
    links = sorted(links, key=lambda x: x[2])

    try: 
        for problem_num in range(completed_upto + 1, len(links)):
            question__title_slug, _ , frontend_question_id, question__title, question__article__slug = links[problem_num]
            url = ALGORITHMS_BASE_URL + question__title_slug
            title = f"{frontend_question_id}. {question__title}"

            # Download each file as html and write chapter to chapters.pickle
            problem_statement_examples_contraints, solution_page_link, solution_content = download(frontend_question_id, url , title, question__article__slug)

            if problem_statement_examples_contraints != '':
                row_item = [frontend_question_id, question__title, problem_statement_examples_contraints, solution_page_link, solution_content]

                with open('data.csv', 'a') as fp:
                    print(Fore.BLACK + Back.CYAN + "  ==>  ", end='')
                    
                    row_item = ['`'.join(''.join([i if ord(i) < 128 else ' ' for i in str(x)]).replace('\n', ' ').split(',')) for x in row_item]

                    fp.write(','.join(row_item) + '\n')
                    
                    print(Fore.BLACK + Back.GREEN + " SUCCESSFUL ")
                    print()

                    # Update upto which the problem is downloaded
                    update_tracker('track.conf', problem_num)

        print(Back.LIGHTYELLOW_EX + '\tDOWNLOAD COMPLETED\t')

    except Exception as e:
        # print(Back.RED + f" Failed in main!!, Error = {e} ")
        print(Back.RED + f" X ")
        

    finally:        
        # Close the browser after download
        driver.quit()
    
    


if __name__ == "__main__":
    main()