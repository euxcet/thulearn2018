import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thulearn2018",
    version="1.0.2",
    author="Chengchi Zhou",
    author_email="zcc16@mails.tsinghua.edu.cn",
    description="Tools for Web Learning of Tsinghua University",
    long_description="Tools for Web Learning of Tsinghua University",
    long_description_content_type="text/markdown",
    url="https://github.com/euxcet/thulearn2018",
    packages=setuptools.find_packages(),
	install_requires=['requests>=2.18.4', 'bs4>=0.0.1', 'beautifulsoup4>=4.6.0'],
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
