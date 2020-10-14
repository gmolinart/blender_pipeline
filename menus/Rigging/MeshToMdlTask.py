import os

import bpy
from cgl.plugins.blender import lumbermill as lm


class MeshToMdlTask(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.mesh_to_mdl_task'
    bl_label = 'Mesh To Mdl Task'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def parent_mesh_to_rig(assetName=''):
    if assetName == '':
        assetName = lm.scene_object().shot
    rigname = '{}_rig'.format(assetName)
    meshGroupName = '{}_mesh_grp'.format(assetName)

    meshGrp = bpy.data.objects[meshGroupName]
    rig = bpy.data.objects[rigname]

    meshes = []

    for obj in bpy.data.objects:

        if 'cs_' not in obj.name:
            if obj.type == "MESH":
                if any([modifier for modifier in obj.modifiers if modifier.type == "ARMATURE"]):
                    print(obj.name)
                    # obj.parent = rig
                    # mesh_grp_name = '{}_mesh_grp'.format(assetName)

                    #        mesh_grp = bpy.data.objects[mesh_grp_name]

                    obj.parent = meshGrp
                    obj.matrix_parent_inverse = meshGrp.matrix_world.inverted()
                    meshes.append(obj)
                    print(obj.parent.name)

                try:

                    for collection in bpy.data.collections:
                        if collection.name == assetName:
                            collection.objects.link(obj)

                except(RuntimeError, TypeError, NameError, AttributeError):
                    pass

                for collection in obj.users_collection:
                    if collection.name != assetName:
                        collection.objects.unlink(obj)

        return meshes


def export_to_task(task):
    task_to_export = lm.scene_object().copy(task=task,
                                            set_proper_filename=True).next_major_version()

    if not os.path.isdir(task_to_export.copy(filename='').path_root):
        os.makedirs(task_to_export.copy(filename='').path_root)

    lm.save_file_as(task_to_export.path_root)
    bpy.ops.object.build()


def unparent_meshes(meshes=None):
    if not meshes:
        meshes = parent_mesh_to_rig()

    for mesh in meshes:
        mesh.parent = None


def delete_group_objects():
    for obj in bpy.data.objects:
        if obj.name.endswith('grp'):
            bpy.data.objects.remove(obj)


def check_required_elements(assetName=''):
    try:
        if assetName == '':
            assetName = lm.scene_object().shot
        rigname = '{}_rig'.format(assetName)
        meshGroupName = '{}_mesh_grp'.format(assetName)
        meshGrp = bpy.data.objects[meshGroupName]
        rig = bpy.data.objects[rigname]
    except(NameError):
        raise NameError('No asset Name provided')
    except(KeyError):
        bpy.ops.object.parent_mesh_to_rig()


def convert_main_collection_name_to_task(task, assetName=''):
    if assetName == '':
        assetName = lm.scene_object().shot

    for collection in bpy.data.collections:
        if collection.name == assetName:
            collection.name = '{}_{}'.format(assetName, task)

    collection = bpy.data.collections.new(assetName)
    bpy.context.scene.collection.children.link(collection)
    parent_mesh_to_rig(assetName)


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    scene = lm.scene_object()
    if not scene.user == 'publish':
        check_required_elements()
        convert_main_collection_name_to_task('rig')
        unparent_meshes()
        delete_group_objects()
        bpy.ops.object.cleanup_scene()
        export_to_task('mdl')


if __name__ == "__main__":
    run()
