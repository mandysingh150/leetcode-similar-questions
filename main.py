# Author: Bishal Sarang
import json
import pickle
import time

import bs4
import colorama
import requests
from colorama import Back, Fore
# from ebooklib import epub
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils import *
import epub_writer

# Initialize Colorama
colorama.init(autoreset=True)

# Setup Selenium Webdriver
CHROMEDRIVER_PATH = r"./driver/chromedriver.exe"
options = Options()
# options.headless = False
# options.page_load_strategy = 'normal'
# options.add_argument("start-maximized")
# Disable Warning, Error and Info logs
# Show only fatal errors
options.add_argument("--log-level=3")
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)


# Get upto which problem it is already scraped from track.conf file
completed_upto = read_tracker("track.conf")

# Load chapters list that stores chapter info
# Store chapter info
with open('chapters.pickle', 'rb') as f:
    chapters = pickle.load(f)

def download(problem_num, url, title, solution_slug):
    print(Fore.BLACK + Back.CYAN + f"Fetching problem num " + Back.YELLOW + f" {problem_num} " + Back.CYAN + " with url " + Back.YELLOW + f" {url} ")
    n = len(title)

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
        # print(Fore.BLACK + Back.CYAN + 'PROBLEM/QUESTION = ' + Back.YELLOW + f'{problem_statement_examples_contraints}')
        print('\t==> problem description')

        # Construct HTML
        # title_decorator = '*' * n
        # problem_title_html = title_decorator + f'<div id="title">{title}</div>' + '\n' + title_decorator
        # problem_html = problem_title_html + str(soup.find("div", {"class": "_1l1MA"})) + '<br><br><hr><br>'



        ####################################################################
        # For obtaining the most voted solution link of the problem
        ####################################################################
        # time.sleep(0.5)
        url = url + '/solutions/?orderBy=most_votes'
        # import validators
        # valid=validators.url('https://www.codespeedy.com/')
        # print(f'valid = {valid}')
        driver.get(url)
        # print(f'-- before WebDriverWait --')
        # Wait 10 secs or until div with class 'transition-[background] duration-500' appears
        element = WebDriverWait(driver, 10).until(
            # EC.visibility_of_element_located((By.CLASS_NAME, "transition-[background]"))
            lambda x: x.find_element(By.XPATH, "//*[@class='relative flex w-full gap-4 px-5 py-3 transition-[background] duration-500']")
            # lambda x: x.find_element(By.CSS_SELECTOR, ".relative.flex.w-full.gap-4.px-5.py-3.transition-[background].duration-500")
            # EC.presence_of_element_located((By.CSS_SELECTOR, ".relative.flex.w-full.gap-4.px-5.py-3.transition-[background].duration-500"))
        )
        # .until(
        #     EC.visibility_of_element_located((By.CLASS_NAME, "relative flex w-full gap-4 px-5 py-3 transition-[background] duration-500"))
        #     # EC.visibility_of_element_located((By.CLASS_NAME, "relative flex w-full gap-4 px-5 py-3 transition-[background] duration-5ṇ00"))
        #     # EC.visibility_of_element_located((By.CLASS_NAME, "transition-[background] duration-500"))
        # )
        # print(Fore.BLACK + Back.CYAN + 'type of object = ' + Back.YELLOW + f'{type(element)}')
        # Get current tab page source
        html = driver.page_source
        # print(f'-- after WebDriverWait --')
        # with open('most_voted_sol.html', 'w') as ff:
        #     ff.writelines(str(driver.page_source))
        soup = bs4.BeautifulSoup(html, "html.parser")
        tt = soup.find("div", {"class": "relative flex w-full gap-4 px-5 py-3 transition-[background] duration-500"})
        solution_slug = tt.div.div.div.a['href']
        solution_page_link = f'https://leetcode.com{solution_slug}'
        print(f'\t==> solution_link = {solution_page_link}')
        # print(Fore.BLACK + Back.CYAN + 'solution_link = ' + Back.YELLOW + f'{solution_page_link}')
        # print('\t==> most voted solution')




        ####################################################################
        # For obtaining the content of the most voted solution of the problem
        ####################################################################
        # time.sleep(0.5)
        url = solution_page_link
        driver.get(url)
        # Wait 10 secs or until div with class '_16yfq _2YoR3' appears
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "._16yfq._2YoR3"))
            # EC.visibility_of_element_located((By.CLASS_NAME, "_16yfq _2YoR3"))
        )
        # Get current tab page source
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, "html.parser")
        tt = soup.find("div", {"class": "_16yfq _2YoR3"})
        txt1 = tt.get_text().splitlines()
        
        tt = soup.find("div", {"class": "mb-6 rounded-lg px-3 py-2.5 font-menlo text-sm bg-fill-3 dark:bg-dark-fill-3"})
        txt2 = tt.get_text().splitlines()

        # print(txt1)
        # print(txt2)

        solution_content = ''
        for text in txt1:
            if text in txt2 and text.lstrip().rstrip() != '':
                break
            solution_content += f'{text}\n'
        # print(f'content = {solution_content}')
        print('\t==> most voted solution content')


        # Append Contents to a HTML file
        # with open("out.html", "ab") as f:
        #     f.write(problem_html.encode(encoding="utf-8"))
        
        # create and append chapters to construct an epub
        # c = epub.EpubHtml(title=title, file_name=f'chap_{problem_num}.xhtml', lang='hr')
        # c.content = problem_html
        # chapters.append(c)

        # Write List of chapters to pickle file
        # dump_chapters_to_file(chapters)
        # # Update upto which the problem is downloaded
        # update_tracker('track.conf', problem_num)
        # print(Fore.BLACK + Back.GREEN + f"Writing problem num " + Back.YELLOW + f" {problem_num} ==>", end='  ')
        # print(Fore.BLACK + Back.GREEN + " SUCCESSFUL ")
        # print(f"Writing problem num {problem_num} with url {url} successfull")


        return problem_statement_examples_contraints, solution_page_link, solution_content

    except Exception as e:
        print(Back.RED + f" Failed Writing!!  {e} ")
        driver.quit()
        exit(0)
        return '', '', ''


    

