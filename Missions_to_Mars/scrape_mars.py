# Declare Dependencies 
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

#turn jupyter notebook to a function to  get the data
def scrape_all():

	executable_path = {'executable_path': ChromeDriverManager().install()}
	browser = Browser('chrome', **executable_path, headless=True)


	#Mars News(it's how we can tell the scrape button works beceause it changes)
	url = "https://redplanetscience.com/"
	browser.visit(url)
	html = browser.html
	soup = bs(html, "html.parser")

	news_article = soup.find_all("div", class_="content_title")[0]
	news_article_title = news_article.text
	news_article_title

	teaser = soup.find_all("div", class_="article_teaser_body")[0]
	article_teaser = teaser.text
	print(article_teaser)

	#featured image relatively straight foward, but add a / to make the image url work
	url = 'https://spaceimages-mars.com'
	browser.visit(url)
	html = browser.html
	soup = bs(html, "html.parser")

	images = soup.find('img', class_="headerimage fade-in")
	feature_pic = (images['src'])
	feature_pic_link = url +"/"+ feature_pic
	print(feature_pic_link)


	#mars and earth table, panda use, just break it down and reconstruct it to a html table
	url = 'https://galaxyfacts-mars.com/'

	tables = pd.read_html(url)

	df = tables[0]
	earth = df[2]
	mars = df[1]
	descriptors = df[0]

	table_df = pd.DataFrame({"Description": descriptors, "Mars": mars, "Earth": earth})
	table_df.set_index('Description', inplace=True)
	## generate html table from the dataframe

	html_table = table_df.to_html(index=False, classes="table", header=False)


	# clean up the table by stripping unwanted n's
	html_table = html_table.replace('\n', '')


	#each hemishpere of mars, four loop, but just try to get to the image first and then construct
	url = "https://marshemispheres.com/"
	browser.visit(url)
	html = browser.html
	soup = bs(html, "html.parser")
	hemisphere_image_url = []

	for i in range(4):

			hemisphere_dict = {}

			browser.find_by_css("a.product-item h3")[i].click()
			hemisphere_dict["title"] = browser.find_by_css("h2.title").text

			html = browser.html
			soup = bs(html, "html.parser")

			sample_text = browser.links.find_by_partial_text("Sample")
			hemisphere_dict["img_url"] = sample_text["href"]

			hemisphere_image_url.append(hemisphere_dict)
			browser.back()


	print(hemisphere_image_url)
	#pe polite and if you don't just a lot of left over windows
	browser.quit()
	#collect all the info together for the website
	mars_information={ 
			"Latest_news_Title": news_article_title,
			"Latest_news_content": article_teaser,
			"Featured_Mars_Image": feature_pic_link,
			"Information_about_Mars" : html_table,
			"High_Res_images_of_Mars_hemispheres" : hemisphere_image_url
	}

	return  mars_information
