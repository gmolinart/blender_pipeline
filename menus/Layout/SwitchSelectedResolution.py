import bpy
from cgl.plugins.blender import lumbermill as lm



def get_items(self, context):
    from cgl.plugins.blender import lumbermill as lm
    import os

    scene = selected_path_object()

    resolutions = scene.glob_project_element('resolution')
    print(resolutions)
    value = [(resolutions[i], resolutions[i], '') for i in range(len(resolutions))]

    return (value)



class SwitchSelectedResolution(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.switch_selected_resolution'
    bl_label = 'Switch Selected Resolution'


    bl_property = "resolutions"
    resolutions = bpy.props.EnumProperty(items=get_items)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.resolutions)
        new_resolution = lm.scene_object().copy(resolution=self.resolutions).path_root
        # lm.open_file(new_resolution)
        switch_resolution(self.resolutions)
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


def switch_resolution(resolution):
    import os
    lumber_object = selected_path_object()
    latest_resolution = lumber_object.copy(resolution=resolution).path_root
    if os.path.isdir(lumber_object.copy(context='render', filename='').path_root):
        latest_resolution = lumber_object.copy(resolution=resolution, context='render').path_root

    library = bpy.context.object.instance_collection.library
    print(library)
    library.filepath = bpy.path.relpath(latest_resolution)
    library.reload()
    print(library.filepath + ' CHANGED')


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    print('Hello World!: button_template')


def register():
    bpy.utils.register_class(SwitchSelectedResolution)


def unregister():
    bpy.utils.unregister_class(SwitchSelectedResolution)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.switch_selected_resolution('INVOKE_DEFAULT')