num1=int(input("Give a number:"))
num2=int(input("Give another number:"))
if (num1%2==0) and (num2%2==0):
	print("Both numbers are even.")
elif(num1%2!=0) and (num2%2==0):
	print("One of the numbers is even.")
elif (num1%2==0) and (num2%2!=0):
	print("One of the numbers is even.")
else:
	print("Both numbers are odd.")