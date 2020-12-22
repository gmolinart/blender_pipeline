import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils as utils


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
    from cgl.plugins.blender.lumbermill import scene_object, LumberObject, import_file
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
            lumberObject = LumberObject(pathToFile)

            print(pathToFile)

            if lumberObject.filename_base in bpy.data.libraries:
                lib = bpy.data.libraries[lumberObject.filename]
                bpy.data.batch_remove(ids=([lib]))
                import_file(lumberObject.path_root, linked=False, append=True)
                bpy.data.ojects[lumberObject.asset].select_set(True)
                bpy.ops.object.unlink_asset()
            else:
                import_file(lumberObject.path_root, linked=False, append=True)

        for p in data:
            print(p)
            data_path = data[p]['source_path']
            blender_transform = data[p]['blender_transform']

            transform_data = []
            for value in blender_transform:
                transform_data.append(float(value))

            pathToFile = os.path.join(scene_object().root, data_path)
            lumberObject = LumberObject(pathToFile)
            obj = bpy.data.objects.new(p, None)
            bpy.context.collection.objects.link(obj)
            obj.instance_type = 'COLLECTION'
            if lumberObject.asset in bpy.data.collections:

                obj.instance_collection = bpy.data.collections[lumberObject.asset]

                location = (transform_data[0], transform_data[1], transform_data[2])
                obj.location = location

                rotation = (transform_data[3], transform_data[4], transform_data[5])
                obj.rotation_euler = rotation

                scale = (transform_data[6], transform_data[7], transform_data[8])
                obj.scale = scale

                if lumberObject.type in ['char', ]:

                    if append:
                        print("___________creating proxy rig for {}____________".format(lumberObject.asset))
                        rig = '{}_rig'.format(lumberObject.asset)
                        print(rig)
                        objects = bpy.context.view_layer.objects
                        bpy.context.view_layer.objects.active = objects[lumberObject.asset]
                        bpy.ops.object.proxy_make(object=rig)

                        if 'blender_action_path' in data[p]:
                            anim_path = data[p]['blender_action_path']
                            path_to_anim = os.path.join(scene_object().root, anim_path)
                            print(path_to_anim)
                            lm.import_file(path_to_anim, type='ANIM', collection_name=data[p]['blender_action'],
                                           linked=False)

            else:
                print("__________________{} not found_____________".format(lumberObject.path_root))
    else:
        print("_____________NO LAYOUT FOUND__________")

class ReadLayoutFromSelected(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.read_layout_from_selected'
    bl_label = 'Read Layout From Selected'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def return_asset_name(object):
    if 'proxy' in object.name:
        name = object.name.split('_')[0]
        return name

    else:
        if '.' in object.name:

            name = object.name.split('.')[0]
        else:
            name = object.name

        return name


def get_lib_from_object(object):
    if not object.is_instancer:
        object = bpy.data.object[return_asset_name(object)]
    library = object.instance_collection.library
    if not library:
        library = bpy.data.libraries['env_{}_mdl.blend'.format(return_asset_name(object))]
    return (library)


def return_lib_path(library):
    from pathlib import Path
    print(library)
    library_path = bpy.path.abspath(library.filepath)
    filename = Path(bpy.path.abspath(library_path)).__str__()
    return (filename)


def run():
    import os
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    object = bpy.context.object

    if object:
        library = get_lib_from_object(object)
        path = return_lib_path(library)
        path_object = lm.LumberObject(path)
        json = path_object.copy(ext='json').path_root
        if os.path.isfile(json):
            read_layout(outFile=json)
            bpy.ops.object.setup_collections()

        else:
            lm.confirm_prompt(message='no layout file found')
    else:
        lm.confirm_prompt(message='please select an object')

