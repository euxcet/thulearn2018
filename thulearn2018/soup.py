from bs4 import BeautifulSoup

from . import settings


class Soup():
    def __init__(self):
        pass

    def parse_ticket(self, content):
        soup = BeautifulSoup(content, "html.parser")
        ticket = ""
        for a in soup.find_all('a'):
            h = a.get('href')
            if (h[0:4] == "http"):
                ticket = h[-59:]
        return ticket

    def markdown_add_title(self, line):
        title = ["作业内容及要求：", "本人提交的作业：", "老师批阅结果："]
        subtitle = ["作业标题", "作业说明", "作业附件", "答案说明", "答案附件",
                    "发布对象", "完成方式", "学号", "提交日期", "截止日期",
                    "上交作业内容", "上交作业附件", "批阅老师", "批阅时间",
                    "成绩", "评语", "评语附件"]
        title_en = ["Contents and Requirements:：", "My coursework submitted：",
                    "Instructors' comments"]
        subtitle_en = ["Title", "Description", "Attach.", "ANS", "Content",
                       "Assign to", "INDV/GRP", "Student No.", "Date",
                       "Deadline", "Content", "By", "Grading Time", "Grade",
                       "Comment"]
        if len(line) == 0:
            return ""
        if (line in subtitle or line in subtitle_en):
            return "#### " + line + "\n"
        if (line in title):
            return "### " + line + "\n"
        if line == title_en[0]:
            return "### " + line[:-2] + "\n"
        if line == title_en[1]:
            return "### " + line[:-1] + "\n"
        if line == title_en[2]:
            return "### " + line + "\n"
        return line + "\n"

    def to_markdown(self, txt):
        txts = [self.markdown_add_title(line.strip()) for line in txt]
        return "".join(txts)

    def parse_homework(self, content, hw):
        soup = BeautifulSoup(content, "html.parser")
        boxbox = soup.find_all('div', class_="boxbox")
        hw_title = boxbox[0].find_all(
            'div', class_="right")[0].get_text().strip()
        is_zh = boxbox[0].find_all(
            'div', class_="ttee")[0].get_text() == "作业内容及要求："
        (ddl_title, instructor_name_title, grading_time_title, grade_title,
            grading_content_title, graded_file_title) = ("截止日期", "批阅老师",
            "批阅时间", "成绩", "评语", "评语附件") if is_zh else (
            "Deadline", "By", "Grading Time", "Grade", "Comment", "Attach.")
        txt = boxbox[0].get_text().replace('\t', '').split('\n') + \
            [ddl_title] + [str(hw["jzsjStr"])] + \
            boxbox[1].get_text().replace('\t', '').split('\n') + \
            ["老师批阅结果：" if is_zh else "Instructors' comments"] + \
            [instructor_name_title] + [str(hw["jsm"])] + \
            [grading_time_title] + [str(hw["pysjStr"])] + \
            [grade_title] + [str(hw["cj"])] + \
            [grading_content_title] + [str(hw["pynr"])] + \
            [graded_file_title] + [str(hw["wjmc"])]
        hw_readme = self.to_markdown(txt)
        return (hw_title, hw_readme)

    def parse_annex(self, content):
        soup = BeautifulSoup(content, "html.parser")
        annexes = [a.find_all('a') for a in soup.find_all(
            'div', class_='list fujian clearfix')]
        calendat_tag = soup.find('div', class_='list calendar clearfix')
        img_urls = [img['src'] for img in calendat_tag.find_all('img')] \
            if calendat_tag else []
        annex_attrs = []
        for annex in annexes:
            attr = ["NONE", "NONE", "NONE"]  # name, download url, id
            if len(annex) > 0:
                attr[0] = annex[0].get_text().strip()
                attr[1] = settings.url+annex[1].get('href')
                attr[2] = annex[1].get('href').split('/')[-1]
            annex_attrs.append(attr)
        return annex_attrs, img_urls