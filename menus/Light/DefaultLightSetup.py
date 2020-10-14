import bpy
from cgl.plugins.blender import lumbermill as lm
#from cgl.plugins.blender import utils

class DefaultLightSetup(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.default_light_setup'
    bl_label = 'Default Light Setup'
    #
    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}



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
    path_object.set_attr(filename='%s_%s_%s.%s' % (path_object.seq,
                                                   path_object.shot,
                                                   path_object.task,
                                                   current_scene.ext
                                                   ))
    default_light = path_object.latest_version()
    print(default_light.path_root)

    default_in_scene = False
    for collection in bpy.data.collections:
        if 'defautLightSet' in collection.name:
            default_in_scene = True

    if not default_in_scene:
        lm.import_file(filepath=default_light.path_root,collection_name=default_light.filename_base, linked=False,append= False ,type='COLLECTION', )

    bpy.context.scene.collection.children.link(bpy.data.collections[path_object.shot])
    return (default_light)



def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    get_default_lighting()

