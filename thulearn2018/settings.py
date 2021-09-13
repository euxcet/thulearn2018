import tempfile, os
from pathlib import Path
from urllib3 import encode_multipart_formdata
from requests_toolbelt.multipart.encoder import MultipartEncoder

headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36' }
upload_headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
 		'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundaryTytyPd5kgvE3t0kW'}

# url = "http://learn2018.tsinghua.edu.cn/"
url = "http://learn.tsinghua.edu.cn/"

user_file_name = '.thulearn2018-user.txt'
local_file_name = '.thulearn2018-local.txt'
path_file_name = '.thulearn2018-path.txt'
temp_path = str(Path.home())
#temp_path = tempfile.gettempdir()
user_file_path = temp_path + os.sep + user_file_name
local_file_path = temp_path + os.sep + local_file_name
path_file_path = temp_path + os.sep + path_file_name

login_id_url = "https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/bb5df85216504820be7bba2b0ae1535b/0?/login.do"
login_url = url + "b/j_spring_security_thauth_roaming_entry"
semester_url = url + "b/kc/zhjw_v_code_xnxq/getCurrentAndNextSemester"
files_url = url + "b/wlxt/kj/wlkc_kjflb/student/pageList"
upload_api = url + 'b/wlxt/kczy/zy/student/tjzy'


def file_url(lesson_id, file_id):
    return url + "b/wlxt/kj/wlkc_kjxxb/student/kjxxb/" + lesson_id + "/" + file_id

def lessons_url(semester):
    return url + "/b/wlxt/kc/v_wlkc_xs_xkb_kcb_extend/student/loadCourseBySemesterId/" + semester

def download_before_url(fid):
    return url + "b/kc/wj_wjb/downloadFileBefore?wjid=" + fid

def download_url(fid):
    return url + "b/wlxt/kj/wlkc_kjxxb/student/downloadFile?sfgk=0&wjid=" + fid

def homeworks_url(lesson_id):
	form = "aoData=[{\"name\":\"wlkcid\",\"value\":\"" + lesson_id + "\"}]"
	return [ url + "b/wlxt/kczy/zy/student/zyListYjwg?" + form, \
             url + "b/wlxt/kczy/zy/student/zyListWj?" + form]

def homework_url(lesson_id, hw):
    return url + "f/wlxt/kczy/zy/student/viewTj?wlkcid=" + lesson_id + "&sfgq=0&zyid=" + hw["zyid"] + "&xszyid=" + hw["xszyid"]

def upload_form(homework_id, file_path, message):
    if (file_path == '.' + os.sep):
        return MultipartEncoder(
            fields = {
                'xszyid' : homework_id,
                'isDeleted' : '1',
                'zynr': message
            },
            boundary = '----WebKitFormBoundaryTytyPd5kgvE3t0kW'
        )
    else:
        return MultipartEncoder(
            fields = {
                'fileupload' :(os.path.basename(file_path), open(file_path, 'rb'), 'application/octet-stream'),
                'xszyid' : homework_id,
                'isDeleted' : '0',
                'zynr': message
            },
            boundary = '----WebKitFormBoundaryTytyPd5kgvE3t0kW'
        )
