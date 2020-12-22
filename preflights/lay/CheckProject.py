from cgl.plugins.preflight.preflight_check import PreflightCheck
from cgl.plugins.blender.tasks.lay import check_reference_attribute



class CheckProject(PreflightCheck):

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

            print(6666666666666666)
            failed_libraries = check_reference_attribute(attribute='project')

            if failed_libraries == []:
                print('Check Project')
                self.pass_check('Check Passed')
            else:

                self.fail_check('Check Failed, {}'.format(failed_libraries))
