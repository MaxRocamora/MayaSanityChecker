# ----------------------------------------------------------------------------------------
# check for invalid pipeline suffixes (skips namespaces nodes)
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

SUFFIXES = ['_MSH', '_SMS', '_NDM', '_SPL', '_SKN', '_PRX']

name = 'Meshes with invalid pipeline suffixes.'
group = CategoryGroups.NAMING
description = 'Mesh not ending with valid pipeline suffix.'
level = SeverityLevels.HIGH
autofix = False
hint = f'Rename flagged meshes with valid ending suffixes \n {SUFFIXES}'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in get_scene_mesh_transform_nodes():
            if node[-4:].upper() not in SUFFIXES:
                self.add_failed_node(node)
