import bpy
from cgl.plugins.blender import lumbermill as lm
from collections import defaultdict


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
                list.append(i)

    dictionary = defaultdict(set)
    dictionary = dict(map(str, x.split(' ')) for x in list_base)

    value = [('{} {}'.format(list[i], dictionary[list[i]]),
              '{} {}'.format(dictionary[list[i]],
                             list[i]), '') for i in range(len(list))]

    return (value)


def get_asset_from_name(keys=''):
    name = keys.split(' ')[0]
    type = keys.split(' ')[1]

    if type in ['char', 'veh']:
        task = 'rig'


    else:
        task = 'mdl'

    current_scene = lm.scene_object()
    dict_ = {'company': current_scene.company,
             'context': 'source',
             'project': current_scene.project,
             'scope': 'assets',
             'seq': type,
             'shot': name,
             'task': task,
             'user': 'publish',
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


class OpenAsset(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.open_asset'
    bl_label = 'OpenAsset'
    bl_property = "my_enum"
    my_enum = bpy.props.EnumProperty(items=get_items)

    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.my_enum)
        lm.open_file(get_asset_from_name(self.my_enum).path_root)
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

    # test call
    bpy.ops.object.open_asset('INVOKE_DEFAULT')