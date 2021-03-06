from cgl.plugins.preflight.preflight_check import PreflightCheck
# from cgl.plugins.blender import magic_browser as lm
# from cgl.plugins.blender import utils


from cgl.plugins.preflight.preflight_check import PreflightCheck
import bpy
from cgl.plugins.blender import utils
from cgl.plugins.blender import alchemy as alc
from cgl.plugins.blender import utils



class DeleteNonTaskObjects(PreflightCheck):

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

        from cgl.plugins.blender.utils import cleanup_file

        cleanup_file(task='mdl')

        print('Delete Non Task Objects')
        self.pass_check('Check Passed')
        # self.fail_check('Check Failed')
