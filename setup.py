import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thulearn2018",
    version="2.3.4",
    author="Chengchi Zhou, Yingtian Liu, Yurui Hong",
    author_email="zcc16@mails.tsinghua.edu.cn, liu-yt16@mails.tsinghua.edu.cn, yuruihong02@outlook.com",
    description="Tools for Web Learning of Tsinghua University",
    long_description="Tools for Web Learning of Tsinghua University",
    long_description_content_type="text/markdown",
    url="https://github.com/euxcet/thulearn2018",
    packages=setuptools.find_packages(),
	install_requires=['requests>=2.18.4', 'bs4>=0.0.1', 'beautifulsoup4>=4.6.0', 'requests_toolbelt', 'click>=7.0'],
	entry_points={
        'console_scripts': [
            'learn = thulearn2018.learn:main',
            ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
