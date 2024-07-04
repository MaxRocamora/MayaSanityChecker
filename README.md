Maya Sanity Checker
===================

![preview](https://github.com/MaxRocamora/SanityChecker/blob/master/sanityChecker/ui/images/tool_img.png)

Description
-----------

+ Performs sanity checks for maya scenes from a customizable library of checks.
+ Checks are organized into Categories and Groups.
+ Custom Checks can be created by subclassing 'check.py' file and saved into /checks folder.
+ Categories & Groups can be customized from config.py file.

Install
-------

Copy 'sanityChecker' folder into users/maya scripts folder
or to any directory and add this path to your PYTHONPATH environment variable.

Create a shelf button with this python command:

```python

import sanityChecker.main as sanity_checker
sanity_checker.load_sanity()

```

Tested on:
Maya 2018, 2019, 2022
Python 3 Required.
