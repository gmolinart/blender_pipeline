import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils as utils
import os


def reorder_list(items, arg=''):
    """
    Reorders list in order of importance, putting rig
    :param items:
    :return:
    """

    if arg:

        for i in items:
            if i == arg:
                items.remove(i)
                items.insert(0, arg)

    return items


def get_task(self, context):
    scene = bpy.types.Scene.scene_enum

    path_object = lm.LumberObject(get_asset_from_name(scene))
    tasks = reorder_list(path_object.glob_project_element('task'), arg='rig')
    value = [(tasks[i], tasks[i], '') for i in range(len(tasks))]

    return (value)


def get_users(self, context):
    scene = bpy.types.Scene.scene_enum
    path_object = lm.LumberObject(get_asset_from_name(scene))

    user_list = path_object.glob_project_element('user')
    if not user_list:
        path_object= path_object.copy(task = 'rig')
        user_list = path_object.glob_project_element('user')
    users = reorder_list(user_list, arg='publish')

    value = [(users[i], users[i], '') for i in range(len(users))]

    return (value)

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

    if outFile == None:
        outFileObject = scene_object().copy(ext='json', task='lay', set_proper_filename=True).latest_version()
        outFile = outFileObject.path_root
    # outFile = scene_object().path_root.replace(scene_object().ext, 'json')

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

        else:
            print("__________________{} not found_____________".format(lumberObject.path_root))



def get_version(self, context):
    scene = bpy.types.Scene.scene_enum
    path_object = lm.LumberObject(get_asset_from_name(scene))

    versions = path_object.glob_project_element('version')
    version = versions.reverse()
    value = [(versions[i], versions[i], '') for i in range(len(versions))]
    return (value)


class DialogUserB(bpy.types.Operator):
    bl_idname = "object.dialog_user_c"
    bl_label = "Please select user, type and version"

    users: bpy.props.EnumProperty(items=get_users)
    task: bpy.props.EnumProperty(items=get_task)
    #version: bpy.props.EnumProperty(items=get_version)

    def execute(self, context):
        # my_users =  bpy.props.EnumProperty(items = split_string(self.my_string))

        path_object = get_asset_from_name(bpy.types.Scene.scene_enum.replace('publish', self.users))
        path_object = path_object.copy(task=self.task, set_proper_filename=True)
        path_object = path_object.latest_version().copy(set_proper_filename=True)
        render = path_object.copy(context='render')
        if os.path.isfile(render.path_root):
            path_object = render
        open_file = path_object.path_root

        message = 'selected {}'.format(open_file)
        try :
            bpy.ops.object.mode_set(mode='OBJECT')
        except RuntimeError:
            pass

        if os.path.isfile((open_file)):

            if  path_object.type == 'env':

                lm.import_file(open_file)
                if os.path.isfile(path_object.copy(ext='json').path_root):
                    read_layout(outFile=path_object.copy(ext='json').path_root, append=True)
                    bpy.ops.object.setup_collections()

            else:
                lm.import_file(open_file, snap_to_cursor=True)
            name = path_object.asset

            if path_object.type in ['char', ]:
                rig = '{}_rig'.format(path_object.asset)
                print(rig)
                objects = bpy.context.view_layer.objects
                objects.active = objects[name]
                bpy.ops.object.proxy_make(object=rig)
        else:
            lm.confirm_prompt(message= 'This file doesnt exist, please check for sync or review for errors')

        # if lm.scene_object().type is not 'env':
        #     bpy.ops.object.setup_collections()

        self.report({'INFO'}, message)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


bpy.utils.register_class(DialogUserB)


def get_items(self, context):
    from cgl.plugins.blender import lumbermill as lm
    import os

    scene = lm.scene_object()
    project = lm.LumberObject(scene.split_after('project'))
    char = project.copy(scope='assets', seq='char')

    assets = ['char', 'prop', 'lib', 'veh', 'env']
    asset_dic = {}

    for asset in assets:
        asset_dic.update({asset: project.copy(scope='assets', seq=asset)})

    list_base = []
    list = []

    for type in assets:

        if os.path.isdir(asset_dic[type].path_root):
            for i in os.listdir(asset_dic[type].path_root):
                list_base.append('{} {}'.format(i, type))

    dictionary = {}

    for i in list_base:
        list.append(i.split(' ')[0])

    dictionary = dict(map(str, x.split(' ')) for x in list_base)

    value = [('{} {}'.format(list[i], dictionary[list[i]]),
              '{} {}'.format(dictionary[list[i]],
                             '{}'.format(list[i])), '') for i in range(len(list))]
    return (value)


def get_asset_from_name(keys=''):
    name = keys.split(' ')[0]
    type = keys.split(' ')[1]
    user = keys.split(' ')[2]

    task = 'mdl'

    current_scene = lm.scene_object()
    dict_ = {'company': current_scene.company,
             'context': 'source',
             'project': current_scene.project,
             'scope': 'assets',
             'seq': type,
             'shot': name,
             'task': task,
             'user': user,
             'resolution': 'high'
             }

    path_object = lm.LumberObject(dict_)
    path_object.set_attr(filename='%s_%s_%s.%s' % (path_object.seq,
                                                   path_object.shot,
                                                   path_object.task,
                                                   current_scene.ext
                                                   ))
    default_asset = path_object.latest_version()
    return (default_asset)


class ImportAsset(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.import_asset'
    bl_label = 'Import Asset'

    bl_property = "my_enum"
    my_enum = bpy.props.EnumProperty(items=get_items)

    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.my_enum)
        bpy.types.Scene.scene_enum = bpy.props.StringProperty(name=self.my_enum)
        bpy.types.Scene.scene_enum = self.my_enum + ' publish'
        bpy.ops.object.dialog_user_c('INVOKE_DEFAULT')

        # lm.open_file(get_asset_from_name(self.my_enum).path_root)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ImportAsset)


def unregister():
    bpy.utils.unregister_class(ImportAsset)


if __name__ == "__main__":
    register()
    bpy.ops.object.import_asset('INVOKE_DEFAULT')