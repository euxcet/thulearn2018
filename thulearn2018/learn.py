#-*- coding: UTF-8 -*-

import sys, os, click
from . import browser

learn = browser.Learn()

@click.command(help = 'Download all course files')
def download():
	learn.init()
	lessons = learn.get_lessons()
	for lesson in lessons:
		click.echo("Check " + lesson[1])
		groups = learn.get_files_id(lesson[0])
		for group in groups:
			learn.download_files(lesson[0], lesson[1], group)
		learn.download_homework(lesson[0], lesson[1])

@click.command(help = 'Reset configurations.')
def reset():
	learn.set_user()
	learn.set_path()

@click.command(help = 'Show configurations.')
def config():
	username, _ = learn.get_user()
	path = learn.get_path()
	print('Username: %s' % username)
	print('Path: %s' % path)


@click.command(help = 'Clear records of all downloaded files.')
def clear():
	learn.set_local()

@click.command(help = 'Submit homework.')
@click.argument('name', default = '')
@click.option('-m', default = '', help = 'The message to submit')
def submit(name, m):
	learn.init()
	id_path = '.' + os.sep + ".xszyid"
	if (not os.path.exists(id_path)):
		print("Homwork Id Not Found!")
		return
	if (name != '' and not os.path.exists('.' + os.sep + name)):
		print("Upload File Not Found!")
		return
	with open(id_path, 'r') as f:
		xszyid = f.read().strip()
	f.close()
	learn.upload(xszyid, '.' + os.sep + name, m)

def align(string, length=0):
	len_en = len(string)
	len_utf8 = len(string.encode('utf-8'))
	lent = len_en + (len_utf8 - len_en) // 2
	return string + ' ' * (length - lent)

@click.command(help = 'Show homework deadlines.')
def ddl():
	learn.init()
	ddls = learn.get_ddl()
	print('Total %d ddl(s)' % (len(ddls)))
	for ddl in ddls:
		print(align(ddl[0][0:8], 25), align(ddl[1][0:20], 30) + align(ddl[3][0:20], 30), ddl[4])


@click.group()
def main():
	pass

main.add_command(download)
main.add_command(reset)
main.add_command(clear)
main.add_command(submit)
main.add_command(ddl)
main.add_command(config)


if __name__ == "__main__":
	main()
