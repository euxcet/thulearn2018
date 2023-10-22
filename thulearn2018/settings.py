import os
from pathlib import Path

from requests_toolbelt.multipart.encoder import MultipartEncoder

headers = {
    'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; '
    'Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/56.0.2924.87 Mobile Safari/537.36'}
upload_headers = {
    'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; '
    'Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/56.0.2924.87 Mobile Safari/537.36',
    'Content-Type': 'multipart/form-data; '
                    'boundary=----WebKitFormBoundaryTytyPd5kgvE3t0kW'}

url = "https://learn.tsinghua.edu.cn/"

user_file_name = 'user.txt'
local_file_name = 'local.txt'
path_file_name = 'path.txt'

if (os.name == 'nt'):
    temp_path = os.path.join(os.environ.get("APPDATA"), "thulearn2018")
elif (os.name == 'posix'):
    temp_path = os.path.join(os.environ.get(
        "XDG_CONFIG_HOME", os.path.expanduser("~/.config")), "thulearn2018")
else:
    temp_path = Path.home()

if (not os.path.exists(temp_path)):
    os.makedirs(temp_path)
    for file_name in [user_file_name, local_file_name, path_file_name]:
        old_file_path = os.path.join(Path.home(), ".thulearn2018-"+file_name)
        if (os.path.exists(old_file_path)):
            os.rename(old_file_path, os.path.join(temp_path, file_name))

user_file_path = os.path.join(temp_path, user_file_name)
local_file_path = os.path.join(temp_path, local_file_name)
path_file_path = os.path.join(temp_path, path_file_name)

login_id_url = "https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/" + \
"bb5df85216504820be7bba2b0ae1535b/0?/login.do"
login_url = url + "b/j_spring_security_thauth_roaming_entry"
semester_url = url + "b/kc/zhjw_v_code_xnxq/getCurrentAndNextSemester"
files_url = url + "b/wlxt/kj/wlkc_kjflb/student/pageList"
upload_api = url + 'b/wlxt/kczy/zy/student/tjzy'


def file_url(lesson_id, file_id):
    return url+"b/wlxt/kj/wlkc_kjxxb/student/kjxxb/"+lesson_id+"/"+file_id


def lessons_url(semester):
    return url+"b/wlxt/kc/v_wlkc_xs_xkb_kcb_extend/student/" + \
    "loadCourseBySemesterId/"+semester+"/en"


def download_before_url(fid):
    return url+"b/kc/wj_wjb/downloadFileBefore?wjid="+fid


def download_url(fid):
    return url+"b/wlxt/kj/wlkc_kjxxb/student/downloadFile?sfgk=0&wjid="+fid


def homeworks_url(lesson_id): # add "Ypg" if needed
    form = "aoData=[{\"name\":\"wlkcid\",\"value\":\""+lesson_id+"\"}]"
    types = ["Yjwg", "Wj", "Ypg"]
    return [url+"b/wlxt/kczy/zy/student/zyList"+x+"?"+form for x in types]


def homework_url(lesson_id, hw):
    return url+"f/wlxt/kczy/zy/student/viewTj?wlkcid="+lesson_id + \
        "&sfgq=0&zyid="+hw["zyid"]+"&xszyid="+hw["xszyid"]


def upload_form(homework_id, file_path, message):
    if (file_path == ''):
        return MultipartEncoder(
            fields={
                'xszyid': homework_id,
                'isDeleted': '1',
                'zynr': message
            },
            boundary='----WebKitFormBoundaryTytyPd5kgvE3t0kW'
        )
    else:
        return MultipartEncoder(
            fields={
                'fileupload': (os.path.basename(file_path),
                               open(file_path, 'rb'),
                               'application/octet-stream'),
                'xszyid': homework_id,
                'isDeleted': '0',
                'zynr': message
            },
            boundary='----WebKitFormBoundaryTytyPd5kgvE3t0kW'
        )
