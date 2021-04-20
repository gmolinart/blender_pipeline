from cgl.plugins.preflight.preflight_check import PreflightCheck
# from cgl.plugins.blender import magic_browser as lm
# from cgl.plugins.blender import utils


class FixNames(PreflightCheck):

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
        print('Fix Names')
        from cgl.plugins.blender import msd

        msd.fix_object_name()

        self.pass_check('Check Passed')
        # self.fail_check('Check Failed')
