# torque_calibration.py
# This script is used to calibration each IRAD actuator
# for torque sensings. The script will run each actuator
# through 2 cycles and generate a calibration curve for
# torque sensing.
# author: Thara Randhawa
# e-mail: thara.randhawa@motivss.com
# date: 10-04-2017

import serial, sys, time, string, binascii, struct, csv
import msvcrt as m
from calibration_fxns import parse_csv

class act_profile:
	def __init__(self):
		self.type_ = '50009900'
		self.sn_ = '0001'
		self.rev_ = 'BLK2'

class signals:
	
	def __init__(self):

		self.num_sigs = 0
		self.data_pts = 0
		self.samp_res = 0
		self.samp_step = 0
		self.rec_v_ = 'RC=0x0'
		self.header_ = 'Time,Input,Output,Torque'

class mtr_settings:
	def __init__(self):
		self.mtr_sp = 0
		self.stop_pos = 0

class elmo_client:

	def __init__(self, port):

		self.s = serial.Serial(port, baudrate=115200, bytesize=8, parity='N',
			stopbits=1, timeout=None, xonxoff=0, rtscts=0)

		self.cmd = ''
		self.value = ''

		self.data = [[sig_.samp_step*x for x in range(sig_.data_pts)] for y in range(sig_.num_sigs + 1)]

	def read(self):

		# number of bytes
		READ_BUFFER_SIZE = 1 

		# mode of commands
		parse_mode = 0;

		cmd_buff = ''

		value_buff = ''

		while parse_mode != 2:

			rx_byte = self.s.read(READ_BUFFER_SIZE)

			if ord(rx_byte) == ord('\r'):

				parse_mode = 1

			elif ord(rx_byte) == ord(';'):

				parse_mode = 2	

			else:

				if parse_mode == 0:

					cmd_buff += rx_byte

				else:

					value_buff += rx_byte

		parse_mode = 0

		self.cmd = cmd_buff

		# sys.stdout.write (self.cmd)
		# sys.stdout.write (' ')

		self.value = value_buff
		# sys.stdout.write (self.value)
		# sys.stdout.write ('\n')


		rx_byte = ''

		cmd_buff = ''

		value_buff = ''

	def write(self, cmd_string):

		self.s.write(cmd_string)

		self.read()

	def parse_record_data(self, str_array, sig_num):

		var_size = int(str_array[0:2],16)

		tx_size = int(str_array[2:4],16)

		ts_multiplier = int(str_array[4:8],16)

		sampling_time = int(str_array[8:12],16)

		conv_factor = struct.unpack('>f', str_array[12:20].decode('hex'))[0]

		# print (str(conv_factor))

		for x in xrange(0,(len(str_array)-20)/tx_size):

			if var_size == 0 :

				data_raw = int(str_array[20+tx_size*x:20+tx_size*(x+1)], 16)

				if data_raw > 2**(4*tx_size-1)-1:
					data_raw = data_raw - 2**(4*tx_size)
				# if tx_size == 8:
				# 	data_raw = struct.unpack('>q', str_array[20+tx_size*x:20+tx_size*(x+1)].decode('hex'))[0]
				# else:
				# 	data_raw = struct.unpack('>i', str_array[20+tx_size*x:20+tx_size*(x+1)].decode('hex'))[0]					
			else:

				data_raw = struct.unpack('>f', str_array[20+tx_size*x:20+tx_size*(x+1)].decode('hex'))[0]

			self.data[sig_num][x] = data_raw * conv_factor
		
		# print (str(self.data[8][0]))

	def close(self):

		self.s.close()

def elmo_init():

	reader.write('MO=0\r')

	reader.write('CA[16]=0\r')

	reader.write('SP[1]=%s\r' % mtr_set_.mtr_sp)

	reader.write('AC[1]=1000000\r')

	reader.write('DC[1]=1000000\r')

	reader.write('SD[1]=1000000\r')

	reader.write('MO=1\r')

	reader.write('SO\r')

	while reader.value != '1':

		reader.write('SO\r')
#		reader.write('MO=1\r')

	print ('elmo initialization completed')

def elmo_run_in_begin():

	reader.write('MR[1]=2\r')

	reader.write('MR[3]=0\r')

	reader.write('MR[4]=%s\r' % mtr_set_.stop_pos)

	reader.write('BG\r')

	print ('run-in begins')

def elmo_run_in_finished():

	reader.write('MR[1]=0\r')

	reader.write('MR[3]=0\r')

	reader.write('PA[1]=0\r')

	reader.write('BG\r')

	reader.write('PX\r')
	
	while reader.value != '0':

		reader.write('PX\r')
	
	reader.write('MO=0\r')

	reader.write('SO\r')
	
	while reader.value != '0':

		reader.write('SO\r')
	
	print ('run-in finished')


def elmo_recorder_config():

	reader.write('RV[1]=70\r') # Relative Input

	reader.write('RV[2]=71\r') # Absolute Output

	reader.write('RV[3]=72\r') # Rxn Torque Sensor

	reader.write('RV[4]=10\r') # Active Current

	reader.write('%s\r' % sig_.rec_v_) # Define recorded variables

	reader.write('RP[0]=1\r') # Time quantum is TS, 50us

	reader.write('RG=%s\r' % sig_.samp_res)# % samp_res)  # Resolution, 50us * 160

	reader.write('RL=%s\r' % sig_.data_pts) # Number of Samples

	reader.write('RP[1]=1\r') # Trigger variable

	reader.write('RP[2]=0\r') # Pre-trigger percentage

	#reader.write('RP[3]=2\r') # Trigger type: positive
	reader.write('RP[3]=0\r') # Immediate trigger

	reader.write('RP[4]=100\r') # Trigger value

	reader.write('RP[8]=0\r')

	reader.write('RP[9]=0\r') 

	print ('Elmo recorder setup completed')

