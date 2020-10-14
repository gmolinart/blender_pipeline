import bpy
from cgl.plugins.blender import lumbermill as lm
import os


class CollectionToAsset(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.collection_to_asset'
    bl_label = 'Collection To Asset'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def export_to_task(assetName, task):
    task_to_export = lm.scene_object().copy(task=task,
                                            set_proper_filename=True,
                                            type = 'prop',
                                            shot=assetName).next_major_version()

    if not os.path.isdir(task_to_export.copy(filename='').path_root):
        os.makedirs(task_to_export.copy(filename='').path_root)

    lm.save_file_as(task_to_export.path_root)


def run():
    collection = bpy.context.collection
    export_to_task(collection.name, task='mdl', )
    bpy.ops.object.cleanup_scene()
    bpy.ops.object.build()


