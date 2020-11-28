import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

class DiscoursScraper():
  
  def __init__(self):
    self.driver = webdriver.Chrome(ChromeDriverManager().install())
    self.main_page_url = 'https://www.vie-publique.fr/discours'

  def scrap_pages_urls(self):
    self.driver.get(self.main_page_url)
    sleep(5) # wait until all elements have loaded
    pages_urls = self.driver.find_elements_by_css_selector("li.pager__item > a")
    pages_urls = [page.get_attribute('href') for page in pages_urls]
    return pages_urls
    
  def scrap_speeches_urls(self, page_url):
    self.driver.get(page_url)
    sleep(5) # wait until all elements have loaded
    articles = self.driver.find_elements_by_css_selector("h2.teaserSimple--title > a")
    articles = [article.get_attribute('href') for article in articles]
    return articles

  def record_speeches_of_page(self, writer, speeches_urls):
    for speech_url in speeches_urls:
      self.driver.get(speech_url)
      sleep(5) # wait until all elements have loaded
      discours = self.driver.find_elements_by_css_selector("p")
      discoursText = ""
      for d in discours[4:19] :
        discoursText += self.remove_line_breaks(d)
        # discours title
      title = self.driver.find_element_by_css_selector("h1")
      # append row on csv file
      writer.writerow({'titre': title.text, 'date': discours[0].text, 'date_publication': discours[1].text, 'intervenants': discours[2].text, 'mots_cles': discours[3].text, 'discours': discoursText})   
    
  def remove_line_breaks(self, element):
    element = element.text.replace('\n', ' ').replace('\r', '') # remove line breaks in text
    return str(element)

  def main(self):
    # create csv
    with open('discours.csv', 'w', encoding='utf-8', newline='') as csvfile:
      fieldnames = ['titre', 'date', 'date_publication', 'intervenants', 'mots_cles', 'discours']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      # scrap first page
      speeches_urls_first_page = self.scrap_speeches_urls(self.main_page_url)
      self.record_speeches_of_page(writer, speeches_urls_first_page)      
      # get speeches urls for each next page
      pages_urls = self.scrap_pages_urls()
      for page in pages_urls:
        speeches_urls = self.scrap_speeches_urls(page)
        # scrap speech text
        self.record_speeches_of_page(writer, speeches_urls)

    # end webdriver session    
    self.driver.quit()
       
if __name__ == "__main__":
    DiscoursScraper().main()  
  

  
