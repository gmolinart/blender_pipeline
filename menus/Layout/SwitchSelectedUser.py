import bpy
from cgl.plugins.blender import alchemy as alc
import os


def get_items(self, context):
    from cgl.plugins.blender import alchemy as alc
    import os

    bpy.ops.file.make_paths_absolute()
    scene = selected_path_object()

    users = scene.glob_project_element('user')
    print(users)
    value = [(users[i], users[i], '') for i in range(len(users))]

    return (value)


def get_collection_from_path_object(path_object):
    import bpy

    for i in bpy.data.collections:
        if i.library:

            if i.library.filepath == path_object.path_root:
                return i


class SwitchSelectedUser(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.switch_selected_user'
    bl_label = 'Switch Selected User'
    bl_property = "users"
    users = bpy.props.EnumProperty(items=get_items)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.users)
        new_user = alc.scene_object().copy(user=self.users).latest_version().path_root
        # alc.open_file(new_user)
        switch_user(self.users)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}


def selected_path_object():
    from pathlib import Path
    selection = bpy.context.selected_objects
    for obj in selection:
        if 'proxy' in obj.name:
            name = obj.name.split('_')[0]
        else:
            if '.' in obj.name:

                name = obj.name.split('.')[0]
            else:
                name = obj.name

        from cgl.plugins.blender.msd import path_object_from_source_path
        from cgl.plugins.blender.utils import selection

        lumber_object = path_object_from_source_path(obj['source_path'])
        return lumber_object


def switch_user(user):
    import os
    from cgl.plugins.blender.utils import get_scene_collection, get_object, load_library, purge_unused_data, \
        set_all_paths_relative
    from cgl.plugins.blender.msd import path_object_from_source_path

    selection = bpy.context.selected_objects
    set_all_paths_relative(False)
    for object in selection:

        library = object['source_path']
        lumber_object = path_object_from_source_path(library)
        latest_version = lumber_object.copy(user=user, context='render').latest_version()

        if latest_version.task == 'mdl':
            print(latest_version.path_root)
            load_library(latest_version)

            collection = get_collection_from_path_object(path_object=latest_version)
            print(collection)
            object.instance_collection = collection

        purge_unused_data()
        alc.confirm_prompt(message='{} update to {}'.format(latest_version.asset, latest_version.version))

        set_all_paths_relative(True)


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    print('Hello World!: button_template')


def register():
    bpy.utils.register_class(SwitchSelectedUser)


def unregister():
    bpy.utils.unregister_class(SwitchSelectedUser)


if __name__ == "__main__":
    register()

    # test call

    bpy.ops.object.switch_selected_user('INVOKE_DEFAULT')
