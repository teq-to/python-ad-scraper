import requests
import bs4
import json
import sys
import time

from bs4 import BeautifulSoup as soup

#current page
page = 1

#create ads array
phones_numbers = []

#programme continue (ask from user )
pro_continue = True

#pagination is end
pagi_end = False

#host_url
host_url = ""

#headers
headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}


#get ads from ikman.lk
def get_ads(page):

	global phones_numbers

	#ads_url
	ads_url = host_url+"/en/ads/sri-lanka/vehicles?page="+str(page)

	#open a connection to url
	r = requests.get(ads_url, headers=headers)
	page = r.content
	print('All Ads: '+str(r.status_code))

	if(r.status_code == 200):

		#parse the html though BeautifulSoup
		page_soup = soup(page, "html.parser")

		#get ad_rows from the html
		ad_rows = page_soup.findAll('div', {"class" : "ui-item"})

		#loop ads
		loop_ads(ad_rows)

		#save to the file
		save_file(phones_numbers)

		#reset phone_numbers list
		phones_numbers = []

		#-----------------------------------------------------------------------
		# Ads Pagination
		#-----------------------------------------------------------------------

		#get pagination next url from html
		pagination_next_url = page_soup.findAll('a', {"class" : "pag-next"})[0]['href']

		#check if pagination url response 200
		r2 = requests.get(host_url+pagination_next_url, headers=headers)

		if(r2.status_code == 200):
			set_pagination(True)

#End ged_ads func


#loop ads
def loop_ads(ad_rows):
	index = 0
	for row in ad_rows:

		print('Getting Ad : '+ str(index))
		#single ad url
		single_ad_url = row.findAll('a', {'class': 'item-title'})[0]['href']

		time.sleep(10)

		#get single add from ad page
		get_single_ad(single_ad_url)

		index += 1
#End loop_ads func

#get single ad
def get_single_ad(ad_url):

	ad_url = host_url+ad_url

	#open a connection to url
	r = requests.get(ad_url, headers=headers)
	page = r.content
	print('Single Ad: '+str(r.status_code))

	if(r.status_code == 200):
		#parse the html though BeautifulSoup
		page_soup = soup(page, "html.parser")

		#get ad phone numbers
		phone_html = page_soup.findAll("div", {"class": "item-contact-more"})

		#loop phone numbers
		for phone in phone_html:
			phone = phone.findAll('span')[0].text
			if(phone.isdigit()):
				phones_numbers.append(phone)

#End ged_single_ad func


#set pagination
def set_pagination(val):
	global pagi_end
	pagi_end = val

#End set pagination func

#get pagination
def get_pagination():
	return pagi_end;

#End get pagination func

#print func
def my_print(data):
	print(json.dumps(data, indent=4, sort_keys=True))

#End my print func

#save in the file
def save_file(phone_numbers):
	ts = time.time()
	f = open(str(ts)+'.json', 'w')
	json.dump(phone_numbers, f)
	f.close()

#-----------------------------------------------------------------------
# Mail Loop
#-----------------------------------------------------------------------

while pro_continue == True:
	#get all ads by page
	get_ads(page)

	print('All ads gratherd from page : '+str(page))

	if (get_pagination() == True):
		next_page = page + 1
		#change page number to next page
		page = next_page
		pro_continue = True
		
	else :
		print('There is nothing to gatherd, programe will automatically closed, and saving the file')
		pro_continue = False
