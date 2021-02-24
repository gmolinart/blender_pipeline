import bpy
import json
from os.path import isdir, isfile
from cgl.plugins.blender import alchemy as alc

from cgl.plugins.blender import utils as utils
from importlib import reload
reload(utils)
reload(alc)



class Build(bpy.types.Operator):
    """
    Builds the shot with all the avilable elements
    """
    bl_idname = 'object.build'
    bl_label = 'Build'

    def execute(self, context):
        run()
        return {'FINISHED'}



def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    alc.build()


if __name__ == "__main__":
    run()