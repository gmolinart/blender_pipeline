import os

import bpy
from cgl.plugins.blender import alchemy as alc


class ReadLayout(bpy.types.Operator):
    """
    reads in the current scene layout.
    """
    bl_idname = 'object.read_layout'
    bl_label = 'Read Layout'

    def execute(self, context):
        run()
        return {'FINISHED'}


def get_layout_libraries(data):
    libraries = {}

    for p in data:

        print(p)
        data_path = data[p]['source_path']

        if data_path in libraries:
            libraries[data_path].append(p)
        else:
            libraries[data_path] = [p]

    return libraries


def read_layout(outFile=None, linked=True, append=False):
    """
    Reads layout from json file
    :param outFile: path to json file
    :param linked:
    :param append: if true the files are imported in the scene
    :return:
    """
    from cgl.plugins.blender.alchemy import scene_object, PathObject, import_file_old
    from cgl.core.utils.read_write import load_json
    import bpy
    import os

    if outFile == None:
        outFileObject = scene_object().copy(ext='json', task='lay', set_proper_filename=True).latest_version()
        outFile = outFileObject.path_root
    # outFile = scene_object().path_root.replace(scene_object().ext, 'json')
    if os.path.isfile(outFile):

        data = load_json(outFile)

        libraries = get_layout_libraries(data)

        print('________LIBRARIES___________')

        for i in libraries:
            pathToFile = os.path.join(scene_object().root, i)
            PathObject = PathObject(pathToFile)

            print(pathToFile)

            if PathObject.filename_base in bpy.data.libraries:
                lib = bpy.data.libraries[PathObject.filename]
                bpy.data.batch_remove(ids=([lib]))
                import_file_old(PathObject.path_root, linked=False, append=True)
                bpy.data.ojects[PathObject.asset].select_set(True)
                bpy.ops.object.unlink_asset()
            else:
                import_file_old(PathObject.path_root, linked=False, append=True)

        for p in data:
            print(p)
            data_path = data[p]['source_path']
            blender_transform = data[p]['blender_transform']

            transform_data = []
            for value in blender_transform:
                transform_data.append(float(value))

            pathToFile = os.path.join(scene_object().root, data_path)
            PathObject = PathObject(pathToFile)
            obj = bpy.data.objects.new(p, None)
            bpy.context.collection.objects.link(obj)
            obj.instance_type = 'COLLECTION'
            if PathObject.asset in bpy.data.collections:

                obj.instance_collection = bpy.data.collections[PathObject.asset]

                location = (transform_data[0], transform_data[1], transform_data[2])
                obj.location = location

                rotation = (transform_data[3], transform_data[4], transform_data[5])
                obj.rotation_euler = rotation

                scale = (transform_data[6], transform_data[7], transform_data[8])
                obj.scale = scale

                if PathObject.type in ['char', ]:

                    if append:
                        print("___________creating proxy rig for {}____________".format(PathObject.asset))
                        rig = '{}_rig'.format(PathObject.asset)
                        print(rig)
                        objects = bpy.context.view_layer.objects
                        bpy.context.view_layer.objects.active = objects[PathObject.asset]
                        bpy.ops.object.proxy_make(object=rig)

                        if 'blender_action_path' in data[p]:
                            anim_path = data[p]['blender_action_path']
                            path_to_anim = os.path.join(scene_object().root, anim_path)
                            print(path_to_anim)
                            alc.import_file_old(path_to_anim, type='ANIM', collection_name=data[p]['blender_action'],
                                           linked=False)

            else:
                print("__________________{} not found_____________".format(PathObject.path_root))
    else:
        print("_____________NO LAYOUT FOUND__________")


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    if alc.scene_object().type == 'env':
        read_layout(outFile=alc.scene_object().copy(ext='json').path_root, append=True)

    elif alc.scene_object().type == 'light':
        read_layout(append=False)


    else:
        read_layout(append=True)


if __name__ == '__main__':
    run()