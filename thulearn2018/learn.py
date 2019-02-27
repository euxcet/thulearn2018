#-*- coding: UTF-8 -*-

import sys
from browser import Learn

def show_help():
	print("usage: learn <command>")
	print("\treset\t\tReset configuration")
	print("\tclear\t\tClear configuration")

def download(learn):
# file
	lessons = learn.get_lessons()
	for lesson in lessons:
		print("Check " + lesson[1])
		groups = learn.get_files_id(lesson[0])
		for group in groups:
			learn.download_files(lesson[0], lesson[1], group)
		learn.homework(lesson[0], lesson[1])

def upload(learn):
	print("upload")

def main():
	learn = Learn()
	if (len(sys.argv) == 1):
		download(learn)
	elif (len(sys.argv) == 2):
		if (sys.argv[1] == "reset"):
			learn.reset_user()
			learn.reset_save_path()
		if (sys.argv[1] == "clear"):
			learn.clear_config()
		if (sys.argv[1] == "upload"):
			upload()

if __name__ == "__main__":
	main()
