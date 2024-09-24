# ----------------------------------------------------------------------------------------
# check for maya recursive namespaces
# skips lookdev namespaces: LDV, STAGE
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

IGNORE_NAMESPACES = ['LDV', 'STAGE', 'lookdev_']
DEFAULT_NAMESPACES = ['UI', 'shared']

name = 'Existing Namespace'
group = CategoryGroups.SCENE
description = 'Namespaces with nodes found in scene'
level = SeverityLevels.CRITICAL
autofix = False
hint = 'Remove your references or namespace from scene using the namespace editor'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        namespaces_info = cmds.namespaceInfo(':', listOnlyNamespaces=True)
        namespaces = [ns for ns in namespaces_info if ns not in DEFAULT_NAMESPACES]

        namespaces_found = []
        if namespaces:
            for each in namespaces:
                ns_children = self._existing_namespace_recursive(each)
                namespaces_found.append(each)
                namespaces_found += ns_children

        for node in namespaces_found:
            if node in IGNORE_NAMESPACES:
                continue

            self.add_failed_node(node)

    def _existing_namespace_recursive(self, namespace: str) -> list:
        """Recursively find all children namespaces of given namespace."""
        ns_children = cmds.namespaceInfo(namespace, listOnlyNamespaces=True)
        if ns_children is None:
            return []

        addition_children = []
        for each in ns_children:
            ns_children = self._existing_namespace_recursive(each)
            if len(ns_children) >= 1:
                addition_children += ns_children

        return ns_children + addition_children
