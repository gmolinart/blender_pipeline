import bpy
from cgl.plugins.blender import lumbermill as lm


def get_items(self, context):
    from cgl.plugins.blender import lumbermill as lm
    import os

    scene = selected_path_object()

    versions = scene.glob_project_element('version')
    print(versions)
    value = [(versions[i], versions[i], '') for i in range(len(versions))]

    return (value)


class SwitchSelectedVersion(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.switch_selected_version'
    bl_label = 'Switch Selected Version'

    bl_property = "versions"
    versions = bpy.props.EnumProperty(items=get_items)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.versions)
        new_version = lm.scene_object().copy(version=self.versions).latest_version().path_root
        # lm.open_file(new_version)
        switch_version(self.versions)
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


def switch_version(version):
    import os
    lumber_object = selected_path_object()
    latest_version = lumber_object.copy(version=version).path_root
    if os.path.isdir(lumber_object.copy(context='render', filename='').path_root):
        latest_version = lumber_object.copy(version=version, context='render').path_root

    library = bpy.context.object.instance_collection.library
    print(library)
    library.filepath = bpy.path.relpath(latest_version)
    library.reload()
    print(library.filepath + ' CHANGED')


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    print('Hello World!: button_template')


def register():
    bpy.utils.register_class(SwitchSelectedVersion)


def unregister():
    bpy.utils.unregister_class(SwitchSelectedVersion)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.switch_selected_version('INVOKE_DEFAULT')