def main():

    # Leetcode API URL to get json of problems on algorithms categories
    ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"

    # Problem URL is of format ALGORITHMS_BASE_URL + question__title_slug
    # If question__title_slug = "two-sum" then URL is https://leetcode.com/problems/two-sum
    ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"

    # Load JSON from API
    algorithms_problems_json = requests.get(ALGORITHMS_ENDPOINT_URL).content
    algorithms_problems_json = json.loads(algorithms_problems_json)

    # styles_str = "<style>pre{white-space:pre-wrap;background:#f7f9fa;padding:10px 15px;color:#263238;line-height:1.6;font-size:13px;border-radius:3px margin-top: 0;margin-bottom:1em;overflow:auto}b,strong{font-weight:bolder}#title{font-size:16px;color:#212121;font-weight:600;margin-bottom:10px}hr{height:10px;border:0;box-shadow:0 10px 10px -10px #8c8b8b inset}</style>"
    # with open("out.html", "ab") as f:
        # f.write(styles_str.encode(encoding="utf-8"))

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

    # Sort by difficulty follwed by problem id in ascending order
    links = sorted(links, key=lambda x: x[2])

    try: 
        for problem_num in range(completed_upto + 1, len(links)):
            question__title_slug, _ , frontend_question_id, question__title, question__article__slug = links[problem_num]
            url = ALGORITHMS_BASE_URL + question__title_slug
            title = f"{frontend_question_id}. {question__title}"

            # Download each file as html and write chapter to chapters.pickle
            problem_statement_examples_contraints, solution_page_link, solution_content = download(problem_num+1, url , title, question__article__slug)

            if problem_statement_examples_contraints != '':
                row_item = [frontend_question_id, question__title, problem_statement_examples_contraints, solution_page_link, solution_content]

                with open('data.csv', 'a') as fp:
                    print(Fore.BLACK + Back.CYAN + f"\tWriting problem num " + Back.YELLOW + f' {problem_num+1} ' + Back.CYAN  + "  ==>  ", end='')
                    
                    # fp.write(f'{frontend_question_id},{question__title},{problem_statement_examples_contraints},{solution_page_link},{solution_content}')
                    # for item in row_item:
                    #     item = '`'.join(item.split(','))
                    
                    row_item = ['`'.join(str(x).split(',')) for x in row_item]
                    # print(f'row_item = {row_item}')

                    fp.write(','.join(row_item))
                    
                    print(Fore.BLACK + Back.GREEN + " SUCCESSFUL ")

                    # Update upto which the problem is downloaded
                    # update_tracker('track.conf', problem_num)

            # Sleep for 20 secs for each problem and 2 minns after every 30 problems
            if (problem_num+1) % 30 == 0:
                print(f"Sleeping 120 secs\n")
                time.sleep(120)
            else:
                print(f"Sleeping 25 secs\n")
                time.sleep(25)

    finally:
        # Close the browser after download
        driver.quit()
    
    # try:
    #     epub_writer.write("Leetcode Questions.epub", "Leetcode Questions", "Anonymous", chapters)
    #     print(Back.GREEN + "All operations successful")
    # except Exception as e:
    #     print(Back.RED + f"Error making epub {e}")
    


if __name__ == "__main__":
    main()
