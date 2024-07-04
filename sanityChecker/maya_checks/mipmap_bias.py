# ----------------------------------------------------------------------------------------
# mipmap bias -2 for bump, normalBump
# only on displace connected filenodes (aiMipBias)
# Connected to displace
# Connected to geometry / bump mapping
#
# Now checks for 0, -2 is too high for render times.
#
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

NODE = 'file'
ATTRIBUTES = 'aiMipBias'
VALUE = 0
IGNORE_NODES = [
    'nodeGraphEditorInfo',
    'shadingEngine',
    'defaultColorMgtGlobals',
    'colorManagementGlobals',
    'defaultRenderUtilityList',
    'defaultShaderList',
    'defaultTextureList',
]
CONNECTIONS = ['bump2d', 'displacementShader']

name = 'Arnold MipmapBias Attribute at 0'
group = CategoryGroups.MAPS
description = f'Filenode mip-map bias value must be {VALUE}'
level = SeverityLevels.MODERATE
autofix = True
hint = f'Set your filenodes {ATTRIBUTES} attribute to {VALUE}'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in self.get_mipmap_filenodes():
            if cmds.getAttr(f'{node}.{ATTRIBUTES}') != VALUE:
                self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            att = f'{node}.{ATTRIBUTES}'
            if cmds.getAttr(att) != VALUE:
                cmds.setAttr(att, VALUE)

    def get_mipmap_filenodes(self) -> list:
        """Collect nodes to scan from maya scene."""
        nodes = []

        for n in cmds.ls(type=NODE):
            connections = cmds.listConnections(n, source=0, destination=1, plugs=1)
            if not connections:
                continue
            connections = {c for c in connections if c not in IGNORE_NODES}
            connected_nodes = [n for c in connections if cmds.nodeType(c) in CONNECTIONS]
            nodes.extend(connected_nodes)

        return nodes
