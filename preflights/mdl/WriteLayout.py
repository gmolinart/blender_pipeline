from cgl.plugins.preflight.preflight_check import PreflightCheck
from cgl.plugins.blender import lumbermill as lm
# from cgl.plugins.blender import utils


def write_layout_file(outFile=None):
    """

    :param outFile:
    :return:
    """
    from cgl.plugins.blender.lumbermill import scene_object, LumberObject, import_file
    from cgl.core.utils.read_write import save_json
    import bpy
    from pathlib import Path
    import os

    if outFile == None:
        outFile = scene_object().copy(ext='json', context='render')
        outDir = outFile.copy(filename='')
    data = {}

    for obj in bpy.data.objects:
        if obj.is_instancer:
            name = obj.name
            #            blender_transform = np.array(obj.matrix_world).tolist()
            blender_transform = [obj.matrix_world.to_translation().x,
                                 obj.matrix_world.to_translation().y,
                                 obj.matrix_world.to_translation().z,
                                 obj.matrix_world.to_euler().x,
                                 obj.matrix_world.to_euler().y,
                                 obj.matrix_world.to_euler().z,
                                 obj.matrix_world.to_scale().x,
                                 obj.matrix_world.to_scale().y,
                                 obj.matrix_world.to_scale().z]
            try:
                libraryPath = bpy.path.abspath(obj.instance_collection.library.filepath)
                filename = Path(bpy.path.abspath(libraryPath)).__str__()
                libObject = LumberObject(filename)

                data[name] = {'name': libObject.asset,
                              'source_path': libObject.path,
                              'blender_transform': blender_transform}
            except AttributeError:
                print('skipping {}'.format(obj.name))

    if not os.path.isdir(outDir.path_root):
        os.makedirs(outDir.path_root)
    save_json(outFile.path_root, data)

    return (outFile)


class WriteLayout(PreflightCheck):

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
        print('Write Layout')
        if lm.scene_object().type == 'env':
            write_layout_file()
            self.pass_check('Check Passed')
        else:
            print('not environment ')
            self.pass_check('Check Passed')
        # self.fail_check('Check Failed')
