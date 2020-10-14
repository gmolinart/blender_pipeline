import bpy
from cgl.plugins.blender import lumbermill as lm
import os

class ExportLightSetup(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.export_light_setup'
    bl_label = 'Export Light Setup'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def export_to_task(assetName, task):
    task_to_export = lm.scene_object().copy(task=task,
                                            set_proper_filename=True,
                                            shot=assetName).next_major_version()

    if task == 'light':
        task_to_export = task_to_export.copy(scope='shots', seq='LIGHT_SETUP', shot=assetName.split('_')[-1])

    if not os.path.isdir(task_to_export.copy(filename='').path_root):
        print('______EMPTY DIR_________')
        os.makedirs(task_to_export.copy(filename='').path_root)

    return task_to_export


def get_default_lighting():
    current_scene = lm.scene_object()
    dict_ = {'company': current_scene.company,
             'context': 'source',
             'project': current_scene.project,
             'scope': 'shots',
             'seq': 'DEFAULT_LIGHT_SETUP',
             'shot': '0010',
             'task': 'light',
             'user': 'publish',
             'resolution': 'high'
             }

    path_object = lm.LumberObject(dict_)
    path_object.copy(set_proper_filename=True)
    # return (default_light)





def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    collection = bpy.context.collection
    light_task = export_to_task(collection.name, task='light')
    lm.save_file_as(light_task.path_root)
    bpy.ops.object.build()
    collection.name = bpy.context.scene.name
    lm.save_file()