from cgl.plugins.preflight.preflight_check import PreflightCheck
# from cgl.plugins.blender import magic_browser as lm
# from cgl.plugins.blender import utils


from cgl.plugins.blender.msd import set_source_path
from cgl.core.path import add_root, PathObject
from cgl.plugins.blender import utils


def add_namespace(task = 'bndl'):
    set_source_path()

    bndl = utils.get_object(task)

    for obj in bndl.children:
        print(obj.name)

        path_object = PathObject(add_root(obj['source_path']))
        asset = path_object.asset
        new_name = '{}:{}'.format(asset, obj.name)

        if ':' not in obj.name:
            obj.name = new_name


class CheckNamespace(PreflightCheck):

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
        print('Check Namespace')
        add_namespace()
        self.pass_check('Check Passed')
        # self.fail_check('Check Failed')
