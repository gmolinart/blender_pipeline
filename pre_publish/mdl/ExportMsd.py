from cgl.plugins.preflight.preflight_check import PreflightCheck
# from cgl.plugins.blender import magic_browser as lm
# from cgl.plugins.blender import utils


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
        from cgl.plugins.blender.tasks import mdl
        from cgl.plugins.blender.alchemy import scene_object
        from cgl.plugins.blender.utils import get_scene_object
        from cgl.plugins.blender import msd
        scene = mdl.Task(scene_object())
        scene.export_msd()
        msd.add_namespace(get_scene_object('mdl'))
        print('Export Msd')
        self.pass_check('Check Passed')
        # self.fail_check('Check Failed')
