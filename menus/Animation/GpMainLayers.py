import bpy
# from cgl.plugins.blender import lumbermill as lm

class GpMainLayers(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.gp_main_layers'
    bl_label = 'Gp Main Layers'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    default_layers = ['MAIN', 'SECONDARY', 'STATIC']
    layers = []

    for i in bpy.context.object.data.layers:
        layers.append(i.info)

    for i in default_layers:
        if i not in layers:
            bpy.context.object.data.layers.new(i)

        else:
            print('{} already exists'.format(i))

    for i in bpy.context.object.data.layers:
        i.use_lights = False



