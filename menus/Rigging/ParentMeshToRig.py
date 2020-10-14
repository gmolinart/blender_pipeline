import bpy
from cgl.plugins.blender import lumbermill as lm


class ParentMeshToRig(bpy.types.Operator):
    """
    takes in group of mesh and adds it ot the rig .
    """
    bl_idname = 'object.parent_mesh_to_rig'
    bl_label = 'Parent Mesh To Rig'
    assetName = bpy.props.StringProperty()

    def execute(self, context):
        run(self.assetName)
        return {'FINISHED'}


def unlink_from_non_asset_collections(obj, assetName=None):
    if not assetName:
        assetName = lm.scene_object().shot

    try:
        bpy.data.collections[assetName].objects.link(obj)

    except(RuntimeError):
        pass

    for collection in obj.users_collection:
        if collection.name != assetName:
            collection.objects.unlink(obj)


def create_mesh_group(meshGroupName, rig):
    try:

        meshGrp = bpy.data.objects[meshGroupName]
    except(KeyError):
        meshGrp = bpy.data.objects.new(meshGroupName, None)
        bpy.context.collection.objects.link(meshGrp)
        meshGrp.parent = rig

        unlink_from_non_asset_collections(meshGrp)
    return meshGrp


def parent_mesh_to_rig(assetName=''):
    if not assetName:
        assetName = lm.scene_object().shot

    rigname = '{}_rig'.format(assetName)
    rig = bpy.data.objects[rigname]
    meshGroupName = '{}_mesh_grp'.format(assetName)
    meshGrp = create_mesh_group(meshGroupName, rig)

    for obj in bpy.data.objects:

        if 'cs_' not in obj.name:
            if obj.type == "MESH":
                if any([modifier for modifier in obj.modifiers if modifier.type == "ARMATURE"]):
                    print(111111111111111111)
                    print(obj)

                    print(obj.name)
                    if not obj.parent == meshGrp:

                        obj.parent = meshGrp
                        obj.matrix_parent_inverse = meshGrp.matrix_world.inverted()

                        unlink_from_non_asset_collections(obj)

                for collection in obj.users_collection:
                    if collection.name != assetName:
                        collection.objects.unlink(obj)


def run(assetName=''):
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    parent_mesh_to_rig(assetName)
    print('objects re parented')
