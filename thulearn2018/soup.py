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
        title = ["作业内容及要求：", "本人提交的作业："]
        subtitle = ["作业标题", "作业说明", "作业附件", "答案说明", "答案附件",
                    "发布对象", "完成方式", "学号", "提交日期", "截止日期",
                    "上交作业内容", "上交作业附件"]
        title_en = ["Contents and Requirements:：", "My coursework submitted："]
        subtitle_en = ["Title", "Description", "Attach.", "ANS", "Content",
                       "Assign to", "INDV/GRP", "Student No.", "Date",
                       "Deadline", "Content"]
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
        return line + "\n"

    def to_markdown(self, txt):
        txts = [self.markdown_add_title(line.strip()) for line in txt]
        return "".join(txts)

    def parse_homework(self, content, ddl):
        soup = BeautifulSoup(content, "html.parser")
        boxbox = soup.find_all('div', class_="boxbox")
        hw_title = boxbox[0].find_all(
            'div', class_="right")[0].get_text().strip()
        ddl_title = "截止日期" if boxbox[0].find_all(
            'div', class_="ttee")[0].get_text() == "作业内容及要求：" else "Deadline"
        txt = boxbox[0].get_text().replace('\t', '').split('\n') + \
            [ddl_title] + [ddl] + \
            boxbox[1].get_text().replace('\t', '').split('\n')
        hw_readme = self.to_markdown(txt)
        return (hw_title, hw_readme)

    def parse_annex(self, content):
        soup = BeautifulSoup(content, "html.parser")
        annex_urls = [a.find_all('a') for a in soup.find_all(
            'div', class_='list fujian clearfix')]
        results = []
        for annex_url in annex_urls:
            result = ["NONE", "NONE", "NONE"]  # name, download url, id
            if len(annex_url) > 0:
                result[0] = annex_url[0].get_text().strip()
                result[1] = settings.url+annex_url[1].get('href')
                result[2] = annex_url[1].get('href').split('/')[-1]
            results.append(result)
        return results
