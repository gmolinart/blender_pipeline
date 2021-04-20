import bpy
# from cgl.plugins.blender import alchemy as alc

class ImagesToTexTask(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.images_to_tex_task'
    bl_label = 'Images To Tex Task'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    from cgl.plugins.blender.tasks import shd, mdl, lay, rig, bndl, tex
    from cgl.plugins.blender import msd, alchemy, utils

    from importlib import reload
    reload(utils)
    reload(alchemy)
    reload(shd)
    reload(lay)
    reload(mdl)
    reload(msd)
    reload(rig)
    reload(tex)
    reload(bndl)

    shd.setup_shader()
    utils.purge_unused_data()

    msd.add_namespace()
    tex.fix_texture_names()
    tex.images_to_tex_task()
