import bpy
import json
import os
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils as utils

class ReadLayout(bpy.types.Operator):
    """
    reads in the current scene layout.
    """
    bl_idname = 'object.read_layout'
    bl_label = 'Read Layout'

    def execute(self, context):
        run()
        return {'FINISHED'}


def read_layout(outFile=None, linked=False, append=False):
    """
    Reads layout from json file
    :param outFile: path to json file
    :param linked:
    :param append:
    :return:
    """
    from cgl.plugins.blender.lumbermill import scene_object, LumberObject, import_file
    from cgl.core.utils.read_write import load_json
    import bpy

    if outFile == None:
        outFileObject = scene_object().copy(ext='json', task='lay', user='publish').latest_version()
        outFileObject.set_attr(filename='%s_%s_%s.%s' % (outFileObject.seq,
                                                         outFileObject.shot,
                                                         outFileObject.task,
                                                         'json'
                                                         ))
        outFile = outFileObject.path_root
    # outFile = scene_object().path_root.replace(scene_object().ext, 'json')



    data = load_json(outFile)

    for p in data:
        print(p)
        data_path = data[p]['source_path']
        blender_transform = data[p]['blender_transform']

        transform_data = []
        for value in blender_transform:
            transform_data.append(value)

        print(transform_data)

        pathToFile = os.path.join(scene_object().root, data_path)
        lumberObject = LumberObject(pathToFile)



        if lumberObject.filename in bpy.data.libraries:
            lib = bpy.data.libraries[lumberObject.filename]
            bpy.data.batch_remove(ids=([lib]))
            import_file(lumberObject.path_root, linked=linked, append=append)
        else:
            import_file(lumberObject.path_root, linked=linked, append=append)

        if p not in bpy.context.collection.objects:
            obj = bpy.data.objects.new(p, None)
            bpy.context.collection.objects.link(obj)
            obj.instance_type = 'COLLECTION'
            obj.instance_collection = bpy.data.collections[lumberObject.asset]
            obj.location = (transform_data[0], transform_data[1], transform_data[2])
            obj.rotation_euler = (transform_data[3], transform_data[4], transform_data[5])
            obj.scale = (transform_data[6], transform_data[7], transform_data[8])

    bpy.ops.file.make_paths_relative()

def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    if lm.scene_object().type == 'env':
        read_layout(outFile=lm.scene_object().copy(ext='json').path_root)

    else:
        read_layout()