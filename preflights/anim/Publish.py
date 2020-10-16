from cgl.plugins.preflight.preflight_check import PreflightCheck
from cgl.plugins.blender import lumbermill as lm
import bpy
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
        current_render = current_scene.copy(context='render', filename=None, ext=None)
        scene = lm.scene_object()
        current_source = scene.copy(context='source', filename=None, ext=None).path_root
        current_render = scene.copy(context='render', filename=None, ext=None).path_root
        cgl_copy(current_source, current_render)
        lm.save_file_as(current_scene.copy(context='render').path_root)
        self.pass_check('Check Passed')
        self.final_check()

        # self.fail_check('Check Failed')
