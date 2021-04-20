import os

import bpy
from cgl.plugins.blender import alchemy as alc
from cgl.plugins.blender.tasks import mdl

from cgl.plugins.blender import utils
from importlib import reload

reload(utils)

class MeshToMdlTask(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.mesh_to_mdl_task'
    bl_label = 'Mesh To Mdl Task'

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
    from cgl.plugins.blender import msd, utils
    from cgl.plugins.blender.alchemy import scene_object
    task = 'mdl'
    utils.cleanup_file(task)

    collection = utils.get_scene_collection()
    collection.name = collection.name.replace(':{}'.format(scene_object().task), ':{}'.format(task))


    mdl_task = utils.save_to_task('mdl')
    alc.confirm_prompt('file exported to mdl task user: {} version: {}'.format(mdl_task.user,mdl_task.version))

if __name__ == "__main__":
    run()
