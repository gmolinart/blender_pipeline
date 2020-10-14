import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import lumbermill as lm
import os


def get_items(self, context):


    scene = lm.scene_object()

    users = scene.glob_project_element('user')
    print(users)

    value = [(users[i], users[i], '') for i in range(len(users))]

    return (value)


class SwitchUsers(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.switch_users'
    bl_label = 'Switch Users'
    bl_property = "my_enum"
    my_enum = bpy.props.EnumProperty(items=get_items)

    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.my_enum)
        new_user = lm.scene_object().copy(user=self.my_enum).latest_version().path_root
        lm.open_file(new_user)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}

