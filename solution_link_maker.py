from bs4 import BeautifulSoup
with open("temp.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    tt = soup.find("div", {"class": "relative flex w-full gap-4 px-5 py-3 transition-[background] duration-500"})
    solution_slug = tt.div.div.div.a['href']

    solution_page_link = f'https://leetcode.com{solution_slug}'

    print(solution_page_link)
    with open('out.html', 'w') as ff:
        ff.writelines(str(solution_page_link))