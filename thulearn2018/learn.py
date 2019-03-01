#-*- coding: UTF-8 -*-

import sys, os
from . import browser

def show_help():
	print("usage:  learn <command>")
	print("command:")
	print("\treset\t\t\tReset configuration")
	print("\tclear\t\t\tClear configuration")
	print("\tupload YOURFILE\t\tUpload homework")

def download(learn):
	lessons = learn.get_lessons()
	for lesson in lessons:
		print("Check " + lesson[1])
		groups = learn.get_files_id(lesson[0])
		for group in groups:
			learn.download_files(lesson[0], lesson[1], group)
		learn.download_homework(lesson[0], lesson[1])

def upload(learn, upload_file_path):
	id_path = '.' + os.sep + ".xszyid"
	if (not os.path.exists(id_path)):
		print("Homwork Id Not Found!")
		return
	if (not os.path.exists('.' + os.sep + upload_file_path)):
		print("Upload File Not Found!")
		return
	with open(id_path, 'r') as f:
		xszyid = f.read().strip()
	f.close()
	learn.upload(xszyid, '.' + os.sep + upload_file_path)

def main():
	learn = browser.Learn()
	if (len(sys.argv) == 1):
		download(learn)
	elif (len(sys.argv) == 2):
		if (sys.argv[1] == "reset"):
			learn.set_user()
			learn.set_path()
		if (sys.argv[1] == "clear"):
			learn.set_local()
		else:
			show_help()
	elif (len(sys.argv) == 3):
		if (sys.argv[1] == "upload"):
			upload(learn, sys.argv[2])
		else:
			show_help()
	else:
		show_help()

if __name__ == "__main__":
	main()
