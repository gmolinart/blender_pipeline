import bpy
from cgl.plugins.blender import lumbermill as lm
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


def get_users(self, context):
    import os
    scene = bpy.types.Scene.scene_enum
    path_object = lm.LumberObject(get_asset_from_name(scene))
    print(1111111111111)
    print(path_object.path_root)

    user_list = path_object.glob_project_element('user')

    if not user_list:
        if path_object.type == 'char':
            path_object = path_object.copy(task='rig')
            user_list = path_object.glob_project_element('user')
        else:
            users = os.listdir(path_object.copy(task='mdl').split_after('task'))

    users = reorder_list(user_list, arg='publish')
    print(users)

    value = [(users[i], users[i], '') for i in range(len(users))]

    return (value)


class DialogUserB(bpy.types.Operator):
    bl_idname = "object.dialog_user_b"
    bl_label = "Please select user"

    users: bpy.props.EnumProperty(items=get_users)

    def execute(self, context):
        # my_users =  bpy.props.EnumProperty(items = split_string(self.my_string))

        path_object = get_asset_from_name(bpy.types.Scene.scene_enum.replace('publish', self.users))
        correctName = '%s_%s_%s.blend' % (path_object.seq,
                                          path_object.shot,
                                          path_object.task,
                                          )
        path_object = path_object.copy(filename=correctName)
        open_file = path_object.latest_version().copy(set_proper_filename=True).path_root

        message = 'selected {}'.format(open_file)
        if os.path.isfile(open_file):
            lm.open_file(open_file)
        else:

            #lm.confirm_prompt(message='this file has an incorrect file name, consider  opening it and renaming it on the utils')
            #lm.LumberObject(open_file).show_in_folder()
            open_available_file(open_file)

        self.report({'INFO'}, message)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


bpy.utils.register_class(DialogUserB)


def open_available_file(path_object):
    import os
    print(3333333333)
    filename = lm.LumberObject(path_object).copy(filename='')
    print(filename.path_root)
    found = False
    files = os.listdir(filename.path_root)

    print(files)
    if files:
        for file in files:
            if file.endswith('.blend') and not found:
                found = True
                print(path_object)
                new_file = filename.copy(filename=file).path_root
                os.rename(new_file,path_object)
                lm.open_file(path_object)


    else:
        lm.confirm_prompt(message='No file found')


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
    import os
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
    if default_asset.type == 'char':
        default_asset = default_asset.copy(task='rig', set_proper_filename=True)

    if not os.path.isfile(default_asset.path_root):
        if default_asset.type == 'char':
            default_asset = path_object.copy(task='rig', set_proper_filename=True)

        else:
            default_asset = path_object.copy(task='mdl')
        # default_asset = default_asset.copy(task='rig', set_proper_filename=True)

    return (default_asset)


class OpenAsset(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.open_asset'
    bl_label = 'Open Asset'

    bl_property = "my_enum"
    my_enum = bpy.props.EnumProperty(items=get_items)

    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.my_enum)
        bpy.types.Scene.scene_enum = bpy.props.StringProperty(name=self.my_enum)
        bpy.types.Scene.scene_enum = self.my_enum + ' publish'
        bpy.ops.object.dialog_user_b('INVOKE_DEFAULT')

        # lm.open_file(get_asset_from_name(self.my_enum).path_root)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OpenAsset)


def unregister():
    bpy.utils.unregister_class(OpenAsset)


if __name__ == "__main__":
    register()

    bpy.ops.object.open_asset('INVOKE_DEFAULT')
