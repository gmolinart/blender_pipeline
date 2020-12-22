import bpy
from cgl.plugins.blender import lumbermill as lm

class ImportBaseMesh(bpy.types.Operator):
    """
    Imports base mesh from the asset/lib/baseMesh/ latest publishe
    """
    bl_idname = 'object.import_base_mesh'
    bl_label = 'Import Base Mesh'

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
    baseMesh = lm.scene_object().copy(asset='baseMesh', task='mdl', user='publish', latest=True,
                                      set_proper_filename=True, type='lib')
    print(baseMesh.path_root)

    lm.import_file(baseMesh.path_root)

    bpy.ops.object.make_local(type='ALL')

    base_mesh = bpy.data.objects['baseMesh']
    base_mesh.select_set(True)

    bpy.ops.object.duplicates_make_real()

    bpy.ops.object.select_all(action='DESELECT')
    base_mesh.select_set(True)

    bpy.ops.object.delete(use_global=False)

