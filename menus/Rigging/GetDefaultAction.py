import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils as utils
import json

class GetDefaultAction(bpy.types.Operator):
    """
    Imports the default rigtest animation for the project
    """
    bl_idname = 'object.get_default_action'
    bl_label = 'GetDefaultAction'

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def get_default_action():
    current_scene = lm.scene_object()
    dict_ = {'company': current_scene.company,
             'context': 'source',
             'project': current_scene.project,
             'scope': 'shots',
             'seq': 'DEFAULT_RIG_CHECK',
             'shot': '0010',
             'task': 'anim',
             'user': 'publish',
             'resolution': 'high'
             }

    path_object = lm.LumberObject(dict_)
    path_object.set_attr(filename='%s_%s_%s.%s' % (path_object.seq,
                                                   path_object.shot,
                                                   path_object.task,
                                                   current_scene.ext
                                                   ))
    default_action = path_object.latest_version()
    print(default_action.path_root)

    default_in_scene = False
    for group in bpy.data.node_groups:
        if path_object.filename in group.name:
            default_in_scene = True

    if not default_in_scene:
        lm.import_file(filepath=default_action.path_root, linked=False, type='ANIM')

    return (default_action)



def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    get_default_action()
    print('Default rig check action imported')

