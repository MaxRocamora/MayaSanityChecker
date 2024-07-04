# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds


def get_scene_mesh_transform_nodes(skip_namespaces: bool = True) -> list:
    """Collect transform mesh nodes from maya scene."""
    all_transforms = cmds.ls(type='transform', shortNames=True)

    # Filter all transforms that are meshes
    mesh_transforms = []
    for transform in all_transforms:
        transform_shapes = cmds.listRelatives(transform, shapes=True, fullPath=True)
        if transform_shapes is not None:
            for shape in transform_shapes:
                if cmds.nodeType(shape) == 'mesh':
                    mesh_transforms.append(transform)
                    break

    # Skip namespaces items
    if skip_namespaces:
        mesh_transforms = [i for i in mesh_transforms if ':' not in i]

    return mesh_transforms


def get_orphan_nodes_of_type(node_types: list) -> list:
    """Collect nodes of given type that have no connections."""
    nodes = []
    for node_type in node_types:
        for node in cmds.ls(type=node_type):
            if cmds.listConnections(node) is None:
                nodes.append(node)

    return nodes


def get_scene_shapes() -> list:
    """Return all shapes in the scene."""
    all_meshes = cmds.ls(type='mesh', dag=True, noIntermediate=True)
    nodes = cmds.listRelatives(all_meshes, parent=True, fullPath=True, path=True)

    # filter namespace nodes
    if nodes:
        nodes = [n for n in nodes if ':' not in n]

    return nodes or []


def get_scene_standins() -> list:
    """Collect Arnold standins from maya scene."""
    all_standins = cmds.ls(type='aiStandIn')
    nodes = cmds.listRelatives(all_standins, parent=True, fullPath=True, path=True)

    # filter namespace nodes
    if nodes:
        nodes = [n for n in nodes if ':' not in n]

    return nodes or []
