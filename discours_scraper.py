import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

class DiscoursScraper():
  
  def __init__(self):
    self.driver = webdriver.Chrome(ChromeDriverManager().install())
    self.main_page_url = 'https://www.vie-publique.fr/discours'
    self.child_page_url = 'https://www.vie-publique.fr/discours?page='
    self.pages_begin = 1;
    self.pages_end = 100;
    
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
      discours = self.driver.find_elements_by_css_selector("div.discour--desc > span > p")
      discoursText = ""
      for d in discours:
        discoursText += self.remove_line_breaks(d)
      # discours title  
      title = self.driver.find_element_by_css_selector("h1")
      # discours date
      date_discours = self.driver.find_element_by_css_selector("time")
      # append row on csv file
      writer.writerow({'titre': title.text, 'date': date_discours.text, 'discours': discoursText})   
    
  def remove_line_breaks(self, element):
    element = element.text.replace('\n', ' ').replace('\r', '') # remove line breaks in text
    return str(element)

  def main(self):
    # create csv
    with open('discours_2020_3.csv', 'a', encoding='utf-8', newline='') as csvfile:
      fieldnames = ['titre', 'date', 'discours']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      # scrap first page
      speeches_urls_first_page = self.scrap_speeches_urls(self.main_page_url)
      self.record_speeches_of_page(writer, speeches_urls_first_page)      
      # get speeches urls for each next page until reach pages_total
      for i in range(self.pages_begin, self.pages_end):
        speeches_urls = self.scrap_speeches_urls(self.child_page_url+str(i))
        # scrap speech text
        self.record_speeches_of_page(writer, speeches_urls)

    # end webdriver session    
    self.driver.quit()
       
if __name__ == "__main__":
    DiscoursScraper().main()  
  

  
