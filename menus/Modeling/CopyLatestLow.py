import bpy
# from cgl.plugins.blender import lumbermill as lm

class CopyLatestLow(bpy.types.Operator):
    """
    Finds the latest low publshed file
    """
    bl_idname = 'object.copy_latest_low'
    bl_label = 'Copy Latest Low'

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


from cgl.plugins.preflight.preflight_check import PreflightCheck
from cgl.plugins.blender import lumbermill as lm
import bpy
import os
from cgl.core.utils.general import split_all, cgl_copy


def get_items():
    from cgl.plugins.blender import lumbermill as lm

    path_object = lm.scene_object()

    versions = path_object.glob_project_element('version')
    version = versions.reverse()
    print(versions)

    value = [(versions[i], versions[i], '') for i in range(len(versions))]

    return (versions)


def copy_latest_low():
    versions = get_items()
    scene = lm.scene_object()
    low_found = None
    for i in versions:
        if not low_found:

            low = scene.copy(version=i, resolution='low')
            low_dir = low.copy(filename='')

            if os.path.isdir(low_dir.path_root):
                print(low.path_root)
                low_found = low_dir

    cgl_copy(low_found.path_root, scene.copy(resolution='low', filename='').path_root)
    cgl_copy(low_found.path_root, scene.copy(context='render', resolution='low', filename='').path_root)



def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    try :
        copy_latest_low()
    except AttributeError:
        pass
