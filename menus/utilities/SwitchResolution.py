import bpy
from cgl.plugins.blender import lumbermill as lm






def get_items(self, context):
    from cgl.plugins.blender import lumbermill as lm
    import os

    scene = lm.scene_object()

    resolution = scene.glob_project_element('resolution')
    print(resolution)

    value = [(resolution[i], resolution[i], '') for i in range(len(resolution))]

    return (value)


class SwitchResolution(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.switch_resolution'
    bl_label = 'Switch Resolution'

    bl_property = "selected_resolution"
    selected_resolution = bpy.props.EnumProperty(items=get_items)

    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.selected_resolution)
        new_user = lm.scene_object().copy(resolution=self.selected_resolution).path_root
        lm.open_file(new_user)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}





def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    print('Hello World!: button_template')

