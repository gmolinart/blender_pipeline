import bpy
# from cgl.plugins.blender import lumbermill as lm

class SimpleController(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.simple_controller'
    bl_label = 'Simple Controller'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def simpleRigCreator():
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)

    selected = bpy.context.selected_objects
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    AssetName = bpy.path.basename(bpy.data.filepath).split('_')[1]

    for obj in selected:
        # ensure origin is centered on bounding box center
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        # create a cube for the bounding box
        bpy.ops.mesh.primitive_cube_add()
        # our new cube is now the active object, so we can keep track of it in a variable:
        bound_box = bpy.context.active_object

        # copy transforms
        bound_box.dimensions = obj.dimensions
        bound_box.name = '%s_Controller' % AssetName
        bound_box.location = obj.location
        bound_box.rotation_euler = obj.rotation_euler

        bound_box.rotation_euler[0] = 1.5708
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
        bpy.context.object.display_type = 'WIRE'
        #   bound_box.hide_viewport = True

        Armature = bpy.ops.object.armature_add(enter_editmode=False, location=obj.location)
        bpy.data.objects['Armature'].name = AssetName
        bpy.data.objects[AssetName].pose.bones["Bone"].name = 'MAIN_CTRL'
        bpy.data.objects[AssetName].pose.bones["MAIN_CTRL"].custom_shape = bound_box

        bpy.context.object.data.bones["MAIN_CTRL"].show_wire = True
        bpy.ops.object.select_all(action='DESELECT')
        bound_box.select_set(True)
        bpy.ops.object.delete(use_global=False)
        bpy.data.objects[AssetName].select_set(True)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def run():
    """
    Creates a simple box controller for rigging
    :return:
    """
    simpleRigCreator()

