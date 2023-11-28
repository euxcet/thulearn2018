# Thu Learn 2018

Tools for Web Learning of Tsinghua University.

<details>
<summary>2023.11.28 Fix UNSAFE_LEGACY_RENEGOTIATION_DISABLED error</summary>

It has been confirmed on some Linux distros that the depreciation of legacy unsafe renegotiation in OpenSSL causes UNSAFE_LEGACY_RENEGOTIATION_DISABLED error. By refering to https://stackoverflow.com/questions/71603314/ssl-error-unsafe-legacy-renegotiation-disabled, the project has provided a custom `openssl.conf` to help address the connectivity issue.

Just set the `OPENSSL_CONFIG` variable when executing `learn` commands:

```bash
OPENSSL_CONF="$HOME/.config/thulearn2018/openssl.conf" learn ...
```

or if you have a custom `XDG_CONFIG_HOME`:

```bash
OPENSSL_CONF="$XDG_CONFIG_HOME/thulearn2018/openssl.conf" learn ...
```

You can also alias `learn` to `OPENSSL_CONF="$HOME/.config/thulearn2018/openssl.conf" learn` to achieve drop-in solution.

**Warning**: When enabling Legacy Unsafe Renegotiation, SSL connections will be vulnerable to the Man-in-the-Middle prefix attack as described in [CVE-2009-3555](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CAN-2009-3555). Use this at your own risk and it is not recommened to `export` the variable shell-wide.

</details>


## Get Started
```bash
pip install thulearn2018
```

Or install the lastest version from GitHub:

```bash
pip install git+https://github.com/euxcet/thulearn2018.git
```

## User Guide

After installing the package, you will get the command `learn` . Check this by running 

```bash
learn --help
```

This will show all the subcommands you can use basically, including downloading all the new files, listing the deadlines and submitting your work.

### Login Authentication

For login authentication, please run 

```bash
learn reset
```

to set or reset your personal configuration, including the username/password for web learning and the absolute path where you want to save your courses in the **current semester**. If you'd like to download from past semesters, always remember to customize the target directory unless the default one is preferred.

**Notice: The username/password is saved to a local file in your temp directory, depending on your OS and won't be uploaded to anywhere online except the web learning.**

Anytime you want to check the config, just run 

```bash
learn config
```

### Functional Commands

Now you could 

- download all the new files and assignments along with the attachments by

  ```bash
  learn download [-e | --exclude "<course_name1>[,<course_name2>, ...]"]
                 [-i | --include "<course_name1>[,<course_name2>, ...]"]
                 [-s | --semester <semester>]
                 [-o | --path <path>]
                 [--download-submission]
  ```
  
	This command will also create subdirectories for all the courses automatically.
  
  - `[-e | --exclude ]`: Courses to be excluded, separated by `,`, default to none. (Do not add space between `,` and the course name, as course names may contain space)
  - `[-i | --include ]`: Courses to be included, separated by `,`, default to all.
  - `[-s | --semester ]`: The semester to download, default to the current one.
  - `[-o | --path ]`: The path to save the files, default to the one in the config.
  - `[--download-submission]`: Whether to download the submissions of assignments, default to `False`, as it will cover the original work. (**Most likely a newer one!**). Designed to download from past semesters, when you don't have a copy of your assignments locally.

There are 4 possible annexes for an assignment, including 1. the requirement, 2. the answer, 3. your submission and 4. reviewed submission. As we cannot control how the teacher names the files, prefixes `answer_` and `reviewed_` will be added to relevant files to avoid clashes.

- list the deadlines sorted by time

  ```bash
  learn ddl [-e | --exclude "<course_name1>[,<course_name2>, ...]"]
            [-i | --include "<course_name1>[,<course_name2>, ...]"]
            [-s | --semester <semester>]
  ```
  

- submit your assignment and the text message with 

  ```bash
  learn submit /path/to/your/assignment [-m "<message>"]
  ```

  **Notice: This command must be excuted at the assignment directory where a file named `.xszyid` exists.**
  If you do not want to upload any text/file, just omit the `-m` option/the parameter following `submit`. 

- clear all the record of your course files and assignments for a semester, default to the current one.

  ```bash
  learn clear [--semester <semester>]
  ```

  This command will **not** delete the existing files. It means the next time you try to download course files, all the files will be redownloaded, no matter whether you have downloaded them. 

### Interrupted Download

You can interrupt the download process of any certain file to skip it by pressing `Ctrl + C`. This skip will be recorded and the next time you try to download the files, the skipped files will not be downloaded again. Used to skip large files like recordings and should be used with caution.

## Feel free to contribute yourself

:heavy_check_mark: Use this package

:heavy_check_mark: Report any bug

:heavy_check_mark: ​Come up with any new idea or feature

:heavy_check_mark: Create your pull request to this repository
