# ----------------------------------------------------------------------------------------
# check for invalid shape names in meshes
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.maya.helpers import get_scene_shapes
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Invalid Shape Names'
group = CategoryGroups.NAMING
description = 'Shape Name mismatch mesh name'
level = SeverityLevels.CRITICAL
autofix = True
hint = 'Rename your shapes to [MeshNameShape]'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in get_scene_shapes():
            old_shape_name = cmds.listRelatives(node, pa=True, type='shape')[0]
            # taking shortname from fullpath
            old_shape_name = old_shape_name.split('|')[-1]

            try:
                new_shape_name = f'{str(node[1:])}Shape'
                # taking shortname from fullpath
                new_shape_name = new_shape_name.split('|')[-1]
            except UnicodeEncodeError:
                new_shape_name = '####'

            if old_shape_name != new_shape_name:
                self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""

        for node in self.nodes():
            mesh = node.name()
            old_shape_name = cmds.listRelatives(mesh, pa=True, type='shape')

            if '|' in mesh:
                mesh = mesh[1:]

            new_shape_name = f'{mesh}Shape'

            if new_shape_name != mesh:
                log.info(
                    f'Fixing Shape: Replacing ({old_shape_name}) with ({new_shape_name})'
                )
                cmds.rename(old_shape_name, new_shape_name)
