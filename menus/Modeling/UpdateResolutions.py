import bpy
from cgl.plugins.blender import lumbermill as lm
import os
from cgl.core.utils.general import split_all, cgl_copy

class UpdateResolutions(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.update_resolutions'
    bl_label = 'Update Resolutions'

    def execute(self, context):
        run()
        return {'FINISHED'}



def check_resolution(scene, res):
    res_path = scene.copy(resolution=res)
    if os.path.isfile(res_path.path_root):
        print('{} found in: \n{} \n'.format(res, res_path.path_root))

        return (res_path)
    else:
        print('{} version {} missing'.format(res, res_path.version))




def get_latest_low():
    scene = lm.scene_object()
    versions = scene.glob_project_element('version')
    version = versions.reverse()

    latest_low = None
    for version in versions:
        path_object = scene.copy(version=version)

        if latest_low == None:

            if path_object.resolution == 'high':
                latest_low = check_resolution(path_object, 'low')
    return latest_low


def get_latest_high():
    scene = lm.scene_object()
    versions = scene.glob_project_element('version')
    version = versions.reverse()

    latest_high = None

    for version in versions:
        path_object = scene.copy(version=version)

        if latest_high == None:
            latest_high = check_resolution(path_object, 'high')

    return latest_high


def copy_latest_low():
    scene = lm.scene_object()
    latest_low_folder = get_latest_low().copy(filename=None, ext=None).path_root
    current_low_folder = scene.copy(filename=None, ext=None, resolution='low').path_root
    cgl_copy(latest_low_folder, current_low_folder)


def copy_latest_high():
    scene = lm.scene_object()
    latest_high_folder = get_latest_high().copy(filename=None, ext=None).path_root
    current_high_folder = scene.copy(filename=None, ext=None, resolution='high').path_root
    cgl_copy(latest_high_folder, current_high_folder)




def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    scene = lm.scene_object()
    copy_latest_low()
    copy_latest_high()
