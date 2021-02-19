from cgl.plugins.preflight.preflight_check import PreflightCheck
# from cgl.plugins.blender import Alchemy as lm
# from cgl.plugins.blender import utils

from cgl.plugins.blender.tasks.tex import fix_texture_names
class CheckNames(PreflightCheck):

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
        
        fix_texture_names()
        print('Checking Textures Names')
        self.pass_check('Check Passed')
        # self.fail_check('Check Failed')
