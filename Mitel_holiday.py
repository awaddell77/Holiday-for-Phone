#mitel holiday 
from Sel_session import *
from dictionarify import *
import credentials
import time, sys
from os import getcwd, path



def text_wc(x,output='listoutput.txt', v = 0):#takes list writes to text
	if '.' not in output:
		raise TypeError("No file extension detected.")
	n_l = x
	name = output
	num = 0
	while(file_present(output)):
		num += 1
		fname_extension = output.split('.')
		fname, extension = fname_extension[0], fname_extension[1]
		output = fname + str(num) + "." + extension
	with open(name, 'w') as wf:
		for i in range(0, len(n_l)):
			if v:
				print(n_l[i])
				new = n_l[i]
				wf.writelines(new)

			else:
				new = n_l[i]
				wf.writelines(new + "\n")
	print("%s saved to %s" % (output, output))
	return True

def file_present(x):
	#only checks current working directory
	full_path = getcwd() + '\\' + x
	if path.exists(full_path):
		return True
	if not path.exists(full_path):
		return False


class Mitel_holiday:
	def __init__(self, holiday_file, number_file):
		#set the location of the driver argument to wherever the firefox.exe file is on your system
		
		self.browser = Sel_session(url='http://www.fsf.org/', driver = 'C:\\Program Files\\Mozilla Firefox71\\firefox.exe')
		self.def_window	= self.browser.driver.current_window_handle	
		self.holiday_file = dictionarify(holiday_file)
		self.number_file = dictionarify(number_file)
		self.completed = []
	def login(self):
		self.browser.go_to("https://10.0.99.10/server-common/cgi-bin/login?back=https%3a%2f%2f10.0.99.10%2fserver-manager%2f")
		time.sleep(5)
		
		self.browser.js('document.getElementsByName("username")[0].value = "{0}";'.format(credentials.USER_NAME))
		self.browser.js('document.getElementsByName("password")[0].value = "{0}";'.format(credentials.PASSWORD))
		self.browser.js('document.getElementsByName("submit")[0].click()')
		return

	def main(self):
		self.login()
		print("Logged in")

		time.sleep(5)
		print("SM")
		self.browser.driver.switch_to.frame(self.browser.driver.find_element_by_name('navigation'))
		self.browser.driver.execute_script('document.getElementById("sme4").click();') #clicks "NuPoint Webconsole" link
		time.sleep(5)
		print("NPM")
		self.browser.js('document.getElementById("npm41").click();') #clicks the "Call Flow" link
		time.sleep(5)
		for i in range(0, len(self.number_file)):
			print("Processing {0}...".format(self.number_file[i]["Number"]))
			self.browser.driver.switch_to.default_content()
			self.browser.driver.switch_to.frame(self.browser.driver.find_element_by_name('main'))
			self.add_holiday(self.number_file[i]["Number"])
			self.completed.append(self.number_file[i]["Number"])
			self.browser.driver.switch_to.default_content()
			time.sleep(1)
			self.browser.driver.switch_to.frame(self.browser.driver.find_element_by_name('navigation'))
			time.sleep(2)
			self.browser.js('document.getElementById("npm41").click();')
			time.sleep(3)
		print("Finished updating")
		text_wc(self.completed, "holiday_schedule_numbers_completed.txt")
	def add_holiday(self, number):
		print("Adding holiday start")
		time.sleep(5)
		com = 'document.getElementsByName("number")[0].value = {0};'.format(number)
		self.browser.js(com)
		print("typed name")
		#self.browser.driver.switch_to.frame(self.browser.driver.find_element_by_name('tui_frame'))
		#print("Switched frame")
		time.sleep(5)
		
		self.browser.js('document.getElementById("view_label").click();')#clicks the Edit button
		print("Submitted")
		time.sleep(5)
		self.browser.js('document.getElementById("sd2").click();') #clicks the "Holiday Schedule" link
		self.browser.js('document.getElementsByClassName("buttonGreen")[0].children[0].click()') #clicks the "Holiday Schedule" button
		holiday_window = self.browser.driver.window_handles[1]
		print("Switching to new window")

		self.browser.driver.switch_to_window(holiday_window)
		
		delete_com = '''
			var len = document.getElementsByName('delete').length;
			for (i = 0; i <= len; i++){
				if (document.getElementById('delete')){ 
						document.getElementById('delete').click();
				};
			};'''

		time.sleep(2)
		self.browser.js(delete_com)
		time.sleep(2)
		print("Adding new holidays")
		for i in range(0, len(self.holiday_file)):
			self.browser.js('document.getElementById("name_field").value = "{0}";'.format(self.holiday_file[i]["name"]))

			self.browser.js('document.getElementById("start_date").value = "{0}";'.format(self.holiday_file[i]["startDay"]))
			self.browser.js('document.getElementById("start_am_pm").value = "AM";')
			self.browser.js('document.getElementById("start_hour").value = "12";')
			self.browser.js('document.getElementById("end_date").value = "{0}";'.format(self.holiday_file[i]["endDay"]))
			self.browser.js('document.getElementById("end_hour").value = "11";')
			self.browser.js('document.getElementById("end_min").value =  "59";')
			self.browser.js('document.getElementById("end_am_pm").value = "PM";')
			self.browser.js('document.getElementById("add").click();')
		print("Done with adding the holidays, now attempting to submit and save")

		self.browser.js('tobeSaved = 0')

		time.sleep(3)
		print("tobeSaved == 1: {0}".format(self.browser.js("return tobeSaved == 1"))) #needs to be false NOTE THIS DOESN'T ACTUALLY WORK WITHOUT A PROXY
		self.browser.js('document.getElementById("submit").click();')
		time.sleep(3)
		print("accepted alert")
		time.sleep(2) 
		print("Trying to switch windows") 
		#this has to be done because the alert in the holiday schedule window doesn't agree with Selenium for some reason
		self.browser.driver.switch_to_window(self.def_window)
		time.sleep(1)
		self.browser.js('document.getElementsByClassName("buttonGreen")[0].children[0].click()')
		self.browser.driver.switch_to_window(holiday_window)
		self.browser.driver.close()
		self.browser.driver.switch_to_window(self.def_window)
		print("Switched windows")
		time.sleep(2)
		print("Trying to click the save button")
		#print("")
		self.browser.js('document.getElementById("save2_label").click();')
		time.sleep(2)
		alert = self.browser.driver.switch_to.alert
		
		alert.dismiss()

		
		return


if __name__ == '__main__':
	if sys.argv[1] in ['?', '-help', '-h']: print("Mitel_holiday.py [holiday_file] [phone_file]")
	else:
		holiday_file = sys.argv[1]
		phone_file = sys.argv[2]
		if '.csv' not in holiday_file or '.csv' not in phone_file: print("Both files must be CSV files")
		m_inst = Mitel_holiday(holiday_file, phone_file)
		m_inst.main()

#m_inst.main()


