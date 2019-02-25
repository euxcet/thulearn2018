#-*- coding: UTF-8 -*-

import requests, os, sys, re, json, time, getpass
from bs4 import BeautifulSoup
import tempfile


class Learn():
	def __init__(self):
		headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36' }
		self.session = requests.Session()
		self.session.headers = headers
		self.url = "http://learn2018.tsinghua.edu.cn/"
		self.semester = ""
		self.temp_path = tempfile.gettempdir()
		self.user_file_name = 'thulearn2018-user.txt'
		self.local_file_name = 'thulearn2018-local.txt'
		self.path_file_name = 'thulearn2018-path.txt'

		self.user_file_path = self.temp_path + os.sep + self.user_file_name
		self.local_file_path = self.temp_path + os.sep + self.local_file_name
		self.path_file_path = self.temp_path + os.sep + self.path_file_name

		self.init_user()
		self.init_save_path()

		# login and get current sememster
		self.login()
		self.set_semester()
		if(self.semester == ""):
			return

		self.init_lessons()
		self.local = set()
		self.init_local_files()

	def init_user(self):
		try:
			f = open(self.user_file_path, 'r')
			# f = open("/tmp/thulearn2018-user.txt", "r")
			lines = f.readlines()
			self.username = lines[0].replace('\n', '').replace('\r', '')
			self.password = lines[1].replace('\n', '').replace('\r', '')
			f.close()

		except:
			print("Enter your username: ")
			self.username = input()
			print("Enter your password: ")
			self.password = getpass.getpass()

			sf = open(self.user_file_path, 'w')
			print(self.username, file = sf)
			print(self.password, file = sf)
			sf.close()

	def init_local_files(self):
		try:
			f = open(self.local_file_path, 'r')
			lines = f.readlines()
			for line in lines:
				self.local.add(line.replace('\n', '').replace('\r', ''))
			f.close()

		except:
			sf = open(self.local_file_path, 'w')
			sf.close()

	def init_save_path(self):
		try:
			f = open(self.path_file_path, 'r')
			self.path = f.readlines()[0].replace('\n', '').replace('\r', '')
			f.close()

		except:
			print("Enter the directory to save documents for this semester: ")
			self.path = input()
			sf = open(self.path_file_path, 'w')
			print(self.path, file = sf)
			sf.close()

	def reset_user(self):
		print("Enter your username: ")
		self.username = input()
		print("Enter your password: ")
		self.password = getpass.getpass()

		sf = open(self.user_file_path, 'w')
		print(self.username, file = sf)
		print(self.password, file = sf)
		sf.close()

	def reset_save_path(self):
		print("Enter the directory to save documents for this semester: ")
		self.path = input()
		sf = open(self.path_file_path, 'w')
		print(self.path, file = sf)
		sf.close()

	def login(self):
		# login
		form = { "i_user" : self.username, "i_pass" : self.password }
		login_id = self.session.post("https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/bb5df85216504820be7bba2b0ae1535b/0?/login.do", data = form)
		soup = BeautifulSoup(login_id.content, "html.parser")
		for a in soup.find_all('a'):
			h = a.get('href')
			if (h[0:4] == "http"):
				ticket = h[-59:]

		login_url = self.url + "b/j_spring_security_thauth_roaming_entry" + ticket
		self.session.post(login_url)

	def set_semester(self):
		# get semester
		semester_url = self.url + "/b/kc/zhjw_v_code_xnxq/getCurrentAndNextSemester"
		content = {}
		try:
			content = json.loads(self.session.get(semester_url).content)
		except TypeError:
			content = json.loads(bytes.decode(self.session.get(semester_url).content))
		except Exception:
			print("密码错误")
			exit(1)

		# use try!!!
		if (content["message"] == "success"):
			self.semester = content["result"]["id"]

	def get_lessons(self):
		# get lesson id
		lessons_url = self.url + "/b/wlxt/kc/v_wlkc_xs_xkb_kcb_extend/student/loadCourseBySemesterId/" + self.semester
		try:
			lesson_json = json.loads(self.session.post(lessons_url).content)["resultList"]
		except TypeError:
			lesson_json = json.loads(bytes.decode(self.session.post(lessons_url).content))["resultList"]

		lessons = []

		for lesson in lesson_json:
			lessons.append((lesson["wlkcid"], lesson["kcm"]))

		return lessons


	def init_lessons(self):
		for lesson in self.get_lessons():
			name = self.path + "/" + lesson[1]
			if not os.path.exists(name):
				os.mkdir(name)

	def get_files_id(self, lesson_id):
		# get files by lesson id
		files_url = self.url + "b/wlxt/kj/wlkc_kjflb/student/pageList"

		# lesson_id example "2018-2019-226ef84e7689589e90168990b99383064"
		try:
			files = json.loads(self.session.post(files_url, data = {"wlkcid": lesson_id}).content)
		except TypeError:
			files = json.loads(bytes.decode(self.session.post(files_url, data = {"wlkcid": lesson_id}).content))

		files_id = []

		for row in files["object"]["rows"]:
			files_id.append(row["id"])

		return files_id


	def save_file_id(self, fid):
		if (fid not in self.local):
			self.local.add(fid)
			try:
				f = open(self.local_file_path, 'a')
				print(fid, file = f)
				f.close()
			except:
				pass
			return True
		else:
			return False

	def download_files(self, lesson_id, lesson_name, file_id):
		# download files
		# lesson_id example "2018-2019-226ef84e7689589e90168990b99383064"
		# file_id example "sjqy_26ef84e7689589e90168990b993830641"
		file_url = self.url + "b/wlxt/kj/wlkc_kjxxb/student/kjxxb/" + lesson_id + "/" + file_id
		try:
			files = json.loads(self.session.get(file_url).content)
		except TypeError:
			files = json.loads(bytes.decode(self.session.get(file_url).content))
		for f in files["object"]:
			file_name = f[1]
			#  fid example "2007990011_KJ_1548755901_04ee49a1-3a86-4b4e-841a-b5b55e789234_sjqy01-admin"
			fid = f[7]

			if (not self.save_file_id(fid)):
				continue

			download_before_url = self.url + "b/kc/wj_wjb/downloadFileBefore" + "?wjid=" + fid
			download_url = self.url + "b/wlxt/kj/wlkc_kjxxb/student/downloadFile" + "?sfgk=0" + "&wjid=" + fid

			page = self.session.get(download_before_url)
			f = self.session.get(download_url)

			fname = "UNKNOWN"
			if (f.headers["Content-Disposition"][:21] == "attachment; filename="):
				fname, extension = os.path.splitext(f.headers["Content-Disposition"][22:-1])

			if (fname != "UNKNOWN"):
				fpath = self.path + "/" + lesson_name + "/" + file_name + extension
				if (not os.path.exists(fpath)):
					print("  New " + file_name + extension + " !")
					with open(fpath, "wb") as local:
						for chunk in f.iter_content(chunk_size = 1024):
							local.write(chunk)

def show_help():
	print("usage: learn [-h] [-r] [-rp]")
	print("\t-r\tReset username and password")
	print("\t-rp\tReset the directory to save documents")

def download(learn):
	lessons = learn.get_lessons()
	for lesson in lessons:
		print("Check " + lesson[1])
		groups = learn.get_files_id(lesson[0])
		for group in groups:
			learn.download_files(lesson[0], lesson[1], group)


if __name__ == "__main__":
	learn = Learn()
	if (len(sys.argv) == 1):
		download(learn)
	elif (len(sys.argv) == 2):
		if (sys.argv[1] == "reset" or sys.argv[1] == "-r"):
			learn.reset_user()
		if (sys.argv[1] == "-rp"):
			learn.reset_save_path()
		if (sys.argv[1] == "-h"):
			show_help()