def elmo_recorder_trigger():

	reader.write('RR=3\r') # Start recording

	reader.write('RR\r')

	while int(reader.value) != 0:

		reader.write('RR\r')

	for x in range (sig_.num_sigs):

		# print (x)

		reader.write('BH='+str(int(1<<x))+'\r')

		reader.parse_record_data(reader.value, x+1)

# calculating the time es
def stop_watch (start_time):
	
	current_time = time.clock();

	return current_time - start_time;

# creating csv file based on elmo's csv format
# use Elmo Recording Data View to view the data
def create_csv(filename):
	with open (filename, 'wb') as f:
		f.write('%s\n' % sig_.header_)

		for x in range (sig_.data_pts):

			for y in range (sig_.num_sigs + 1):

				f.write(str(reader.data[y][x]))

				f.write(',')

			f.write('\n')

		f.close()

def write_calibration(filename, cal_curve):
	with open (filename, 'wb') as c:
		c.write('Pos,Delta\n')
		
		for pos in range(cal_curve[:,1].size):
			c.write(str(cal_curve[pos,0]))
			c.write(',')
			c.write(str(cal_curve[pos,1]))
			c.write('\n')
			
		c.close()

def update_sampling():
	run_time = mtr_set_.stop_pos / mtr_set_.mtr_sp
	sig_.samp_res = int(run_time / sig_.data_pts)
	sig_.samp_step = sig_.samp_res*0.00005

if __name__ == "__main__":

	#actuator test profile:
	act_ = act_profile()

	act_.type_ = '50009900'
	act_.sn_ = '0012'

	#signals
	sig_ = signals()

	#nominal error run settings
	sig_.num_sigs = 2
	sig_.data_pts = 7500
	sig_.samp_res = 106
	sig_.samp_step = sig_.samp_res*0.00005
	sig_.rec_v_ = 'RC=0x3'
	sig_.header_ = 'Time,Input,Output'
	
	#motor settings
	mtr_set_ = mtr_settings()
	mtr_set_.mtr_sp = 125000
	mtr_set_.stop_pos = -5000000


	# update_sampling()
	
	comport = sys.argv[1]

	reader = elmo_client(comport)

	#prompt user for actuator profile
	act_.type_ = input('Enter the actuator pn (i.e. 5000XXXX): ')
	act_.sn_ = input('Enter the actuator sn: ')
	#act_.rev_ = input('Enter the actuator revision (i.e. BLK1 or BLK2)')

	cont_ = input('Enter 1 to perform nominal calibration')
	if(cont_ == 1):
		elmo_init()

		s_time = time.clock()

		#begin nominal error run
		elmo_run_in_begin()

		elmo_recorder_config()

		elmo_recorder_trigger()

		csv_name = 'unloaded_' + str(act_.type_) + '_' + str(act_.sn_) + '_' + str(act_.rev_) + '.csv'

		create_csv(csv_name)

		print (csv_name + ' is created and saved.')	

		reader.write('UI[1]\r')
		ssi_pos = reader.value
		print ('Starting Rotor Position: %s', ssi_pos)

		# cal_curve = parse_csv('run 0 min.csv')		

		elmo_run_in_finished()

		# write_calibration('cal_.csv', cal_curve = cal_curve)


	reader.close()
	
	#begin small load calibration cycle
	#loaded run settings
	sig_.num_sigs = 4
	sig_.data_pts = 4000
	sig_.samp_res = 160
	sig_.samp_step = sig_.samp_res*0.00005
	sig_.rec_v_ = 'RC=0xF'
	sig_.header_ = 'Time,Input,Output,Torque,Current'
	
	# update_sampling()

	raw_input("Load actuator with small load and press any key to continue...")
	
	# reader.data = [[sig_.samp_step*x for x in range(sig_.data_pts)] for y in range(sig_.num_sigs + 1)]

	reader = elmo_client(comport)

	cont_ = input('Enter 1 to perform nominal calibration')
	if(cont_ == 1):

		elmo_init()

		elmo_run_in_begin()

		elmo_recorder_config()

		elmo_recorder_trigger()

		csv_name = 'lowload_' + str(act_.type_) + '_' + str(act_.sn_) + '_' + str(act_.rev_) + '.csv'

		create_csv(csv_name)

		print (csv_name + ' is created and saved.')

		elmo_run_in_finished()


	reader.close()

		#begin small load calibration cycle
	#loaded run settings
	sig_.num_sigs = 4
	sig_.data_pts = 4000
	sig_.samp_res = 160
	sig_.samp_step = sig_.samp_res*0.00005
	sig_.rec_v_ = 'RC=0xF'
	sig_.header_ = 'Time,Input,Output,Torque,Current'
	
	# update_sampling()

	raw_input("Load actuator with large load and press any key to continue...")
	
	# reader.data = [[sig_.samp_step*x for x in range(sig_.data_pts)] for y in range(sig_.num_sigs + 1)]

	reader = elmo_client(comport)

	cont_ = input('Enter 1 to perform nominal calibration')
	if(cont_ == 1):

		elmo_init()

		elmo_run_in_begin()

		elmo_recorder_config()

		elmo_recorder_trigger()

		csv_name = 'highload_' + str(act_.type_) + '_' + str(act_.sn_) + '_' + str(act_.rev_) + '.csv'

		create_csv(csv_name)

		print (csv_name + ' is created and saved.')

		elmo_run_in_finished()


	reader.close()