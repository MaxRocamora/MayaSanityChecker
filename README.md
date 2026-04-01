Maya Sanity Checker
-------------------

![preview](https://github.com/MaxRocamora/MayaSanityChecker/blob/master/sanityChecker/resources/images/tool_img.png)

# Description
This tool aims to check the sanity of the scene in Maya.  
It checks for common issues that can cause problems in the scene.  
The checks are divided into categories and groups, each category can have multiple checks.  
The checks can be added or removed from the configuration file, same for categories.  
**The best use case for this tool is to check the scene before publishing or sharing it with others.**  
**Note:** Most of the checks are configured to my day to day needs, but you can edit the checks as per your requirements.

## Install (Maya 2018/2019/2022/2024/2025/2026)

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

- Arnold Texture Memory Limit
- AOV in Scene
- Atmosphere Nodes
- Custom User View on scene
- DisplayLayers
- Empty Namespace
- Existing Namespace
- Legacy RenderLayers
- Multiple Arcane ContextNode
- Visible View Nodes on scene

## NODES Group

- blindDataTemplate Node
- Unconnected createColorSet Nodes
- GroupID Nodes
- Scene Total Nodes: Limit of 2000
- Model Orphan Nodes
- Scene Orphan Nodes
- Unconnected Nodes
- Unknown Nodes
- XGen Nodes in Scene

## MESHES Group

- Animation Curves on meshes
- Empty UVSet on Mesh
- Hidden Faces or defaultHideFaceDataSet Node
- History on Mesh
- LaminaFaces
- Mesh missing map1 UVSet
- Display Smoothness Enabled
- Multiple Shapes on the same Transform Node
- Multiple UV Sets on meshes
- No Shading Group on mesh
- Non Manifold Geometry
- Non Zero Pivot on Mesh
- Non Zero Transforms
- NGonSide Polygon on Mesh
- Arnold Max Subdivisions Iterations
- Visibility Off

## NAMING Group

- Duplicate Names
- Invalid Shape Names
- Invalid StandIn Shape Names
- Meshes Names ending with numbers
- Meshes with invalid pipeline suffixes.

## MAPS Group

- Alpha Luminance Attribute
- ignoreColorSpaceFileRules Attribute Enabled
- Files Colorspaces
- Auto Generate Tx Attribute
- Texture File with old colorspace
- HDRI ColorSpace
- Arnold MipmapBias Attribute at 0
- Missing Filemaps
- Missing TX Filemaps


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

## Changelog (v4.4.0)

- Fixed viewport smooth autofix execution.
- Fixed right-click context menu crash when no tree item is selected.
- Fixed logger handler cleanup when closing the UI.
- Fixed severity color mapping for check level progress bar.
- Fixed scene config typo for viewport smooth check key.
- Improved dynamic check loading with safer error handling.
- Added startup self-check logs (loaded checks, unresolved config entries, shared checks).
- Standardized autofix methods to use explicit flagged node names.
- Replaced legacy `%s`/`.format(...)` string formatting with f-strings.

## Note

On version 5.0.0 I will drop support for PySide2 and Maya 2018/2019, so the minimum requirements will be Maya 2025 and PySide6.