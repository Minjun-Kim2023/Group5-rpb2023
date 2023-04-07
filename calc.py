def main():
	print("Let's implement division.")
	x = int(input("x > "))
	y = int(input("y > "))
	print("%d/%d=%0.3f" % (x,y,divide(x,y)))
def add(x,y):
	return x+y

def divide(x,y):
	if y == 0:
		print("Error : cannot divide by zero.")
	else:
		return x/y


main()
