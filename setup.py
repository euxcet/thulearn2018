import setuptools
import os
from pathlib import Path
from setuptools.command.install import install


class CustomInstall(install):
    def run(self):
        install.run(self)
        if (os.name == 'nt'):
            config_dir = os.path.join(
                os.environ.get("APPDATA"), "thulearn2018")
        elif (os.name == 'posix'):
            config_dir = os.path.join(
                os.environ.get("XDG_CONFIG_HOME",
                               os.path.expanduser("~/.config")),
                "thulearn2018")
        else:
            config_dir = Path.home()
        if (not os.path.exists(config_dir)):
            os.makedirs(config_dir)
            for file_name in ["user.txt", "local.txt", "path.txt"]:
                old_file_path = os.path.join(Path.home(),
                                             ".thulearn2018-"+file_name)
                if (os.path.exists(old_file_path)):
                    os.rename(old_file_path,
                              os.path.join(config_dir, file_name))
        with open(os.path.join(config_dir, "openssl.conf"), 'w') as f:
            f.write("openssl_conf = openssl_init\n\n"
                    "[openssl_init]\n"
                    "ssl_conf = ssl_sect\n\n"
                    "[ssl_sect]\n"
                    "system_default = system_default_sect\n\n"
                    "[system_default_sect]\n"
                    "Options = UnsafeLegacyRenegotiation\n")


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thulearn2018",
    version="2.4.3",
    author="Chengchi Zhou, Yingtian Liu, Yurui Hong",
    author_email="zcc16@mails.tsinghua.edu.cn, liu-yt16@mails.tsinghua.edu.cn,"
                 "yuruihong02@outlook.com",
    description="Tools for Web Learning of Tsinghua University",
    long_description="Tools for Web Learning of Tsinghua University",
    long_description_content_type="text/markdown",
    url="https://github.com/euxcet/thulearn2018",
    packages=setuptools.find_packages(),
        install_requires=['requests>=2.18.4', 'bs4>=0.0.1',
                          'beautifulsoup4>=4.6.0', 'requests_toolbelt',
                          'click>=7.0'],
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
    cmdclass={
        'install': CustomInstall,
    }
)
