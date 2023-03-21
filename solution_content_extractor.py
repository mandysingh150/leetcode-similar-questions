from bs4 import BeautifulSoup
with open("temp.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    tt = soup.find("div", {"class": "_16yfq _2YoR3"})
    txt1 = tt.get_text().splitlines()
    
    tt = soup.find("div", {"class": "mb-6 rounded-lg px-3 py-2.5 font-menlo text-sm bg-fill-3 dark:bg-dark-fill-3"})
    txt2 = tt.get_text().splitlines()

    print(txt1)
    print(txt2)

    t2 = ''
    for text in txt1:
        if text in txt2 and text.lstrip().rstrip() != '':
            break
        t2 += f'{text}\n'

    print(t2)
    with open('out.html', 'w') as ff:
        ff.writelines(t2)