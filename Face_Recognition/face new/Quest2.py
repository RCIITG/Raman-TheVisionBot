def Quest(Keywords):
	import json
	if Keywords is "all":
		ans = open("loc.txt", "r+")
		txt = json.loads(ans.read())
		loc = txt["loc"]
		name = txt["name"]
		print("People present here are")
		for n in name:
			print(name)