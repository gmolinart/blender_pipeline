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

        currentScene = lm.scene_object()
        assetName = lm.scene_object().shot
        obj_in_collection = bpy.data.collections[assetName].all_objects

        utils.setup_preview_viewport_display(selection = obj_in_collection)

        print(' Viewport Color Assigned')
        self.pass_check('Check Passed')
        # self.fail_check('Check Failed')
