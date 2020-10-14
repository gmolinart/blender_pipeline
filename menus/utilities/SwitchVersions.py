import bpy
from cgl.plugins.blender import lumbermill as lm




def get_items(self, context):
    from cgl.plugins.blender import lumbermill as lm
    import os

    path_object = lm.scene_object()

    versions = path_object.glob_project_element('version')
    version =versions.reverse()
    print(versions)

    value = [(versions[i], versions[i], '') for i in range(len(versions))]

    return (value)

class SwitchVersions(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.switch_versions'
    bl_label = 'Switch Versions'

    bl_property = "selected_versions"
    selected_versions = bpy.props.EnumProperty(items=get_items)

    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.selected_versions)
        new_user = lm.scene_object().copy(version=self.selected_versions).path_root
        lm.open_file(new_user)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}

