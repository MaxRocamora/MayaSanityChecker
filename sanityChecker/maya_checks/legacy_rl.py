# ----------------------------------------------------------------------------------------
# check for maya legacy renderlayers
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Legacy RenderLayers'
group = CategoryGroups.SCENE
description = 'Delete all Legacy Render Layers.'
level = SeverityLevels.CRITICAL
autofix = True
hint = 'On RenderSetup>Options, set show legacy renderlayers in outliner and delete them'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in self.get_renderlayers():
            self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            try:
                cmds.delete(node)
            except RuntimeError as e:
                log.error(str(e))

    def get_renderlayers(self) -> list:
        """Collects renderlayer nodes from maya scene."""
        nodes = cmds.ls(type='renderLayer')
        nodes[:] = [n for n in nodes if n != 'defaultRenderLayer']
        nodes[:] = [n for n in nodes if ':' not in n]
        nodes[:] = [n for n in nodes if not n.startswith('rs_')]

        return nodes
