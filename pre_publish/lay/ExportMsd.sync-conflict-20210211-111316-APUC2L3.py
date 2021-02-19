from cgl.plugins.preflight.preflight_check import PreflightCheck
# from cgl.plugins.blender import Alchemy as lm
# from cgl.plugins.blender import utils
from cgl.plugins.blender import msd
import os

class ExportMsd(PreflightCheck):

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
        print('Export Msd')
        scene = msd.MagicSceneDescription()
        scene.export()

        if os.path.isfile(scene.output_msd):
            self.pass_check('Check Passed')
        else:
            self.fail_check('Check Failed')