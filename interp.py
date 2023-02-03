from bs4 import BeautifulSoup
import csv
import requests


def get_soup(links):
    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US'})
    url = requests.get(links, headers=HEADERS)
    soup1 = BeautifulSoup(url.text, 'lxml')
    return soup1

def get_productdesc(soup1):
    try:
        a=soup1.find("div", id="productDescription").get_text()
    except AttributeError:
        a='not available'
    return a

def get_productasin(soup1):
    a=''
    try:
        a=soup1.find("input", id="ASIN")["value"]
    except:
        pass
    return a

def get_productmanufacturer(soup1):
    try:
        a=soup1.find("a", id="bylineInfo").text
    except AttributeError:
        a='not available'
    return a


def get_prices(soup):

    try:
        price = soup.find_all('span', attrs={'class': "a-price-whole"})
    except AttributeError:
        price = None

    return price


def get_url(soup):
    try:
        urls = soup.find_all('a',attrs = {'class' : "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
    except AttributeError:
        urls = None

    return urls


def get_rating(soup):
    try:
        ratings = soup.find_all('span',attrs = {'class' : "a-icon-alt"})
    except AttributeError:
        ratings = None

    return ratings


def get_reviews(soup):
    try:
        reviews_no = soup.find_all('span', attrs={'class': "a-size-base s-underline-text"})
    except AttributeError:
        reviews_no = None

    return reviews_no


def get_link(soup):
    try:
        linky = soup.find('a', attrs={'class': "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"})
    except AttributeError:
        linky = None

    return linky


cnt = 0
fieldnames = ['name', 'url', 'price', 'rating','number of reviews','description','asin','manufacturer']
rowo=[]
rowi=[]
products=[]
link = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"



for j in range(20):
    soup = get_soup(link)
    try:
        nxt_page = get_link(soup).get("href")
    except AttributeError:
        pass

    prices = get_prices(soup)
    url_names = get_url(soup)
    ratings = get_rating(soup)
    reviews = get_reviews(soup)
    print("Page = ",j+1)
    for i in range(len(url_names)):
        cnt += 1
        rowi=[]
        try:
            print("Name:", url_names[i].text)
            rowi.append(url_names[i].text)
            print("url:", "https://www.amazon.in" + str(url_names[i]['href']))
            rowi.append("https://www.amazon.in" + str(url_names[i]['href']))
            #products.append("https://www.amazon.in" + str(url_names[i]['href']))
            soup1=get_soup("https://www.amazon.in" + str(url_names[i]['href']))

            print("price:", prices[i].text)
            rowi.append(prices[i].text)
            print("rating:", ratings[i].text)
            rowi.append(ratings[i].text)
            print("number of reviews:", (reviews[i].text)[1:-1])
            rowi.append((reviews[i].text)[1:-1])
            rowi.append(get_productdesc(soup1))
            rowi.append(get_productasin(soup1))
            rowi.append(get_productmanufacturer(soup1))
            rowo.append(rowi)
        except IndexError:
            print("Insufficient Data")
        print("\n------------------------------------------------------------\n")

    link = "https://www.amazon.in"+str(nxt_page)


print("total items",cnt)
with open('am1.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(fieldnames)

    # write multiple rows
    writer.writerows(rowo)