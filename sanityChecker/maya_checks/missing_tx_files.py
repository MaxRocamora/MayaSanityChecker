# ----------------------------------------------------------------------------------------
# check for missing tx files from files on file node
# ----------------------------------------------------------------------------------------
import glob
import os
import maya.cmds as cmds  # type: ignore

from sanityChecker.libs.check import Check
from sanityChecker.libs.enums import CategoryGroups, SeverityLevels
from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

name = 'Missing TX Filemaps'
group = CategoryGroups.MAPS
description = 'TX version of filemaps are missing.'
level = SeverityLevels.CRITICAL
autofix = False
hint = 'Generate your missing tx files'


class Check(Check):
    def __init__(self):  # noqa: D107
        super().__init__(name, group, description, level, autofix, hint)

    def run(self):
        """Performs scan of this check on maya scene/nodes."""
        self.reset()

        for node in self.get_non_tx_filenodes():
            filename = cmds.getAttr(f'{node}.fileTextureName')
            color_space = cmds.getAttr(f'{node}.colorSpace')

            if not self.has_tx_file(filename, color_space):
                self.add_failed_node(node)

    @staticmethod
    def has_tx_file(filename: str, color_space: str) -> bool:
        """Return whether a legacy or Arnold color-space TX file exists."""
        filepath_no_extension, extension = os.path.splitext(filename)
        legacy_tx_filename = f'{filepath_no_extension}.tx'
        arnold_tx_filenames = (
            f'{filepath_no_extension}_{color_space}{extension}.tx',
            f'{filepath_no_extension}_{color_space}_*{extension}.tx',
            f'{filepath_no_extension}_raw{extension}.tx',
        )
        return os.path.exists(legacy_tx_filename) or any(
            glob.glob(tx_filename) for tx_filename in arnold_tx_filenames
        )

    def get_non_tx_filenodes(self) -> list:
        """Collect nodes to scan from maya scene."""
        _non_tx_filenodes = []

        for n in cmds.ls(type='file', long=True):
            filename = cmds.getAttr(f'{n}.fileTextureName')
            if os.path.splitext(filename)[1] != '.tx':
                _non_tx_filenodes.append(n)

        return _non_tx_filenodes
