import bpy
import re


# from cgl.plugins.blender import lumbermill as lm

class CleanupWeights(bpy.types.Operator):
    """
    deletes vertex groups with no verteces in them
    """
    bl_idname = 'object.cleanup_weights'
    bl_label = 'Cleanup Weights'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}

def remove_unused_weights():

    ob = bpy.context.active_object
    ob.update_from_editmode()

    vgroup_used = {i: False for i, k in enumerate(ob.vertex_groups)}
    vgroup_names = {i: k.name for i, k in enumerate(ob.vertex_groups)}

    for v in ob.data.vertices:
        for g in v.groups:
            if g.weight > 0.0:
                vgroup_used[g.group] = True
                vgroup_name = vgroup_names[g.group]
                armatch = re.search('((.R|.L)(.(\d){1,}){0,1})(?!.)', vgroup_name)
                if armatch != None:
                    tag = armatch.group()
                    mirror_tag = tag.replace(".R", ".L") if armatch.group(2) == ".R" else tag.replace(".L", ".R")
                    mirror_vgname = vgroup_name.replace(tag, mirror_tag)
                    for i, name in sorted(vgroup_names.items(), reverse=True):
                        if mirror_vgname == name:
                            vgroup_used[i] = True
                            break
    for i, used in sorted(vgroup_used.items(), reverse=True):
        if not used:
            ob.vertex_groups.remove(ob.vertex_groups[i])

def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    remove_unused_weights()
