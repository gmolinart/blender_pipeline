import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils as utils
import json

class GetDefaultCamera(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.get_default_camera'
    bl_label = 'GetDefaultCamera'

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def get_default_camera():
    current_scene = lm.scene_object()
    dict_ = {'company': current_scene.company,
             'context': 'source',
             'project': current_scene.project,
             'scope': 'shots',
             'seq': 'DEFAULT_RIG_CHECK',
             'shot': '0010',
             'task': 'cam',
             'user': 'publish',
             'resolution': 'high'
             }

    path_object = lm.LumberObject(dict_)
    path_object.set_attr(filename='%s_%s_%s.%s' % (path_object.seq,
                                                   path_object.shot,
                                                   path_object.task,
                                                   'blend'
                                                   ))
    default_camera = path_object.latest_version()
    print(default_camera.path_root)

    default_in_scene = False
    for group in bpy.data.node_groups:
        if path_object.filename in group.name:
            default_in_scene = True

    if not default_in_scene:
        lm.import_file(filepath=default_camera.path_root, type='CAMERA', linked=False,
                       collection_name=path_object.filename_base)
        bpy.context.scene.collection.objects.link(bpy.data.objects[path_object.filename_base])

    outFile = default_camera.copy(ext='json').path_root
    with open(outFile) as json_file:

        data = json.load(json_file)
        bpy.context.scene.frame_start = data['frame_start']
        bpy.context.scene.frame_end = data['frame_end']

    #

    return (default_camera)




def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    get_default_camera()

    print('DefaultCamera Imported')

