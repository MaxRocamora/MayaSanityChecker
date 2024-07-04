# ----------------------------------------------------------------------------------------
# Maximiliano Rocamora / maxirocamora@gmail.com
#
# 05/2019 v2.0.1 added version
# 07/2019 v2.1.6 used qtStandardTool class, log system, errorCount
# 07/2019 v2.1.7 added HiddenFaceDataCheck
# 09/2019 v2.1.8 added AtmosphereNodesCheck
# 04/2020 v3.0.0 made maya standalone version / check refactor / config.ini
# 08/2020 v3.1.0 reworked ui, more compact
# 08/2020 v3.1.1 refactor interface controller, drop-shadow Icons
# 08/2020 v3.1.2 remove version menu and close button
# 11/2020 v3.1.5 refactor buttons to qt button subclass
# 01/2021 v3.1.6 removed menu bar
# 08/2021 v3.1.7 added xGen and model_orphan_nodes checks
# 08/2021 v3.1.8 some refactor and fixes
# 08/2021 v3.2.0 new Icons and refactor Icons
# 08/2021 v4.0.0 new design and modules
# 08/2021 v4.0.1 qTree module, run category button callback
# 10/2021 v4.0.2 one bug fix, new texture ram limit check, improved alpha luminance check
# 11/2021 v4.1.0 Python3 UI migration
# 01/2022 v4.1.1 added skip namespaces items on some checks ':'
# 02/2022 v4.1.2 refactor and cleaned Icons
# 03/2022 v4.1.3 added new check for context_node, refactor groups to enum
# ----------------------------------------------------------------------------------------
import os

VERSION_MAJOR = 4
VERSION_MINOR = 1
VERSION_PATCH = 3

version = f'{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}'

app_name = 'Sanity Checker'
__qt__ = 'Arcane2:Qt_' + app_name + '_ui'
ui_file = os.path.join(os.path.dirname(__file__), 'resources', 'ui', 'main.ui')
