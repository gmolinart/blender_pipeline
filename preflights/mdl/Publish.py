from cgl.plugins.preflight.preflight_check import PreflightCheck
from cgl.plugins.blender import lumbermill as lm
import bpy
import os
from cgl.core.utils.general import split_all, cgl_copy


# from cgl.plugins.blender import utils


class Publish(PreflightCheck):

    def getName(self):
        pass

    def run(self):
        """
        script to be executed when the preflight is run.

        If the preflight is successful:
        self.pass_check('Message about a passed Check')

        if the preflight fails:
        self.fail_check('Message about a failed check')
        :return:
        """
        print('Publish')


        #lm.save_file()
        current_scene = lm.scene_object()
        render_file = current_scene.copy(context='render')
        current_source = current_scene.copy(context='source', filename=None, ext=None).path_root
        current_render = current_scene.copy(context='render', filename=None, ext=None).path_root

        bpy.ops.file.make_paths_relative()
        if os.path.isdir(current_render):
            if current_scene.filename not in os.listdir(current_render):
                lm.save_file_as(render_file.path_root)
            else:
                os.remove(render_file.path_root)
                lm.save_file_as(render_file.path_root)
        else:
            os.makedirs(current_render)
            lm.save_file_as(render_file.path_root)

        lm.open_file(current_scene.copy(context='source').path_root)
        bpy.ops.file.make_paths_relative()
        lm.save_file()
        bpy.ops.object.copy_latest_low()
        self.pass_check('Check Passed')
        self.final_check()

        # self.fail_check('Check Failed')
