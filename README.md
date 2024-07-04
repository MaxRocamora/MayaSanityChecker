Maya Sanity Checker
-------------------

![preview](https://github.com/MaxRocamora/SanityChecker/blob/master/sanityChecker/resources/images/tool_img.png)

# Description
This tool aims to check the sanity of the scene in Maya.  
It checks for common issues that can cause problems in the scene.  
The checks are divided into categories and groups, each category can have multiple checks.  
The checks can be added or removed from the configuration file, same for categories.  
**The best use case for this tool is to check the scene before publishing or sharing it with others.**  
**Note:** Most of the checks are configured to my day to day needs, but you can edit the checks as per your requirements.


## Install (Maya 2018/2019/2022)

copy 'sanityChecker' folder into users/maya scripts folder

+ Run Python Command
```python
    import sanityChecker.main as SanityChecker
    SanityChecker.load()
```

---

# Checks
This section will list all the checks that are currently available in the sanity checker.
The checks are divided into categories and groups, each category can have multiple checks.
Some checks have an automatic fix, which can be applied by right clicking on the check.
I recommend editing the checks as per your requirements.

### *(Checks Documentation still in progress)*

## SCENE Group

- Arnold Atmosphere Nodes in Scene
- Arnold AOV Nodes in Scene
- Custom User Views on the Scene
- Display Layers in Scene
- Empty Namespaces in Scene
- Existing Namespaces in Scene
- Legacy Render Layers in Scene
- Default Views Visible in Scene

## NODES Group

- blindDataTemplate Nodes in Scene
- Unconnected Color Sets Nodes in Scene
- GroupID Nodes in Scene
- Total Scene nodes exceeds limit
- Unknown Nodes in Scene
- XGen Nodes in Scene

## MESHES Group

- Animation Curves on Meshes
- Empty UV Sets on Meshes
- Arnold Max Subdivision Limit
- Arnold Texture Max Memory
- Lamina Faces on Meshes

## NAMING Group

- Duplicate Names in Scene
- Naming Convention for Mesh Suffix

## MAPS Group

- alphaIsLuminance on maps
- ignoreColorSpaceFileRules disabled on maps
- valid Colorspace value on maps
- aiAutoTx enabled on maps.
- old Colorspace value on maps

# Configuration

To add or remove checks, you can edit the `sanityChecker/config/config.py` file.
Just add or remove the name of the check from the `CHECKS` list from the Category.
Custom Categories can be created just by editing this dictionary.

# UI

# Custom Checks

1. Create a new python file in the `sanityChecker/checks` folder.
2. Create a new class that inherits from `sanityChecker.libs.check`.
3. Set the required variables in the class.
4. Implement the `run` method in the class.
5. Implement the `fix` method in the class if can have autofix.
6. Add the check to the configuration file.