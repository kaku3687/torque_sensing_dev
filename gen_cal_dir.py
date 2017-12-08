import os, errno

working_dir = "C:/Users/Owner/Documents/Robomantis_Cal/"

type_ = ["50009880", "50009900", "50010350"]
type_1_start = 11
type_3_start = 16
type_5_start = 3

type_1_num = 12
type_3_num = 18
type_5_num = 4



for i in range(type_1_start, (type_1_num + type_1_start)):
	dir_name = working_dir + type_[0] + "_00" + str(i) + "_BLK2"
	file_name = dir_name + "/" + "README_" + type_[0] + "_00" + str(i) + ".txt"
	rdme_f = open(file_name, "w")
	rdme_f.write(file_name)
	rdme_f.write("\n")
	rdme_f.write("Calibrated On:")
	rdme_f.write("Calibrated By:")
	rdme_f.write("\n")
	rdme_f.write("Commutation Parameters:")
	rdme_f.write("		CS:")
	rdme_f.write("		SSI1:")
	rdme_f.write("\n")
	rdme_f.write("Nominal Temperature:")
	rdme_f.write("\n")
	rdme_f.write("SSI1:")
	rdme_f.write("		0 Rel:")
	rdme_f.write("		10000 Rel:")
	rdme_f.write("		0 Rel:")
	rdme_f.close()

	try:
		os.makedirs(dir_name)
	except OSError as e:
		if e.errno !=errno.EEXIST:
			raise