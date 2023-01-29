user=input("Give name:")
if user=="John" :
	passw=input("Give password:")
	if passw=="ABC123" :
		print("Both inputs are correct!")
	else:
		print("The password is incorrect.")
else:
	print("The given name is wrong.")