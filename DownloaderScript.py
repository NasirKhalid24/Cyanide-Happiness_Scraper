import webbrowser, bs4, requests, os, sys

url = "http://explosm.net/comics/latest/"
# url = "http://explosm.net/comics/latest"
os.makedirs('All_Comics', exist_ok=True)
os.makedirs('Random_Comics', exist_ok=True)

count = input("How many random comics? (0 for all comics): ")
while count.isnumeric() == False:
	print("Invalid input \n")
	count = input("How many random comics? (negative number for all): ")
count = int(count)
if count == 0: count -= 1
else: count+= 1
start = False
while True:
	req = requests.get(url)
	# print("Downloading comic on page: " + url)
	try:
		req.raise_for_status()
	except Exception as exc:
		print('There was a problem: %s' % (exc))

	soup = bs4.BeautifulSoup(req.text, 'html.parser')
	url_comic = "http:" + soup.find(id="main-comic").get("src")
	
	end_name = os.path.basename(url_comic).split('?')[0]
	
	if count>0:
		if start:
			print("Downloaded: " + str(end_name))
			img = open(os.path.join('Random_Comics', end_name), 'wb')
			for amount in requests.get(url_comic).iter_content(1000000):
				img.write(amount)
			img.close()
		url_next = soup.find(class_="nav-random").get("href")
		count -= 1
		start = True
	else:
		print("Downloaded: " + str(end_name))
		img = open(os.path.join('All_Comics', end_name), 'wb')
		for amount in requests.get(url_comic).iter_content(1000000):
			img.write(amount)
		img.close()
		url_next = soup.find(class_="nav-previous").get("href")
	if url_next == None or count==0:
		sys.exit()
	url = "http://explosm.net" + url_next