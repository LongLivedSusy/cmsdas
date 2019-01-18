import json

json_file = "limits.json"
with open(json_file, "r") as read_file:
	data = json.load(read_file)

ctau_list = [float(ct) for ct in data]
ctau_list.sort()

output_file = "limits_info.txt"
with open(output_file, "w") as write_file:
	write_file.write("# x, y, -2, +2, -1, +1 \n")
	for ctau in ctau_list:
		string = "{0} {1} {2} {3} {4} {5} \n".format(int(ctau), data[str(ctau)]["exp0"], data[str(ctau)]["exp-2"], data[str(ctau)]["exp+2"], data[str(ctau)]["exp-1"], data[str(ctau)]["exp+1"])
		write_file.write(string)
		print string
