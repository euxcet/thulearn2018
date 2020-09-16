from . import settings
from . import utils
import platform
import getpass
import os, sys

class FileManager():
	def __init__(self):
		pass

	def mkdir(self, name):
		if not os.path.exists(name):
			# os.mkdir(name)
			os.makedirs(name)

	def mkdirl(self, name):
		self.mkdir(name)
		self.mkdir(name + os.sep + "file")
		self.mkdir(name + os.sep + "homework")

	def set_user(self):
		print("Enter your username: ")
		username = input()
		print("Enter your password: ")
		password = getpass.getpass()
		sf = open(settings.user_file_path, 'w')
		print(username, file = sf)
		print(password, file = sf)
		sf.close()
		return (username, password)

	def get_user(self):
		try:
			f = open(settings.user_file_path, 'r')
			lines = f.readlines()
			username = lines[0].replace('\n', '').replace('\r', '')
			password = lines[1].replace('\n', '').replace('\r', '')
			f.close()
		except:
			username, password = self.set_user()

		return (username, password)

	def set_local(self):
		sf = open(settings.local_file_path, 'w')
		sf.close()

	def get_local(self):
		local = set()
		try:
			f = open(settings.local_file_path, 'r')
			lines = f.readlines()
			for line in lines:
				local.add(line.replace('\n', '').replace('\r', ''))
			f.close()
		except:
			self.set_local()
		return local

	def set_path(self):
		print("Enter the directory to save documents for this semester: ")
		path = input()
		sf = open(settings.path_file_path, 'w')
		print(path, file = sf)
		sf.close()
		return path

	def get_path(self):
		try:
			f = open(settings.path_file_path, 'r')
			path = f.readlines()[0].replace('\n', '').replace('\r', '')
			f.close()
		except:
			path = self.set_path()
		return path

	def append(self, fname, content):
		try:
			f = open(fname, 'a')
			print(content, file = f)
			f.close()
		except:
			pass
	def init_homework(self, hw, hw_dir, hw_title, hw_readme):
		if (not os.path.exists(hw_dir + os.sep + ".xszyid")):
			print("  Homework " + hw_title)

		self.mkdir(hw_dir)

		try:
			f = open(hw_dir + os.sep + "README.md", 'w', encoding = 'utf-8')
			f.write(hw_readme)
			f.close()
		except:
			pass

		if (not os.path.exists(hw_dir + os.sep + ".xszyid")):
			with open(hw_dir + os.sep + ".xszyid", "w") as f:
				f.write(hw["xszyid"])

	def downloadto(self, save_path, file_page, file_name, file_id):
		total_size = 0
		try:
			total_size = int(file_page.headers['Content-Length'])
		except:
			pass
		temp_size = 0
		print("  New " + file_name + " !")
		if (not os.path.exists(save_path)):
			print("  Create " + file_name)
		else:
			print("  Cover " + file_name)
		with open(save_path, "wb") as local:
			for chunk in file_page.iter_content(chunk_size = 1024 * 10):
				if chunk:
					temp_size += len(chunk)
					local.write(chunk)
					local.flush()
					if (total_size != 0):
						done = int(30 * temp_size / total_size)
						space = " "
						if (platform.system() == "Windows"):
							space = "  "
						sys.stdout.write("\r[%s%s] %d%% %s/%s    \t" % ('█' * done, space * (30 - done), 100 * temp_size / total_size, utils.size_format(temp_size), utils.size_format(total_size)))
						sys.stdout.flush()
					else:
						sys.stdout.write("\r\t%s/UNKNOWN    \t" % (utils.size_format(temp_size)))
						sys.stdout.flush()

		print()
