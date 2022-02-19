import os, requests
from bs4 import BeautifulSoup

url = "https://www.cgccomics.com/certlookup/"
WRITE_PATH = os.path.join(os.getcwd(), "Images")
certificateNumbers = []

def addCertNumbers():
	while(True):
		try:
			numberofCertificate = int(input("\nHow many certificate numbers would you like to enter?: "))
			break
		except Exception as e:
			print('Wrong input. Please enter a number ...')

	for i in range(0, numberofCertificate):
		while(True):
			try:
				certNo = int(input("Enter certificate number {}: ".format(i+1)))
				if len(str(certNo)) == 10 :
					certificateNumbers.append(certNo)
					break
				else:
					print("Invalid certificate number!")

			except Exception as e:
				print('Invalid certificate number!')

def viewCertNumbers():
	for i in range(0, len(certificateNumbers)):
		print("Certificate number {}: {}".format(i+1, certificateNumbers[i]))

def scrape(certNo):
	try:
		page = requests.get("https://www.cgccomics.com/certlookup/" + str(certNo))
		soup = BeautifulSoup(page.content, 'html.parser')
		cardname = soup.find("dt", text="Card Name").findNext("dd").string
		cardset = soup.find("dt", text="Card Set").findNext("dd").string
		cardnumber = soup.find("dt", text="Card Number").findNext("dd").string

		filename = cardname + "_" + cardset + "_" + cardnumber
		filename = filename.replace(" ", "_")
		filename = filename.replace("/", "_")


		images = soup.find_all(class_='certlookup-images-item')

	except Exception as e:
		raise e

	i=0
	for item in images:
		#print(item.find('a').get('href'))
		if i == 0:
			facing = "front"
		else:
			facing = "back"

		try:
			r = requests.get(item.find('a').get('href'))
			with open(os.path.join(WRITE_PATH, filename + "_" + facing + ".jpg"), "wb") as f:
				f.write(r.content)
			i+=1
		except Exception as e:
			raise



def beginScraping():
	for i in certificateNumbers:
		scrape(i)


menu_options = {
	1: 'Add certificate numbers',
	2: 'View current list of certificate numbers',
	3: 'Begin Scraping',
	4: 'Exit',
}

def print_menu():
	print("\n")
	for key in menu_options.keys():
		print (key, '--', menu_options[key] )

def main():
	for i in range(0, 45):
		print("=", end="")
	print("\n\n\tWelcome to CGC Image Scraper!")
	print("")
	for i in range(0, 45):
		print("=", end="")


	while(True):
		print_menu()
		option = ''
		try:
			option = int(input('\nEnter your choice: '))
		except Exception as e:
			print('Wrong input. Please enter a number ...')
		if option == 1:
			addCertNumbers()
		elif option == 2:
			viewCertNumbers()
		elif option == 3:
			beginScraping()
		elif option == 4:
			print('Exiting...')
			clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
			clearConsole()
			exit()
		else:
			print('Invalid option. Please enter a number between 1 and 4.')

if __name__ == "__main__":
	clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
	clearConsole()
	if os.path.exists(WRITE_PATH) == False:
		os.mkdir(WRITE_PATH)
	main()