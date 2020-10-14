import bpy
from cgl.plugins.blender import lumbermill as lm

class Defaultshader(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.defaultshader'
    bl_label = 'Defaultshader'

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

    def assignToon(context):
        def instanciate_group(nodes, group_name):
            group = nodes.new(type='ShaderNodeGroup')
            group.node_tree = bpy.data.node_groups[group_name]
            return group

        def assignToonShader(material):
            '''To do Handle if the material output doesnt exist'''
            toonShader = instanciate_group(material.node_tree.nodes, "ToonShader_2")
            node2 = material.node_tree.nodes['Material Output']
            material.node_tree.links.new(toonShader.outputs[0], node2.inputs[0])

        objects = bpy.context.selected_objects
        for obj in objects:
            if len(obj.material_slots) < 1:

                bpy.ops.object.material_slot_add()

                if obj.name not in bpy.data.materials:

                    mat = bpy.data.materials.new(obj.name)
                else:
                    mat = bpy.data.materials[obj.name]

                obj.data.materials[0] = mat
                mat.use_nodes = True

            for mat in obj.data.materials:
                if mat.name == '':
                    mat.name = obj.name

                matNodes = mat.node_tree.nodes

                assignToonShader(mat)
                if 'Principled BSDF' in matNodes:
                    matNodes.remove(matNodes['Principled BSDF'])
                # else:
                #     for n in matNodes:
                #         if n != material.node_tree.nodes['Material Output']:
                #             matNodes.remove(n)


    shaderPath = r'D:/COMPANIES/loneCoconut/render/MILVIO_CGL/assets/lib/TOONSCEENSETUP/shd/publish/001.000/high/lib_TOONSCEENSETUP_shd.blend'
    collection_name = 'ToonSceneSetup'
    # dict_ = {'company': 'loneCoconut',
    #          'context': 'render',
    #          'project': 'MILVIO',
    #          'scope': 'assets',
    #          'seq': 'lib',
    #          'shot': 'TOONSCEENSETUP',
    #          'task': 'shd',
    #          'user': 'publish',
    #          'resolution': 'high'}
    # shaderPath = lm.LumberObject(dict_)
    # print(shaderPath.latest_version().path_root)
    #
    # collection_name = shaderPath.shot

    if collection_name not in bpy.data.collections:

        # link all collections starting with 'MyCollection'
        with bpy.data.libraries.load(shaderPath, link=False) as (data_from, data_to):
            data_to.collections = [c for c in data_from.collections if c.startswith(collection_name)]

        # link collection to scene collection
        for coll in data_to.collections:
            if coll is not None:
                bpy.data.scenes['Scene'].collection.children.link(coll)

    else:
        print("Toon Shader Exist")


    assignToon(bpy.context)

