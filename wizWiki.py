from bs4 import BeautifulSoup
import requests

search = input()
r = requests.get("https://www.google.com/search?client=firefox-b-1-d&q=wizard101 central " + search)
soup = BeautifulSoup(r.text, 'html.parser')

#find first link
for i in soup.find_all('a'):
    if (i.get('href')[:4] == "/url"):
        rawLink = i.get('href')
        break

rawLink = rawLink[7:]
link = ""
for i in rawLink:
    if (i == "&"):
        break
    else:
        link += i
link = link.replace('%2527', '\'')
link = link.replace('%25', '%')
if ("http://www.wizard101central.com/wiki" not in rawLink):
    print("Not found")
else:
    #find page title
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = ((soup.find('title')).string).replace(" - Wizard101 Wiki", "")

    #find image
    content = requests.get(link).content
    soup = BeautifulSoup(content,'lxml')
    image_tags = soup.findAll('img')

    if ("Item:" in link):
        for i in image_tags:
            if "thumb" not in i.get('src').lower() and "icon" not in i.get('src').lower() and "http" not in i.get('src').lower():
                imageURL = "http://www.wizard101central.com" + (i.get('src'))
                break
    elif (image_tags[2].get('src') == "/wiki/images/thumb/d/d5/%28General%29_Doodle_Programmer.png/120px-%28General%29_Doodle_Programmer.png"):
        imageURL = "http://www.wizard101central.com" + (image_tags[3].get('src'))
    else:
        imageURL = "http://www.wizard101central.com" + (image_tags[2].get('src'))

    #find cheats if creature
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    if ("Creature:" in link):
        #get health
        rows = soup.find_all('tr')
        rows = [row for row in rows if 'Health' in str(row)]
        health = rows[0].text.replace("Health", "")
        #get cheats
        cheats = soup.findAll('tr', {"class": "data-table-green"})
        cheatList = []
        if cheats != []:
          for cheat in cheats:
              cheatList.append(cheat.text)
          cheatsText = ((cheatList[1][7:])[:1000] + '...')
          if len(cheatsText) > 997:
              cheatsText += '...'
          print(cheatsText)

    print(imageURL, health)
