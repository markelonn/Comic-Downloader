import sys
import urllib.request as urllib
import re
import os

def month_comic_downloader(year,month,price):
	steps = int(len(price)/10)
	base_url_comic = 'http://explosm.net/comics/'
	dn = os.path.dirname(os.path.realpath(__file__))
	i = 0
	year = str(year)
	month = str(month)
	newfolder = year + '/' + month
	if not os.path.exists(newfolder):
		os.makedirs(newfolder)
	dnf = dn + '/' + newfolder
	while i < len(price):
		os.chdir(dnf)
		find_url = 'http://explosm.net/comics/' + price[i]
		base_img_url = 'http://files.explosm.net/comics/'
		hfile = urllib.urlopen(find_url)
		htext = hfile.read().decode()
		reg = '<img id="main-comic" src="//files.explosm.net/comics/(.+?\.[png]*[gif]*[jpg]*)"/>'
		patt = re.compile(reg)
		url_extender = re.findall(patt,htext)
		if not url_extender:
			i = i + 1
			continue
		final_url = base_img_url + str(url_extender)
		final_url = final_url.replace("['","")
		final_url = final_url.replace("']","")
		if " " in final_url:
			final_url = final_url.replace(" ","%20")
		ext_checker = final_url[-3:]
		filename = len(price) - i
		if 'gif' in ext_checker:
			ffilename = str(filename) + '.gif'
		elif 'jpg' in ext_checker:
			ffilename = str(filename) + '.jpg'
		else:
			ffilename = str(filename) + '.png'
		#print(final_url)
		urllib.urlretrieve(final_url,ffilename)
		if i%steps == 0:
			print('.',end='')
			sys.stdout.flush()
		i = i + 1
	print('] Done!')

year = input("Enter the year : ")
month = input("Enter the month : ")
base_url = 'http://explosm.net/comics/archive/'
required_url = base_url + str(year) + '/' + str(month)
htmlfile = urllib.urlopen(required_url)
htmltext = htmlfile.read().decode()
regex = 'data-id="([0-9]+)"'
pattern = re.compile(regex)
price = re.findall(pattern,htmltext)
width = 12
spaces = ' ' * (width)
backspace = '\b' * (width+1)
print('Starting [{}]{}'.format(spaces, backspace), end='')
sys.stdout.flush()
month_comic_downloader(year,month,price)