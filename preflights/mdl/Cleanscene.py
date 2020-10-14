from cgl.plugins.preflight.preflight_check import PreflightCheck
# from cgl.plugins.blender import lumbermill as lm
# from cgl.plugins.blender import utils
import bpy

class Cleanscene(PreflightCheck):

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
        print('Cleanscene')
        bpy.ops.object.cleanup_rig()
        self.pass_check('Check Passed')
        # self.fail_check('Check Failed')
