import os

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from . import filemanager, jsonhelper, settings, soup, utils


class Learn():
    def __init__(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.session = requests.Session()
        self.session.headers = settings.headers

        self.fm = filemanager.FileManager()
        self.username, self.password = self.fm.get_user()
        self.path = self.fm.get_path()

        self.soup = soup.Soup()
        self.jh = jsonhelper.JsonHelper()

    def set_user(self):
        self.fm.set_user()

    def set_path(self):
        self.fm.set_path()

    def set_local(self):
        self.fm.set_local()

    def get_path(self):
        return self.fm.get_path()

    def get_user(self):
        return self.fm.get_user()

    def post(self, url, form={}, csrf=True, headers=None):
        if csrf:
            params = {
                '_csrf': self.session.cookies.get_dict()['XSRF-TOKEN']
            }
            return self.session.post(url, data=form, params=params,
                                     verify=False, headers=headers).content
        else:
            self.session.trust_env = False
            return self.session.post(url, data=form,
                                     verify=False, headers=headers).content

    def get(self, url, params={}, csrf=True):
        if csrf:
            params.update({
                '_csrf': self.session.cookies.get_dict()['XSRF-TOKEN']
            })
        return self.session.get(url, params=params).content

    def login(self):
        form = {"i_user": self.username, "i_pass": self.password}
        content = self.post(settings.login_id_url, form, csrf=False)
        ticket = self.soup.parse_ticket(content)
        self.post(settings.login_url + ticket, csrf=False)

    def set_semester(self, semester=""):
        if semester != "":
            self.semester = semester
        else:
            content = self.jh.loads(self.get(settings.semester_url))
            self.semester = content["result"]["id"]
            if os.path.exists(settings.local_file_path) and \
               not os.path.islink(settings.local_file_path):
                os.rename(settings.local_file_path,
                          os.path.join(settings.config_dir,
                                       self.semester+".txt"))
        # create or redirect local.txt to current semester
        if os.path.exists(settings.local_file_path):
            os.unlink(settings.local_file_path)
        if os.name == 'nt':
            os.link(os.path.join(settings.config_dir, self.semester+".txt"),
                    settings.local_file_path)
        else:
            os.symlink(os.path.join(settings.config_dir, self.semester+".txt"),
                       settings.local_file_path)
        self.local = self.fm.get_local()

    # -------------------------------------------------------------------------
    def get_lessons(self, exclude=[], include=[]):
        content = self.jh.loads(self.post(settings.lessons_url(self.semester)))
        # first sort by lesson name, then sort by teacher name
        lessons = [[x["wlkcid"], utils.escape_str(x["kcm"]), x["jsm"], x["kch"]]
                   for x in content["resultList"] if (x["kcm"] not in exclude) and (include == [] or x["kcm"] in include or utils.escape_str(x["kcm"]) in include)]

        lessons.sort(key=lambda x: (x[1], x[2]))

        # create a helper function to determine the folder name
        for i in range(len(lessons)):
            _, kcm, jsm, kch = lessons[i]

            # check the previous and next lesson to
            # determine the naming method of the current lesson
            prev_lesson = lessons[i-1] if i-1 >= 0 else None
            next_lesson = lessons[i+1] if i+1 < len(lessons) else None

            if (prev_lesson is None or prev_lesson[1] != kcm) and \
               (next_lesson is None or next_lesson[1] != kcm):
                lessons[i].append(kcm)
            elif (prev_lesson is None or prev_lesson[1] != kcm or
               prev_lesson[2] != jsm) and \
               (next_lesson is None or next_lesson[1] != kcm or
               next_lesson[2] != jsm):
                lessons[i].append(f"{kcm}_{jsm}")
            else:
                lessons[i].append(f"{kcm}_{kch}")
        return lessons

    def init_lessons(self, exclude, include):
        lessons = self.get_lessons(exclude=exclude, include=include)

        for i in range(len(lessons)):
            self.fm.mkdirl(os.path.join(self.path, lessons[i][4]))
        return lessons

    def get_files_id(self, lesson_id):
        form = {"wlkcid": lesson_id}
        files = self.jh.loads(self.get(settings.files_url, params=form))
        files_id = [row["id"] for row in files["object"]["rows"]]

        return files_id

    def file_id_exist(self, fid):
        return (fid in self.local)

    def save_file_id(self, fid, fpath):
        if (fid not in self.local):
            self.local.add(fid)
            self.fm.append(settings.local_file_path, fid+" "+fpath)

    def download_files(self, lesson_id, lesson_name, file_id):
        # file_id example "sjqy_26ef84e7689589e90168990b993830641"
        files = self.jh.loads(self.get(settings.file_url(lesson_id, file_id)))
        for f in files["object"]:
            # fid example "2007990011_KJ_1548755901_04ee49a1-
            # 3a86-4b4e-841a-b5b55e789234_sjqy01-admin"
            fid = f[7]
            if (not self.file_id_exist(fid)):
                self.get(settings.download_before_url(fid))
                fs = self.session.get(settings.download_url(fid), stream=True)
                if 'Content-Disposition' in fs.headers:
                    fname, extension = os.path.splitext(
                        fs.headers["Content-Disposition"][22:-1])
                elif 'ETag' in fs.headers:
                    fname, extension = os.path.splitext(fs.headers['ETag'])
                else:
                    print('not found name')
                    exit(0)
                # fix special character that exists in filename
                real_filename = utils.escape_str(f[1])
                fpath = os.path.join(self.path, lesson_name, "file",
                                     real_filename + extension)
                self.fm.downloadto(fpath, fs, real_filename + extension)
                self.save_file_id(fid, fpath)

    def download_homework(self, lesson_id, lesson_name, download_submission):
        ddls = []
        for api in settings.homeworks_url(lesson_id):
            for hw in self.jh.loads(self.get(api))["object"]["aaData"]:
                content = self.get(settings.homework_url(lesson_id, hw))
                hw_title, hw_readme = self.soup.parse_homework(content, hw)
                ddls.append((lesson_name, hw_title, hw["jzsjStr"], hw["wjmc"] +
                             "   "+utils.size_format(int(hw["wjdx"])) if
                             hw["wjmc"] is not None else hw["zynrStr"] if
                             hw["zynrStr"] != "" else hw["zt"]))

                hw_dir = os.path.join(self.path, lesson_name, "homework",
                                      utils.escape_str(hw_title))
                self.fm.init_homework(hw, hw_dir, hw_title, hw_readme)

                # download annexes and images
                annex_attrs, img_urls = self.soup.parse_annex(content)
                for i, attr in enumerate(annex_attrs):
                    if i == 2 and not download_submission:
                        break
                    annex_name, download_url, annex_id = attr
                    annex_prefix = "answer_" if i == 1 else \
                        "reviewed_" if i == 3 else ""
                    if (annex_name != "NONE" and
                            not self.file_id_exist(annex_id)):
                        annex = self.session.get(download_url, stream=True)
                        fpath = os.path.join(hw_dir, annex_prefix+annex_name)
                        self.fm.downloadto(fpath, annex, annex_name)
                        self.save_file_id(annex_id, fpath)
                img_names = []
                for i, img_url in enumerate(img_urls):
                    img = self.session.get(img_url, stream=True)
                    img_name = f'''{i+1}_{img.headers.get(
                        'content-disposition').split(
                        'filename=')[1].strip('"')}'''
                    if img.content[:8] == b'\x89PNG\x0d\x0a\x1a\x0a':
                        img_name = os.path.splitext(img_name)[0] + ".png"
                    fpath = os.path.join(hw_dir, img_name)
                    self.fm.downloadto(fpath, img, img_name, quiet=True)
                    img_names.append(img_name)

                # add images to README.md
                if img_names:
                    readme_path = os.path.join(hw_dir, "README.md")
                    with open(readme_path, "r") as f:
                        content = f.readlines()
                    for i, line in enumerate(content):
                        if line.strip() in ["#### Description", "#### 作业说明"]:
                            insert_index = i + 1
                            break
                    for img_name in reversed(img_names):
                        content.insert(insert_index, f"![]({img_name})\n")
                    with open(readme_path, "w") as file:
                        file.writelines(content)
        return ddls

    def upload(self, homework_id, file_path, message):
        form = settings.upload_form(homework_id, file_path, message)
        response = self.jh.loads(self.post(settings.upload_api, form=form,
                                 headers=settings.upload_headers))
        if response["result"] == "success":
            print("done")
        else:
            print(f"Error: assignment may have expired. Details:\n{response}")

    def get_ddl(self, lessons, download_submission=False):
        ddls = []
        for lesson in lessons:
            ddls += self.download_homework(
                lesson[0], lesson[4], download_submission)
        # delete expired homework by comparing ddl[2] with current time
        ddls = [ddl for ddl in ddls if not utils.expired(ddl[2])]
        ddls.sort(key=lambda x: x[2])
        return [[ddl[0], ddl[1], ddl[2], utils.time_delta(ddl[2]), ddl[3]]
                for ddl in ddls]


def main():
    pass


if __name__ == "__main__":
    main()
