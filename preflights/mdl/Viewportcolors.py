from cgl.plugins.preflight.preflight_check import PreflightCheck
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils
import bpy


class Viewportcolors(PreflightCheck):

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


        try:
            #bpy.ops.object.setup_shader_color()
            #setup_preview_viewport_display(selection = obj_in_collection)
            self.pass_check('Check Passed')
        except :
            self.fail_check('Check Failed, please delete shaders and assign them again')
            # pass
            # self.pass_check('Check Passed')
        print(' Viewport Color Assigned')

