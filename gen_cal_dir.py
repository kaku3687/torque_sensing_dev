import os, errno

working_dir = "C:/Users/trandhawa/Documents/Robomantis_Cal/"

type_135 = ["50009880", "50009900", "50010350"]
start_135 = [11, 16, 3]

num_135 = [12, 18, 4]

act_prof = [type_135, start_135, num_135]

for k in range(len(act_prof[0])):
	for i in range(int(act_prof[1][k]), (int(act_prof[2][k]) + int(act_prof[1][k]))):
		dir_name = working_dir + act_prof[0][k] + "_00" + str(i) + "_BLK2"
		try:
			os.makedirs(dir_name)
		except OSError as e:
			if e.errno !=errno.EEXIST:
				raise
		file_name = dir_name + "/" + "README_" + act_prof[0][k] + "_00" + str(i) + ".txt"

		rdme_f = open(file_name, "w")
		rdme_f.write(act_prof[0][k] + "_00" + str(i))
		rdme_f.write("\n")
		rdme_f.write("Calibrated On:")
		rdme_f.write("\n")
		rdme_f.write("\n")
		rdme_f.write("Calibrated By:")
		rdme_f.write("\n")
		rdme_f.write("\n")
		rdme_f.write("Commutation Parameters:")
		rdme_f.write("\n")
		rdme_f.write("		CS:")
		rdme_f.write("\n")
		rdme_f.write("		SSI1:")
		rdme_f.write("\n")
		rdme_f.write("\n")
		rdme_f.write("Nominal Temperature:")
		rdme_f.write("\n")
		rdme_f.write("\n")
		rdme_f.write("SSI1:")
		rdme_f.write("\n")
		rdme_f.write("		0 Rel:")
		rdme_f.write("\n")
		rdme_f.write("		10000 Rel:")
		rdme_f.write("\n")
		rdme_f.write("		0 Rel:")
		rdme_f.close()
