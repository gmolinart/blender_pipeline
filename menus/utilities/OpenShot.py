import bpy
from cgl.plugins.blender import lumbermill as lm
import os


def get_users(self, context):
    scene = bpy.types.Scene.scene_enum
    path_object = lm.LumberObject(get_shot_from_name(scene))

    users = os.listdir(path_object.split_after('task'))

    for i in users:

        if i == 'publish':
            users.remove(i)
            users.insert(0, "publish")

    value = [(users[i], users[i], '') for i in range(len(users))]

    return (value)


def get_items(self, context):
    from cgl.plugins.blender import lumbermill as lm
    import os

    scene = lm.scene_object()
    project = lm.LumberObject(scene.split_after('project'))
    proj_shots = project.copy(scope='shots', context='source')

    print('_______________SHOTS___________')

    sequences = os.listdir(proj_shots.path_root)

    # print(sequences)
    shots = []

    for seq in sequences:
        # print(seq)
        seq_path = os.path.join(proj_shots.path_root, seq)
        if os.path.isdir(seq_path):
            # print(seq_path)

            list = os.listdir(seq_path)
            for shot in list:
                if os.path.isdir(os.path.join(seq_path, shot)):
                    shot_dir = os.path.join(seq_path, shot)
                for task in os.listdir(shot_dir):

                    if os.path.isdir(os.path.join(shot_dir, task)):
                        shotid = '{} {} {}'.format(seq, shot, task)
                        if '.json' not in shotid:

                            shots.append((shotid, shotid, ''))
                        # print(22222222222)
                        print(shotid)

    return (shots)


def get_shot_from_name(keys=''):
    seq = keys.split(' ')[0]
    shot = keys.split(' ')[1]
    task = keys.split(' ')[3]

    current_scene = lm.scene_object()
    dict_ = {'company': current_scene.company,
             'context': 'source',
             'project': current_scene.project,
             'scope': 'assets',
             'seq': seq,
             'shot': shot,
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


def get_shot_from_name(keys=''):
    seq = keys.split(' ')[0]
    shot = keys.split(' ')[1]
    task = keys.split(' ')[2]
    user = keys.split(' ')[3]

    current_scene = lm.scene_object()
    dict_ = {'company': current_scene.company,
             'context': 'source',
             'project': current_scene.project,
             'scope': 'shots',
             'seq': seq,
             'shot': shot,
             'task': task,
             'user': user,
             'resolution': 'high'
             }

    path_object = lm.LumberObject(dict_)
    default_asset = path_object.latest_version()
    return default_asset


class DialogUser(bpy.types.Operator):
    bl_idname = "object.dialog_user"
    bl_label = "Please select user"

    users: bpy.props.EnumProperty(items=get_users)

    def execute(self, context):
        # my_users =  bpy.props.EnumProperty(items = split_string(self.my_string))

        path_object = get_shot_from_name(bpy.types.Scene.scene_enum.replace('publish', self.users))
        correctName = '%s_%s_%s.blend' % (path_object.seq,
                                          path_object.shot,
                                          path_object.task,
                                          )
        path_object = path_object.copy(filename=correctName)
        open_file = path_object.latest_version().copy(set_proper_filename=True).path_root

        message = 'selected {}'.format(open_file)
        lm.open_file(open_file)
        self.report({'INFO'}, message)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class OpenShot(bpy.types.Operator):
    bpy.utils.register_class(DialogUser)

    """
    imports latest version of selectd task
    """
    bl_idname = 'object.open_shot'
    bl_label = 'Open Shot'

    bl_property = "my_enum"
    my_enum = bpy.props.EnumProperty(items=get_items)

    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.my_enum)
        bpy.types.Scene.scene_enum = bpy.props.StringProperty(name=self.my_enum)
        bpy.types.Scene.scene_enum = self.my_enum + ' publish'
        bpy.ops.object.dialog_user('INVOKE_DEFAULT')

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OpenShot)


def unregister():
    bpy.utils.unregister_class(OpenShot)


if __name__ == "__main__":
    register()
    bpy.ops.object.open_shot('INVOKE_DEFAULT')

