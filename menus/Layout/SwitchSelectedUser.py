import bpy
from cgl.plugins.blender import lumbermill as lm
import os


def get_items(self, context):
    from cgl.plugins.blender import lumbermill as lm
    import os

    bpy.ops.file.make_paths_absolute()
    scene = selected_path_object()

    users = scene.glob_project_element('user')
    print(users)
    value = [(users[i], users[i], '') for i in range(len(users))]

    return (value)


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
        new_user = lm.scene_object().copy(user=self.users).latest_version().path_root
        # lm.open_file(new_user)
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
        library = bpy.context.object.instance_collection.library
        library_path = bpy.path.abspath(library.filepath)
        filename = Path(bpy.path.abspath(library_path)).__str__()
        lumber_object = lm.LumberObject(filename)
        lumber_object = lumber_object.copy(context='source')
        return lumber_object


def switch_user(user):
    import os
    lumber_object = selected_path_object()
    latest_version = lumber_object.copy(user=user).latest_version()
    print(1111111111111)
    # print(latest_version)
    if os.path.isdir(latest_version.copy(context='render', filename='').path_root):
        latest_version = latest_version.copy(context='render')

    library = bpy.context.object.instance_collection.library
    library.filepath = latest_version.path_root
    bpy.ops.file.make_paths_relative()
    library.reload()

    print(library.filepath + ' CHANGED')


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