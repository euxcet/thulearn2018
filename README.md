# Thu Learn 2018

Tools for Web Learning of Tsinghua University.

## Get Started
```
pip install thulearn2018
```

## User Guide

After installing the package, you will get the command `learn` . Check this by running 

```
learn --help
```

This will show all the subcommands you can use basically, including downloading all the new files, listing the deadlines and submitting your homework.

For login authentication, please run 

```
learn reset
```

to set or reset your personal configuration, such as the username/password for web learning and the absolute path where you want to save your course directories. **Notice: The username/password is saved to a local file in your temp directory, depending on your OS and won't be uploaded to anywhere online except the web learning.** You could reset the configuration  by rerun the command. Anytime you want to check the config, just run 

```
learn config
```

Now you could 

- download all the new files and homeworks along with the attachments by

  ```
  learn download
  ```
  
	This command will also create subdirectories for all the courses automatically. 

- list the deadlines sorted by time

  ```
  learn ddl
  ```

- submit your homework and the text message with 

  ```
  learn submit /path/to/your/homework/file -m "the text message you want to submit."
  ```

  **Notice: This command must be excuted at the homework directory where a file named `.xszyid` exists.**

- clear all the record of your course files and homeworks

  ```
  learn clear
  ```

  This command will **not** delete the exist files. It means the next time you try to download course files, all the files will be redownloaded, no matter whether you have downloaded them. 



## Feel free to contribute yourself

:heavy_check_mark: Use this package

:heavy_check_mark: Report any bug

:heavy_check_mark: ​Come up with any new idea or feature

:heavy_check_mark: Create your pull request to this repository

