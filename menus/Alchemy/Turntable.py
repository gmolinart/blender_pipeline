import bpy
from cgl.plugins.blender import alchemy as alc
#from cgl.plugins.blender import utils
class Turntable(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.turntable'
    bl_label = 'Turntable'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def get_default_lighting():
    current_scene = alc.scene_object()
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

    path_object = alc.PathObject(dict_)
    path_object.set_attr(filename='%s_%s_%s.%s' % (path_object.seq,
                                                   path_object.shot,
                                                   path_object.task,
                                                   current_scene.ext
                                                   ))
    default_light = path_object.latest_version()

    alc.import_file(filepath=default_light.path_root, collection_name =  default_light.filename_base ,linked=False, append= False, type='COLLECTION')
    bpy.context.scene.collection.children.link(bpy.data.collections[default_light.filename_base])

    return (default_light)

def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:

    """
    if bpy.context.selected_objects:
        try:

            bpy.ops.object.delete_defaults()
            bpy.ops.object.delete_turntable()
        except AttributeError:
            print('no objects to delete')
        alc.create_turntable()
        get_default_lighting()
        bpy.ops.object.build()

    else:
        alc.confirm_prompt(message='Please select geo')