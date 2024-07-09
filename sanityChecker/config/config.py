# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
# ----------------------------------------------------------------------------------------

# Just add or remove the name of the check from the `CHECKS` list from the Category.
# Custom Categories can be created just by editing this dictionary.


CHECKS = {
    'my_test_suite': [
        'subdivision_limit',
    ],
    'scene': [
        'group_id_node',
        'hdri_colorspace',
        'invalid_shape_name_standin',
        'invalid_shape_name',
        'maya_viewport_smoooth',
        'missing_files',
        'missing_tx_files',
        'multiple_context_node',
        'no_shading_group',
        'scene_orphan_nodes',
        'legacy_rl',
        'subdivision_limit',
        'unconnected_nodes',
        'unknown_nodes',
        'visible_views',
        'xgen_nodes',
    ],
    'model': [
        'anim_curves',
        'aovs',
        'atmosphere_nodes',
        'blind_data_node',
        'custom_views',
        'display_layers',
        'duplicated_names',
        'empty_create_colorset',
        'empty_namespace',
        'empty_uvset',
        'existing_namespace',
        'group_id_node',
        'hdri_colorspace',
        'hide_facedata_set',
        'history',
        'invalid_shape_name_standin',
        'invalid_shape_name',
        'mesh_ending_number',
        'missing_files',
        'missing_tx_files',
        'multiple_context_node',
        'multiple_shapes',
        'no_shading_group',
        'non_manifold_geometry',
        'lamina_faces',
        'legacy_rl',
        'mesh_suffix',
        'node_limit',
        'non_zero_transforms',
        'non_zero_pivot',
        'nsided_polygons',
        'orphan_model_nodes',
        'scene_orphan_nodes',
        'subdivision_limit',
        'unconnected_nodes',
        'unknown_nodes',
        'visible_views',
        'visibility_off',
        'xgen_nodes',
    ],
    'shading': [
        'anim_curves',
        'aovs',
        'arnold_texture_memory',
        'atmosphere_nodes',
        'blind_data_node',
        'custom_views',
        'display_layers',
        'duplicated_names',
        'empty_create_colorset',
        'empty_namespace',
        'empty_uvset',
        'existing_namespace',
        'file_alpha_luminance',
        'file_colorspace_rule',
        'file_colorspaces',
        'file_generate_tx',
        'file_old_colorspaces',
        'group_id_node',
        'hdri_colorspace',
        'hide_facedata_set',
        'history',
        'invalid_shape_name_standin',
        'invalid_shape_name',
        'map_uv_set',
        'viewport_smooth',
        'mesh_ending_number',
        'mipmap_bias',
        'missing_files',
        'missing_tx_files',
        'multiple_context_node',
        'multiple_shapes',
        'multiple_uv_sets',
        'no_shading_group',
        'non_manifold_geometry',
        'lamina_faces',
        'legacy_rl',
        'mesh_suffix',
        'node_limit',
        'non_zero_transforms',
        'non_zero_pivot',
        'nsided_polygons',
        'orphan_model_nodes',
        'subdivision_limit',
        'unconnected_nodes',
        'unknown_nodes',
        'visible_views',
        'visibility_off',
        'xgen_nodes',
    ],
}


if __name__ == '__main__':
    # print all checks
    unique_checks = set()
    for category, checks in CHECKS.items():
        for check in checks:
            unique_checks.add(check)

    for check in sorted(unique_checks):
        print(check)
