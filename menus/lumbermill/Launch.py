import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender.main_window import CGLumberjack
class Launch(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.launch'
    bl_label = 'Launch'

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}

# class BlenderJack(CGLumberjack):
#
#     if bpy.data.filepath :
#
#         scene = lm.scene_object()
#         scope = scene.scope
#         task = scene.task
#         if scene.shot:
#             if scope == 'assets':
#                 open_path = '{}/*'.format(scene.split_after('asset'))
#
#             else:
#                 if task == 'lay':
#                     open_path = '{}/assets'.format(scene.split_after('project'))
#
#                 else:
#                     open_path = '{}/*'.format(scene.split_after('shot'))
#
#         else :
#             open_path= path
#         def __init__(self, parent=None, path=open_path, user_info=None):
#             CGLumberjack.__init__(self, parent, user_info=user_info, previous_path=path, sync_enabled=False)
#             print('Application Path path is %s' % path)





def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    lm.launch_()




    #lm.launch_()

