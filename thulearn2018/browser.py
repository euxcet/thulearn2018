import requests, os, sys, re, json, time, getpass
import tempfile
from bs4 import BeautifulSoup
from collections import OrderedDict
from urllib3 import encode_multipart_formdata
from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests.packages.urllib3.exceptions import InsecureRequestWarning

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


		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
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

	def clear_config(self):
		f = open(self.local_file_path, 'w')
		f.close()

	def login(self):
		# login
		form = { "i_user" : self.username, "i_pass" : self.password }
		login_id = self.session.post("https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/bb5df85216504820be7bba2b0ae1535b/0?/login.do", data = form, verify = False)
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



	#-------------------------------------------------------------------------------------------

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
			name = self.path + os.sep + lesson[1]
			if not os.path.exists(name):
				os.mkdir(name)
			if not os.path.exists(name + os.sep + "file"):
				os.mkdir(name + os.sep + "file")
			if not os.path.exists(name + os.sep + "homework"):
			 	os.mkdir(name + os.sep + "homework")

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


	def file_id_exist(self, fid):
		if (fid not in self.local):
			return False
		return True

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

	def size_format(self, size_b):
		if(size_b < 1024):
			return "%.2f"%(size_b) + 'B'
		elif(size_b < 1024 * 1024):
			return "%.2f"%(size_b / 1024) + 'KB'
		elif(size_b < 1024 * 1024 * 1024):
			return "%.2f"%(size_b / 1024 / 1024) + 'MB'
		elif(size_b > 1024 * 1024 * 1024 * 1024):
			return "%.2f"%(size_b / 1024 / 1024 / 1024) + 'GB'

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

			if (self.file_id_exist(fid)):
				continue

			download_before_url = self.url + "b/kc/wj_wjb/downloadFileBefore" + "?wjid=" + fid
			download_url = self.url + "b/wlxt/kj/wlkc_kjxxb/student/downloadFile" + "?sfgk=0" + "&wjid=" + fid

			page = self.session.get(download_before_url)
			f = self.session.get(download_url, stream=True)

			fname = "UNKNOWN"
			if (f.headers["Content-Disposition"][:21] == "attachment; filename="):
				fname, extension = os.path.splitext(f.headers["Content-Disposition"][22:-1])

			if (fname != "UNKNOWN"):
				fpath = self.path + os.sep + lesson_name + os.sep + "file" + os.sep + file_name + extension
				self.downloadto(fpath, f, file_name + extension, fid)
				self.save_file_id(fid)

	def homework(self, lesson_id, lesson_name):
		title = ["作业内容及要求：", "本人提交的作业："]
		subtitle = ["作业标题", "作业说明", "作业附件", "答案说明", "答案附件", "发布对象", "完成方式", "学号", "提交日期", "截止日期", "上交作业内容", "上交作业附件"]
		form = "aoData=[{\"name\":\"wlkcid\",\"value\":\"" + lesson_id + "\"}]"
		api_list = ["b/wlxt/kczy/zy/student/zyListYjwg?", "b/wlxt/kczy/zy/student/zyListWj?"]
		for api in api_list:
			hws = self.session.get(self.url + api + form)
			try:
				hws = json.loads(hws.content)
			except TypeError:
				hws = json.loads(bytes.decode(hws.content))

			for hw in hws["object"]["aaData"]:
				url = self.url + "f/wlxt/kczy/zy/student/viewTj?wlkcid=" + lesson_id + "&sfgq=0&zyid=" + hw["zyid"] + "&xszyid=" + hw["xszyid"]
				page = self.session.get(url)
				soup = BeautifulSoup(page.content, "html.parser")
				boxbox = soup.find_all('div', class_ = "boxbox")[0]
				txt = boxbox.get_text().replace('\t', '').split('\n')
				hw_title = boxbox.find_all('div', class_ = "right")[0].get_text().strip()
				hw_readme = ""
				for line in txt:
					l = line.strip()
					if (len(l) > 0):
						if (l in subtitle):
							hw_readme += "#### " + l + '\n'
						elif (l in title):
							hw_readme += "### " + l + '\n'
						else:
							hw_readme += l + '\n'

				hw_dir = self.path + os.sep + lesson_name + os.sep + "homework" + os.sep + hw_title

				if(os.path.exists(hw_dir + os.sep + ".xszyid")):
					continue

				print("  Homework " + hw_title)
				if (not os.path.exists(hw_dir)):
					os.mkdir(hw_dir)
				try:
					if(not os.path.exists(hw_dir + os.sep + "README.md")):
						f = open(hw_dir + os.sep + "README.md", 'w', encoding = 'utf-8')
						f.write(hw_readme)
						f.close()
				except:
					pass

				if (not os.path.exists(hw_dir + os.sep + ".xszyid")):
					with open(hw_dir + os.sep + ".xszyid", "w") as f:
						f.write(hw["xszyid"])

				annex = soup.find_all('div', class_ = 'list fujian clearfix')[0]
				annex_url = annex.find_all('a')
				if(len(annex_url) > 0):
					annex_name = annex_url[0].get_text().strip()
					download_url = self.url + annex_url[1].get('href')
					annex_id = annex_url[1].get('href').split('/')[-1]
					if(self.file_id_exist(annex_id)):
						continue

					annex_page = self.session.get(download_url, stream=True)
					self.downloadto(hw_dir + os.sep + annex_name, annex_page, annex_name, annex_id)
					self.save_file_id(annex_id)

	def downloadto(self, save_path, file_page, file_name, file_id):
		total_size = int(file_page.headers['Content-Length'])
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
					done = int(50 * temp_size / total_size)
					sys.stdout.write("\r[%s%s] %d%% %s/%s         \t" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size, self.size_format(temp_size), self.size_format(total_size)))
					sys.stdout.flush()
		print()

	def upload(self, homework_id, file_path):
		upload_api = 'b/wlxt/kczy/zy/student/tjzy'

		# headers = self.session.headers + {"Content-Type" : "multipart/form-data; boundary=----WebKitFormBoundaryTytyPd5kgvE3t0kW"}
		headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
		 		'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundaryTytyPd5kgvE3t0kW'}
		m = MultipartEncoder(
			fields = {
				'fileupload' :(os.path.basename(file_path), open(file_path, 'rb'), 'application/octet-stream'),
				'xszyid' : homework_id,
				'isDeleted' : '0',
				'zynr': ''
			},
			boundary = '----WebKitFormBoundaryTytyPd5kgvE3t0kW'
		)
		self.session.post(self.url + upload_api, data = m, headers = headers)
