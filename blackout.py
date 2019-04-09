import os, sys, json

versionString = "blackout 1.2 RC1"

# load database
try:
	with open("database.json") as jsonfile:
		database = json.load(jsonfile)
except:
	print(" [-] Couldn't load database. Building a new one.")
	database = {}
	database["wordlist"] = []
	database["accounts"] = {}

print(versionString)

while True:
	# get input
	command = input("> ")
	
	# seperate args and the command
	args = command.split(" ")[1:]
	command = command.split(" ")[0]
	
	# clear screen
	if(command == "cls" or command == "clear"):
		os.system("clear")
	
	# save db to file
	if(command == "save" or command == "dump"):
		try:
			with open('database.json', 'w') as fp:
				json.dump(database, fp) 
			print(" [+] Saved successfully!")
				 
		except OSError:
			print(" [-] Error! Permissions probably bad. (OSError)")
			
		except:
			print(" [-] Unknown error!")
	
	if(command == "generate"):
		try:
			if(args[0] == "wordlist"):
				# get all passwords
				words = []
				for service in database["accounts"]:
					for account in database["accounts"][service]:
						words.append(database["accounts"][service][account])
				for password in database["wordlist"]:
					words.append(password)
				
				# export in chunks of 1000
				# this speeds up the process a lot
				i = 0
				export = ""
				for word in words:
					if(i < 1001):
						export = export + "\n"
						i += 1
						export = export + word
					else:
						with open("wordlist.txt", "w") as f:
							f.write(export)
						export = ""
						i = 0
				with open("wordlist.txt", "w") as f:
					f.write(export)
				print(" [+] Successfully generated a wordlist! Check wordlist.txt")
		except:
			print(" [-] Unknown error.")
						
	
	# search database for account
	if(command == "lookup"):
		try:
			for service in database["accounts"]:
				for account in database["accounts"][service]:
					if(args[0] in account):
						print("Found account! (service: " + service + ") Login: " + account + ":" + database["accounts"][service][account])
		except:
			print(" [*] Usage:")
			print("     lookup (username/email)")
	
	if(command == "list"): # self-explanitory
		try:
			if(args[0] == "accounts"):
				for service in database["accounts"]:
					for account in database["accounts"][service]:
						print(account)
			elif(args[0] == "services"):
				for service in database["accounts"]:
					print(service)
			elif(args[0] == "passwords"):
				for service in database["accounts"]:
					for account in database["accounts"][service]:
						print(database["accounts"][service][account])
				for password in database["wordlist"]:
					print(password)
			else:
				args[0] = args[0] / 0
		except:
			print(" [*] Usage:")
			print("     List accounts/services/passwords")
	
	if(command == "load" or command == "import"): # import file
		try:
			filename = args[0]
			filetype = args[1]
			
			if(filetype != "accounts" and filetype != "wordlist"):
				filetype = filetype / 0 # throw an error to trigger the syntax thingy
			
			if(filetype == "accounts"):
				try:
					service = args[2] # organization
				except:
					service = "mixed"
				
				try:
					temp = database["accounts"][service]
				except KeyError:
					database["accounts"][service] = {}
			
			with open(filename) as f:
				fileRaw = f.read() # read the file
			
			if(filetype == "wordlist"): # add wordlist to database
				words = fileRaw.split("\n")
				for word in words:
					database["wordlist"].append(word)
			else: #add accounts to database
				accountslist = fileRaw.split("\n")
				accounts = []
				for account in accountslist:
					account = account.split(":")
					accounts.append(account)
				for account in accounts:
					if(len(account) == 2):
						database["accounts"][service][account[0]] = account[1]
				
		except FileNotFoundError:
			print(" [-] File not found.")
		
		except:
			print(" [*] Usage:")
			print("     import file accounts service - Import an account and sort by service. Default service is mixed.")
			print("     import file wordlist - Use only for password wordlists - seperated by newline.")
				
