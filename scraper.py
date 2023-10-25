"""
Amazon Web Scraper
"""
from bs4 import BeautifulSoup
import requests

class WebScraper:
    def __init__(self):
        self.products={"Title":[], "Price":[], "Ratings":[], "Reviews":[], "Availability":[], "Link":[], "Icon":[]}

    def getPrice(self,soup) -> str:
        try:
            price=soup.find("span", attrs={"class":'a-price'}).find("span", attrs={'class': 'a-offscreen'}).text
        except AttributeError:
            price=""
        return price

    def getTitle(self,soup) -> str:
        try:
            title=soup.find("span", attrs={'id':'productTitle'}).text.strip()
        except AttributeError:
            title=""
        return title

    def getIcon(self,soup, title) -> str:
        try:
            img=soup.find("div", attrs={'id':'main-image-container'}).find("img", attrs={"alt":title})['data-a-dynamic-image']
        except AttributeError:
            img="No Image Available"
        return img

    def getReviews(self,soup) -> str:
        try:
            box=soup.find('div', attrs={'id':"averageCustomerReviews"})
            reviews=box.find('span', attrs={'id':'acrCustomerReviewText'}).text.strip()
            rating=box.find('span', attrs={'class':'a-size-base a-color-base'}).text.strip()
            for i in range(len(reviews)):
                if reviews[i]==" ": 
                    reviews=reviews[:i]
                    break
        except AttributeError:
            reviews="0"
            rating="No Rating"
        return [rating,reviews]

    def getAvailability(self,soup) -> str:
        try:
            available = soup.find("div", attrs={'id':'availability'})
            available = available.find("span").string.strip()

        except AttributeError:
            available = "Out of Stock"	

        return available

    def interpretInput(self,input) -> str:
        res="s?k="
        for i in range(len(input)):
            if input[i]==" ": res+="+"
            else: res+=input[i]
        return res

    def getResults(self,links):
        # Get all the links from search page
        product_list=[]
        for i in range(len(links)):
            link="https://amazon.com" + links[i].get('href')
            product_list.append(link)

        # Fill in the table
        for i,link in enumerate(product_list):
            HEADERS=({'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36', 'Accept-Language' : 'en-US, en;q=0.5'})
            new_page=requests.get(link,headers=HEADERS)
            new_soup=BeautifulSoup(new_page.content, "html.parser")
            title=self.getTitle(new_soup)
            self.products["Title"].append(title)
            self.products["Price"].append(self.getPrice(new_soup))
            review=self.getReviews(new_soup)
            self.products["Reviews"].append(review[1])
            self.products["Ratings"].append(review[0])
            self.products["Link"].append(link)
            self.products["Availability"].append(self.getAvailability(new_soup))
            # print(f'{i}: product:{self.products["Title"][i]} --- price:{self.products["Price"][i]} --- rating:{self.products["Ratings"][i]} --- reviews:{self.products["Reviews"][i]} --- link:{self.products["Link"][i]} --- Availability:{self.products["Availability"][i]} \n')
            if i>1: break

    def printResults(self):
        print(self.products)

if __name__=="__main__":
    w=WebScraper()
    input=input('What are you searching for?\n')
    search=w.interpretInput(input)
    HEADERS=({'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36', 'Accept-Language' : 'en-US, en;q=0.5'})
    # URL = "https://www.amazon.com/s?k=playstation+4&crid=1CJB1CIZGBKBN&sprefix=playstation+%2Caps%2C159&ref=nb_sb_noss_2"
    URL = "https://www.amazon.com/"+search
    page = requests.get(URL,headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")
    links=soup.find_all("a", attrs={'class' : 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    res=w.getResults(links)
    # app.run(host="0.0.0.0",port=80)   