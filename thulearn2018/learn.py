#-*- coding: UTF-8 -*-

import requests, os, sys, re, json, time
from bs4 import BeautifulSoup

class Learn():
	def __init__(self):
		headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36' }
		self.session = requests.Session()
		self.session.headers = headers
		self.url = "http://learn2018.tsinghua.edu.cn/"
		self.semester = ""

		self.init_user()
		self.check_save_path()

		# login and get current sememster
		self.login()
		self.set_semester()

		self.init_lessons()

	def init_user(self):
		try:
			f = open("/tmp/user.txt", "r")
			lines = f.readlines()
			self.username = lines[0].replace('\n', '').replace('\r', '')
			self.password = lines[1].replace('\n', '').replace('\r', '')
			f.close()
		
		except:
			print("Enter your username: ")
			self.username = raw_input()
			print("Enter your password: ")
			self.password = raw_input()

			sf = open("/tmp/user.txt", "w")
			print >> sf, self.username
			print >> sf, self.password
			sf.close()

	def check_save_path(self):

		try:
			f = open("/tmp/path.txt", "r")
			self.path = f.readlines()[0].replace('\n', '').replace('\r', '')
			f.close()

		except:
			print("Enter the directory to save documents for this semester: ")
			self.path = raw_input()
			sf = open("/tmp/path.txt", "w")
			print >> sf, self.path
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
		content = json.loads(self.session.get(semester_url).content)

		# use try!!!
		if (content["message"] == "success"):
			self.semester = content["result"]["id"]

	def get_lessons(self):
		# get lesson id
		lessons_url = self.url + "/b/wlxt/kc/v_wlkc_xs_xkb_kcb_extend/student/loadCourseBySemesterId/" + self.semester
		lesson_json = json.loads(self.session.post(lessons_url).content)["resultList"]
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
		files = json.loads(self.session.post(files_url, data = {"wlkcid": lesson_id}).content)
		files_id = []

		for row in files["object"]["rows"]:
			files_id.append(row["id"])

		return files_id
		

	def download_files(self, lesson_id, lesson_name, file_id):
		# download files
		# lesson_id example "2018-2019-226ef84e7689589e90168990b99383064"
		# file_id example "sjqy_26ef84e7689589e90168990b993830641"
		file_url = self.url + "b/wlxt/kj/wlkc_kjxxb/student/kjxxb/" + lesson_id + "/" + file_id
		files = json.loads(self.session.get(file_url).content)
		for f in files["object"]:
			file_name = f[1]
			fid = f[7]
			#  fid example "2007990011_KJ_1548755901_04ee49a1-3a86-4b4e-841a-b5b55e789234_sjqy01-admin"

			download_before_url = self.url + "b/kc/wj_wjb/downloadFileBefore" + "?wjid=" + fid
			download_url = self.url + "b/wlxt/kj/wlkc_kjxxb/student/downloadFile" + "?sfgk=0" + "&wjid=" + fid

			page = self.session.get(download_before_url)
			f = self.session.get(download_url)

			fname = "UNKNOWN"
			if (f.headers["Content-Disposition"][:21] == "attachment; filename="):
				fname, extension = os.path.splitext(f.headers["Content-Disposition"][22:-1])
					
			if (fname != "UNKNOWN"):

				print("  New " + file_name + extension + " !")

				with open(self.path + "/" + lesson_name + "/" + file_name + extension, "wb") as local:
					for chunk in f.iter_content(chunk_size = 1024):
						local.write(chunk)


def download():
	learn = Learn()
	lessons = learn.get_lessons()
	for lesson in lessons:
		print("Check " + lesson[1])
		groups = learn.get_files_id(lesson[0])
		for group in groups:
			learn.download_files(lesson[0], lesson[1], group)


if __name__ == "__main__":
	download()
