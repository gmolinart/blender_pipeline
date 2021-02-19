import os

import bpy
from cgl.plugins.blender import alchemy as alc


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

    path_object = alc.PathObject(get_asset_from_name(scene))
    tasks = reorder_list(path_object.glob_project_element('task'), arg='rig')
    value = [(tasks[i], tasks[i], '') for i in range(len(tasks))]

    return (value)


def get_users(self, context):
    scene = bpy.types.Scene.scene_enum
    path_object = alc.PathObject(get_asset_from_name(scene))

    user_list = path_object.glob_project_element('user')
    if not user_list:
        path_object= path_object.copy(task = 'rig')
        user_list = path_object.glob_project_element('user')
    users = reorder_list(user_list, arg='publish')

    value = [(users[i], users[i], '') for i in range(len(users))]

    return (value)



def get_version(self, context):
    scene = bpy.types.Scene.scene_enum
    path_object = alc.PathObject(get_asset_from_name(scene))

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
            alc.reference_file(path_object.path_root, namespace=path_object.asset)

            name = path_object.asset

            if path_object.type in ['char', ]:
                rig = '{}_rig'.format(path_object.asset)
                print(rig)
                objects = bpy.context.view_layer.objects
                objects.active = objects['{}:rig'.format(name)]
                bpy.ops.object.proxy_make(object=rig)
        else:
            alc.confirm_prompt(message= 'This file doesnt exist, please check for sync or review for errors')

        # if alc.scene_object().type is not 'env':
        #     bpy.ops.object.setup_collections()

        self.report({'INFO'}, message)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


bpy.utils.register_class(DialogUserB)


def get_items(self, context):
    from cgl.plugins.blender import alchemy as alc
    import os

    scene = alc.scene_object()
    project = alc.PathObject(scene.split_after('project'))
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

    current_scene = alc.scene_object()
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

    path_object = alc.PathObject(dict_)
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

        # alc.open_file(get_asset_from_name(self.my_enum).path_root)
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