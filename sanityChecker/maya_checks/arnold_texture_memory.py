# ----------------------------------------------------------------------------------------
# Checks for low value on Arnold Texture Memory Limit
# ----------------------------------------------------------------------------------------
import contextlib
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

ATTRIBUTE = 'defaultArnoldRenderOptions.textureMaxMemoryMB'
VALUE = 16384
name = 'Arnold Texture Memory Limit'
group = CategoryGroups.SCENE
description = 'Low value on Arnold Textures Memory Limit.'
level = SeverityLevels.HIGH
autofix = True
hint = f'Set value of memory limit to: {VALUE}'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        with contextlib.suppress(ValueError):
            if int(cmds.getAttr(ATTRIBUTE)) < VALUE:
                self.add_failed_node('defaultArnoldRenderOptions.textureMaxMemoryMB')

    def fix(self):
        """Perform technical fix on this check."""
        cmds.setAttr(ATTRIBUTE, VALUE)
