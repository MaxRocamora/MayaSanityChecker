# ----------------------------------------------------------------------------------------
# check for maya NSided polygons in meshes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds
import maya.mel as mel

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_mesh_transform_nodes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'NGonSide Polygon on Mesh'
group = CategoryGroups.MESHES
description = 'Mesh has NSide polygons'
level = SeverityLevels.LOW
autofix = False
hint = 'Rework your model topology to avoid polygons with 5 or more sides'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in get_scene_mesh_transform_nodes():
            node_long_name = cmds.ls(node, long=1)
            cmds.select(node_long_name, r=True)

            mel.eval('changeSelectMode -component;')
            mel.eval('selectType -smp 0 -sme 1 -smf 0 -smu 0 -pv 0 -pe 1 -pf 0 -puv 0;')
            mel.eval('polySelectConstraint -mode 3 -type 0x0008 -size 3;')
            mel.eval('polySelectConstraint -disable;')

            polys = cmds.polyEvaluate(faceComponent=True)

            cmds.select(clear=True)
            if not isinstance(polys, int):
                continue

            if polys > 0:
                self.add_failed_node(node)

            mel.eval('changeSelectMode -object;')
            cmds.select(clear=True)
