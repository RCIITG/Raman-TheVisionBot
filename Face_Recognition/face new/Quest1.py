def Quest(Keywords):
	import json
	if Keywords == "name":
		ans = open("loc.txt", "r+")
		txt = json.loads(ans.read())
		loc = txt["loc"]
		name = txt["name"]
		i= 0
		for l in loc:
			if l == [0, 0]:
				print("Your name is " +name[i])
			i+=1

	else:
		print("Sorry didn't get you")
	ans.close()

	#else print("I dont know your name... May I know your name ?")
	#import save_name

