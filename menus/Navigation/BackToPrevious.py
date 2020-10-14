import bpy
# from cgl.plugins.blender import lumbermill as lm

class BackToPrevious(bpy.types.Operator):
    """
    goes to the most recent file under files, recent files
    """
    bl_idname = 'object.back_to_previous'
    bl_label = 'Back To Previous'

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

    from os.path import exists, basename
    from cgl.plugins.blender import lumbermill as lm
    fp = bpy.utils.user_resource('CONFIG', "recent-files.txt")
    print(fp)

    try:
        with open(fp) as file:
            recent_files = file.read().splitlines()
    except (IOError, OSError, FileNotFoundError):
        recent_files = []

    lm.open_file(recent_files[0])


