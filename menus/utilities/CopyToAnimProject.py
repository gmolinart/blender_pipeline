import bpy
# from cgl.plugins.blender import lumbermill as lm

class CopyToAnimProject(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.copy_to_anim_project'
    bl_label = 'Copy To Anim Project'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


from cgl.plugins.blender import lumbermill as lm
from cgl.core.utils.general import split_all, cgl_copy

def move_to_project(project):
    context = ['source', 'render']
    scene = lm.scene_object()
    for item in context:
        fromDir = scene.copy(context=item, filename=None).path_root
        toDir = scene.copy(context=item, filename=None, project=project).path_root
        cgl_copy(fromDir, toDir)


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """



    # project = lm.InputDialog(title='Move to project',
    #                   message='Please Type project Name', line_edit=True,
    #                   regex='^([a-z]{3,}, *)*[a-z]{3,}', name_example='MILVIO_ANIM',buttons = ['ok','cancel'])


    project = 'MILVIO_ANIM'

    #if project[1] == 'ok':

    move_to_project(project)