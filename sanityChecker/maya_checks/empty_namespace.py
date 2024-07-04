# ----------------------------------------------------------------------------------------
# check for maya empty namespaces
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Empty Namespace'
group = CategoryGroups.SCENE
description = 'Empty Namespaces on your scene'
level = SeverityLevels.HIGH
autofix = True
hint = 'Remove empty namespaces using the Namespace Editor window'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in self.get_empty_namespaces():
            self.add_failed_node(node)

    def fix(self):
        """Perform technical fix on this check."""
        for node in self.nodes():
            if cmds.namespace(exists=node):
                cmds.namespace(rm=node)

    def get_empty_namespaces(self) -> list:
        """Returns empty namespaces."""
        nodes = []
        current_ns = cmds.namespaceInfo(currentNamespace=True)

        if cmds.namespaceInfo(current_ns, isRootNamespace=True):
            namespace_info = cmds.namespaceInfo(current_ns, listOnlyNamespaces=True)

            if namespace_info is not None:
                for each in namespace_info:
                    is_empty = self.empty_namespace_recursive(each)
                    if is_empty is not None:
                        nodes.append(is_empty)

        return nodes

    def empty_namespace_recursive(self, ns_name: str):
        """Returns empty namespace recursively."""
        namespace_info = cmds.namespaceInfo(ns_name, listOnlyNamespaces=True)

        if namespace_info is not None:
            for each in namespace_info:
                is_empty = self.empty_namespace_recursive(each)

                if is_empty is not None:
                    return is_empty

        elif cmds.namespaceInfo(ns_name, listNamespace=True) is None:
            if ns_name != 'shared':
                return ns_name
