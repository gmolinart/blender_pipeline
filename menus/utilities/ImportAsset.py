import os

import bpy
from cgl.plugins.blender import alchemy as alc
from cgl.plugins.blender.tasks.lay import import_rig
from cgl.plugins.blender.tasks import lay
from importlib import reload
from cgl.plugins.blender.utils import get_layer

reload(lay)


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
        path_object = path_object.copy(task='rig')
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


def get_variant(self, context):
    scene = bpy.types.Scene.scene_enum
    path_object = alc.PathObject(get_asset_from_name(scene))

    versions = path_object.glob_project_element('variant')
    version = versions.reverse()
    value = [(versions[i], versions[i], '') for i in range(len(versions))]
    return (value)


class DialogUserB(bpy.types.Operator):
    bl_idname = "object.dialog_user_c"
    bl_label = "Please select user, type and version"

    users: bpy.props.EnumProperty(items=get_users)
    task: bpy.props.EnumProperty(items=get_task)
    variant: bpy.props.EnumProperty(items=get_variant)
    # version: bpy.props.EnumProperty(items=get_version)
    from cgl.plugins.blender.utils import get_object, parent_object

    def execute(self, context):

        # my_users =  bpy.props.EnumProperty(items = split_string(self.my_string))

        path_object = get_asset_from_name(bpy.types.Scene.scene_enum.replace('publish', self.users))
        path_object = path_object.copy(task=self.task, variant=self.variant, set_proper_filename=True)
        path_object = path_object.latest_version().copy(set_proper_filename=True)
        render = path_object.copy(context='render')

        if os.path.isfile(render.path_root):
            path_object = render
        open_file = path_object.path_root

        message = 'selected {}'.format(open_file)

        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except RuntimeError:
            pass

        if os.path.isfile((open_file)):
            from cgl.core.path import PathObject
            file_to_be_imported = PathObject(open_file)
            if file_to_be_imported.task == 'bndl':
                from cgl.plugins.blender.tasks import bndl
                bndl.bundle_import(file_to_be_imported.msd_path)
                return

            if path_object.type in ['char', ] and path_object.task == 'rig':
                print(path_object.path_root)
                object = lay.import_rig(path_object)


            else:
                from cgl.plugins.blender.utils import get_object, parent_object, get_scene_object
                from cgl.plugins.blender import alchemy as alc
                object = alc.reference_file(path_object.path_root)
                main = get_layer('MAIN')

                if not main :
                    try:
                        main = get_scene_object()
                        parent_object(object, main)
                    except:
                        alc.confirm_prompt('please click on build')
            print(object)
            cursor = bpy.context.scene.cursor.location
            print(object.location)
            print(cursor)
            object.location = cursor


        else:
            alc.confirm_prompt(message='This file doesnt exist, please check for sync or review for errors')

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
    char = project.copy(scope='assets', seq='char', branch=scene.branch)

    assets = ['char', 'prop', 'lib', 'veh', 'env']
    asset_dic = {}

    for asset in assets:
        asset_dic.update({asset: project.copy(scope='assets', seq=asset, branch=scene.branch)})

    list_base = []
    list = []

    for type in assets:
        path_root = asset_dic[type].path_root
        print(path_root)
        if os.path.isdir(path_root):
            print(path_root)

            for i in os.listdir(path_root):
                list_base.append('{} {}'.format(i, type))

    dictionary = {}
    print(dictionary)

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
             'branch': current_scene.branch,
             'variant': 'default',
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