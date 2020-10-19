import os
import bpy
from cgl.plugins.blender import lumbermill as lm
from shutil import copyfile

def get_name_from_user():
    from cgl.core.config import app_config
    import getpass

    CONFIG = app_config()
    user = getpass.getuser().lower()
    current_user = CONFIG['project_management']['ftrack']['users'][user]['first']
    print(current_user)
    return current_user


def get_items(self, context):
    from cgl.plugins.blender import lumbermill as lm
    scene = lm.scene_object()

    users = scene.glob_project_element('user')
    current_user = get_name_from_user()
    if current_user not in users:
        users.append(current_user)
    print(users)

    value = [(users[i], users[i], '') for i in range(len(users))]

    return (value)


class CopyToUser(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.copy_to_user'
    bl_label = 'Copy To User'
    bl_property = "my_enum"
    my_enum = bpy.props.EnumProperty(items=get_items)

    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.my_enum)
        new_user = lm.scene_object()

        user_version = new_user.copy(user=self.my_enum)
        user_version_dir = user_version.copy(filename='')
        new_version = user_version_dir.new_minor_version_object()
        if os.path.isdir(new_version.path_root):
            new_version = new_version.new_minor_version_object()

        os.makedirs(new_version.path_root)
        lm.save_file_as(new_version.copy(set_proper_filename=True).path_root)
        lm.open_file(new_version.copy(set_proper_filename=True).path_root)
        if os.path.isfile(lm.scene_object().copy(extension = 'json').path_root):
            print("______________Json File Saved____________")
            copyfile(lm.scene_object().copy(extension = 'json').path_root,
                     new_version.copy(set_proper_filename=True,ext = 'json').path_root)
        else:
            print("______________No Json File on: ____________")
            print(lm.scene_object().copy(extension = 'json').path_root)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(CopyToUser)


def unregister():
    bpy.utils.unregister_class(CopyToUser)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.copy_to_user('INVOKE_DEFAULT')