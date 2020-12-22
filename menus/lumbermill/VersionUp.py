import bpy
from cgl.plugins.blender import alchemy as alc
from cgl.core.utils.general import create_file_dirs, cgl_copy

class VersionUp(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.version_up'
    bl_label = 'Version Up'

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    scene = alc.scene_object()

    if scene.context == 'source':
        if scene.resolution == 'high':
            alc.version_up()


            bpy.ops.file.make_paths_relative()

            low_res = alc.scene_object().copy(resolution='low')
            for res in low_res.glob_project_element('filename'):
                create_file_dirs(res)
                cgl_copy(res.path_root, low_res.path_root)

            alc.confirm_prompt(message="Version up to {}".format(alc.scene_object().version))

        else:
            alc.confirm_prompt(message="This is a low resolution version , please edit source file")

    else:
        alc.confirm_prompt(message="files in the render context shouldn't be versioned up, please edit source file")



