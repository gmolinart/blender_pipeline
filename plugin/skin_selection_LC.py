bl_info = {
    "name": "Skin Selection",
    "author": "Artell",
    "version": (1, 93, 10),
    "blender": (2, 80, 0),
    "location": "Toolbar (T) > Animation > Skin Selection",
    "description": "Selection of the controller bones from the mesh surface",
    "tracker_url": "",
    "category": "Animation"}

import bpy, time, bmesh
import gpu, bgl, blf
from gpu_extras.batch import *
import gpu_extras
from random import random
import numpy as np
from mathutils import *
from bpy_extras import *
from bpy_extras.view3d_utils import location_3d_to_region_2d as loc3d2d


###########################################################################################
# OP FUNCTIONS
def set_active_object(object_name):
    bpy.context.view_layer.objects.active = bpy.data.objects[object_name]
    try:  # the object may not be in the view layer (proxy case?)
        bpy.data.objects[object_name].select_set(state=1)
    except:
        pass


def _ss_add_vgroup(self):
    scene = bpy.context.scene
    context = bpy.context
    vname = scene.skin_sel_vgroup1[:-2]
    side = scene.skin_sel_vgroup1[-2:]

    if scene.skin_sel_vgroup2 != "":
        vname += ", " + scene.skin_sel_vgroup2[:-2]

    if scene.skin_sel_vgroup3 != "":
        vname += ", " + scene.skin_sel_vgroup3[:-2]

    if context.active_object.vertex_groups.get("fs: " + vname + side) == None:
        context.active_object.vertex_groups.new(name="fs: " + vname + side)
    else:
        self.report({'ERROR'}, "Vertex group already created for this bones set:" + "\nfs: " + vname + side)


def _ss_pick_controller(value):
    scene = bpy.context.scene
    context = bpy.context

    if value == 1:
        context.scene.skin_sel_vgroup1 = bpy.context.active_pose_bone.name
    if value == 2:
        context.scene.skin_sel_vgroup2 = bpy.context.active_pose_bone.name
    if value == 3:
        context.scene.skin_sel_vgroup3 = bpy.context.active_pose_bone.name


def _ss_mirror_vgroup():
    context = bpy.context
    obj = context.active_object
    base_name = obj.vertex_groups[obj.vertex_groups.active_index].name
    # check if mirror mod
    mirror_mod = False
    for mod in obj.modifiers:
        if mod.type == "MIRROR":
            mirror_mod = True
            break

    bpy.ops.object.vertex_group_copy()

    v_group_idx = obj.vertex_groups.active_index
    vgroup_name = obj.vertex_groups[v_group_idx].name
    vgroup_list = vgroup_name[3:].split(',')
    final_name = "fs: "
    right_sides = [".r,", "_r"]
    left_sides = [".l", "_l"]

    # clear weights if mirror
    if mirror_mod:
        if base_name[-2:].lower() in right_sides + left_sides:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.vertex_group_remove_from()
            bpy.ops.object.mode_set(mode='OBJECT')

    for i, bone_name in enumerate(vgroup_list):
        bone_name = bone_name.strip()
        side = "left"
        if bone_name[-2:].lower() in right_sides:
            side = "right"

        # _copy delete
        bone_name = bone_name.replace("_copy", "")

        if side == "left":
            # left to right
            if bone_name[-2:] == ".l":
                bone_name = bone_name[:-2] + ".r"

            elif bone_name[-2:] == ".L":
                bone_name = bone_name[:-2] + ".R"

            elif bone_name[-2:] == "_L":
                bone_name = bone_name[:-2] + "_R"

            elif bone_name[-2:] == "_l":
                bone_name = bone_name[:-2] + "_r"
        else:
            # right to left
            if bone_name[-2:] == ".r":
                bone_name = bone_name[:-2] + ".l"

            if bone_name[-2:] == ".R":
                bone_name = bone_name[:-2] + ".L"

            if bone_name[-2:] == "_R":
                bone_name = bone_name[:-2] + "_L"

            if bone_name[-2:] == "_r":
                bone_name = bone_name[:-2] + "_l"

        if i < len(vgroup_list) - 1:
            final_name += bone_name + ", "
        else:
            final_name += bone_name

    bpy.ops.object.mode_set(mode='OBJECT')

    # check if a mirror group already exists, delete it
    if obj.vertex_groups.get(final_name) != None:
        obj.vertex_groups.remove(obj.vertex_groups[final_name])

    # assign mirrored name
    obj.vertex_groups[vgroup_name].name = final_name

    # mirror
    bpy.ops.object.vertex_group_mirror(flip_group_names=False, all_groups=False, use_topology=False,
                                       mirror_weights=True)


###########################################################################################
# FUNCTIONS

def get_object_and_face_mouse(context, event, self):
    scene = context.scene
    raycast_type = "scene"

    if raycast_type == "scene":
        ray_direction = self._ray_target - self._ray_origin
        success, location, normal, face_index, object, mat = bpy.context.scene.ray_cast(bpy.context.view_layer,
                                                                                        self._ray_origin, ray_direction)

    if raycast_type == "object":
        matrix_inv = self.current_mesh.matrix_world.inverted()
        ray_origin_obj = matrix_inv @ self._ray_origin
        ray_target_obj = matrix_inv @ self._ray_target
        ray_direction_obj = ray_target_obj - ray_origin_obj
        obj_eval = context.evaluated.objects.get(self.current_mesh.name, None)
        if obj_eval:
            success, location, normal, face_index = obj_eval.ray_cast(ray_origin_obj, ray_direction_obj)

    if face_index and object:
        if object.find_armature():  # only skinned objects
            return object, face_index

    return None, None


def search_value_in_dict(dict, value_searched):
    # search the value in dict and returns the key
    for key in dict:
        if value_searched in dict[key]:
            return key
    return None


def end_skin_select(context, self):
    if self.draw_handler:
        print("remove handler")
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')
    if self.text_draw_handler:
        bpy.types.SpaceView3D.draw_handler_remove(self.text_draw_handler, 'WINDOW')
    # context.window_manager.event_timer_remove(self.timer_handler)

    self.draw_handle = None
    self.draw_event = None

    # restore overlays
    if self.show_overlay:
        bpy.context.space_data.overlay.show_bones = self.show_overlay
        bpy.context.space_data.overlay.show_extras = self.show_overlay

    # restore selection
    # restrict selection to armature
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.show_object_select_mesh = True
                    space.show_object_select_light = True
                    space.show_object_select_empty = True
                    space.show_object_select_camera = True

    context.scene.skin_sel_active = False
    print("End modal")


def map_input_keys(_event, self):
    context = bpy.context
    if context.scene.skin_sel_second_input == "ALT":
        self.second_input = _event.alt
    elif context.scene.skin_sel_second_input == "SHIFT":
        self.second_input = _event.shift
    elif context.scene.skin_sel_second_input == "CTRL":
        self.second_input = _event.ctrl

    if context.scene.skin_sel_third_input == "ALT":
        self.third_input = _event.alt
    elif context.scene.skin_sel_third_input == "SHIFT":
        self.third_input = _event.shift
    elif context.scene.skin_sel_third_input == "CTRL":
        self.third_input = _event.ctrl

    if (context.scene.skin_sel_second_input == "ALT" and context.scene.skin_sel_third_input == "SHIFT") or (
            context.scene.skin_sel_second_input == "SHIFT" and context.scene.skin_sel_third_input == "ALT"):
        self.multiple_input = _event.ctrl
    elif (context.scene.skin_sel_second_input == "CTRL" and context.scene.skin_sel_third_input == "SHIFT") or (
            context.scene.skin_sel_second_input == "SHIFT" and context.scene.skin_sel_third_input == "CTRL"):
        self.multiple_input = _event.alt
    elif (context.scene.skin_sel_second_input == "CTRL" and context.scene.skin_sel_third_input == "ALT") or (
            context.scene.skin_sel_second_input == "ALT" and context.scene.skin_sel_third_input == "CTRL"):
        self.multiple_input = _event.shift


def build_mesh_data(self):
    # cache mesh data for faster access
    if self.current_mesh:
        # mesh = self.current_mesh.to_mesh(depsgraph=bpy.context.evaluated_depsgraph_get(),
        # preserve_all_data_layers=True)
        # mesh = self.current_mesh.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
        deps = bpy.context.evaluated_depsgraph_get()
        object_eval = self.current_mesh.evaluated_get(deps)
        mesh = object_eval.to_mesh(preserve_all_data_layers=True, depsgraph=bpy.context.evaluated_depsgraph_get())
    else:
        return

    ob_data = self.current_mesh.data
    vgroup_active_index = self.current_mesh.vertex_groups.active_index

    print('[' + self.current_mesh.name + ']')
    print("Build faces...")
    faces_groups_dict = {}
    start_time = time.time()
    # build the faces groups from vertex groups
    method = 2

    if method == 1:  # older method, slower
        for vgroup in self.current_mesh.vertex_groups:
            if not (vgroup.name[:3] == "fs_" or vgroup.name[:3] == "fs:"):
                continue
            # print(vgroup.name)
            polys_in = []
            for poly in mesh.polygons:
                all_face_verts_belong = True
                for vi in poly.vertices:
                    vert = mesh.vertices[vi]
                    vert_groups_index = [vg.group for vg in vert.groups]
                    if not (vgroup.index in vert_groups_index):
                        all_face_verts_belong = False
                        break
                    else:
                        for grp in vert.groups:
                            if grp.weight != 1:
                                continue
                            try:
                                grp_name = self.current_mesh.vertex_groups[grp.group].name
                            except:
                                continue
                            if grp_name == vgroup.name:
                                if grp.weight != 1:
                                    all_face_verts_belong = False
                                break

                if all_face_verts_belong:
                    if not poly in polys_in:
                        polys_in.append(poly)
                        # print("appended polys_in")

            faces_groups_dict[vgroup.name] = [i.index for i in polys_in]

    elif method == 2:  # newest method, faster
        # skip meshes that don't contain fs groups
        found_fs_group = False
        for vgroup in self.current_mesh.vertex_groups:
            if vgroup.name.startswith("fs_") or vgroup.name.startswith("fs:"):
                found_fs_group = True
                break

        if found_fs_group:
            for poly in mesh.polygons:
                poly_vgroups = {}

                for vi in poly.vertices:
                    vert = mesh.vertices[vi]
                    for grp in vert.groups:
                        grp_index = grp.group
                        group_name = self.current_mesh.vertex_groups[grp_index].name
                        if group_name.startswith("fs:") or group_name.startswith("fs_"):
                            if not group_name in poly_vgroups:
                                poly_vgroups[group_name] = 1
                            else:
                                poly_vgroups[group_name] += 1

                for grp_name in poly_vgroups:
                    if poly_vgroups[grp_name] == len(poly.vertices):
                        if not grp_name in faces_groups_dict:
                            faces_groups_dict[grp_name] = [poly.index]
                        else:
                            list = faces_groups_dict[grp_name]
                            list.append(poly.index)
                            faces_groups_dict[grp_name] = list

    print("Built in", str(round(time.time() - start_time, 2)), "seconds")
    print("Face group dict length:", len(faces_groups_dict))
    # print("Faces_groups_dict:")
    # print(self.faces_groups_dict)

    print("Build vertices and indices...")
    start_time = time.time()
    # build the vertices and indices groups dicts
    vertex_groups_dict = {}
    indices_groups_dict = {}
    for vertex_group_name in faces_groups_dict:
        # print("vertex group name", vertex_group_name)
        # vgroup = self.current_mesh.vertex_groups.get(vertex_group_name)
        list_total_indices = []  # [[0,1,2],[0,2,3]...] list of vertex indices making triangles
        list_total_verts = []  # [171,177,5...] list of all vertex indices
        for active_poly_index in faces_groups_dict[vertex_group_name]:
            # print("active poly index", active_poly_index)
            # triangulate and store indices
            active_poly = mesh.polygons[active_poly_index]
            count_v = 0
            indice_pack = []  # [[0,1,2],[0,3,4]...] list of vertex indices making triangles in the current polygons
            indice_tri = []  # [0,1,2] triplet list of vertex indices making the current triangle
            last_index = None
            for vi in active_poly.vertices:
                # print("vertice...", vi)
                # store vertices dict
                if not vi in list_total_verts:
                    list_total_verts.append(vi)
                # store indices dict
                if len(indice_pack) == 0:
                    indice_tri.append(list_total_verts.index(vi))
                    # we append the index of the vert *being in the group vert list*, not the actual index
                    count_v += 1
                    if count_v == 3:
                        indice_pack.append(indice_tri)
                        last_index = list_total_verts.index(vi)
                        indice_tri = []
                        count_v = 0
                else:
                    indice_pack.append([indice_pack[0][0], last_index, list_total_verts.index(vi)])
                    last_index = vi

            list_total_indices += indice_pack

        # self.indices_groups_dict[vertex_group_name] = list_total_indices
        # self.vertex_groups_dict[vertex_group_name] = list_total_verts
        indices_groups_dict[vertex_group_name] = list_total_indices
        vertex_groups_dict[vertex_group_name] = list_total_verts

    self.objects_data[self.current_mesh.name] = {"vertex_groups_dict": vertex_groups_dict,
                                                 "indices_groups_dict": indices_groups_dict,
                                                 "faces_groups_dict": faces_groups_dict}

    print("Built in", str(round(time.time() - start_time, 2)), "seconds")
    # clear temp data
    object_eval.to_mesh_clear()
    """  
    print("Indices_groups_dict:")
    for i in self.indices_groups_dict:
        print(i, self.indices_groups_dict[i])
    """


###########################################################################################
# CLASSES
class SS_OT_mirror_vgroup(bpy.types.Operator):
    """Mirror the selected vertex group name and weights (if symmetrical model)"""
    bl_idname = "id.ss_mirror_vgroup"
    bl_label = "ss_mirror_vgroup"

    @classmethod
    def poll(cls, context):
        if bpy.context.active_object:
            if bpy.context.active_object.type == 'MESH':
                return True

    def execute(self, context):
        use_global_undo = context.preferences.edit.use_global_undo
        context.preferences.edit.use_global_undo = False

        try:
            _ss_mirror_vgroup()

        finally:
            context.preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}


class SS_OT_add_vgroup(bpy.types.Operator):
    """ Create a vertex group for the bone set above"""
    bl_idname = "id.ss_add_vgroup"
    bl_label = "ss_add_vgroup"

    @classmethod
    def poll(cls, context):
        if bpy.context.active_object:
            if bpy.context.active_object.type == 'MESH':
                return True

    def execute(self, context):
        use_global_undo = context.preferences.edit.use_global_undo
        context.preferences.edit.use_global_undo = False

        try:
            _ss_add_vgroup(self)

        finally:
            context.preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}


class SS_OT_pick_controller(bpy.types.Operator):
    """Pick the selected bone controller for this set"""
    bl_idname = "id.ss_pick_controller"
    bl_label = "ss_pick_controller"

    value: bpy.props.IntProperty(default=0)

    @classmethod
    def poll(cls, context):
        if context.mode == 'POSE':
            return True

    def execute(self, context):
        use_global_undo = context.preferences.edit.use_global_undo
        context.preferences.edit.use_global_undo = False

        try:
            _ss_pick_controller(self.value)
        finally:
            context.preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}


class SS_OT_skins_selection(bpy.types.Operator):
    """Bones Skin Selection"""

    bl_idname = "id.skin_selection"
    bl_label = "skin_selection"

    def __init__(self):
        self.current_mesh = None
        self.current_vgroup = None
        self.current_bone = None
        self.armature = None
        self.highlight_color = (
            bpy.context.scene.skin_sel_color[0], bpy.context.scene.skin_sel_color[1],
            bpy.context.scene.skin_sel_color[2],
            bpy.context.scene.skin_sel_alpha)
        self.backface_cull = None
        self.objects_data = {}
        # self.faces_groups_dict = {}
        # self.vertex_groups_dict = {}
        # self.indices_groups_dict = {}

        self._view_vector = None
        self._ray_origin = None
        self._ray_target = None

        self.show_overlay = None

        self.shader = gpu.shader.from_builtin('3D_SMOOTH_COLOR')

        self.draw_handler = None
        self.text_draw_handler = None
        self.build_data = False

        self.text_report = ""
        self.is_mouse_moving = "False"
        self.second_input = None
        self.third_input = None
        self.multiple_input = None

    def get_rig_name(self, context):

        return rigname

    def draw_text(self, context):
        # draw some text
        font_id = 0
        rigname = bpy.context.object.name
        rigname = rigname.replace('_proxy', '')
        blf.size(font_id, 90, 15)
        blf.position(font_id, 50, 120, 0)
        blf.draw(font_id, rigname)
        blf.size(font_id, 80, 15)
        blf.position(font_id, 50, 100, 0)
        blf.draw(font_id, self.text_report)

    def draw(self, context):
        # only draw highlight if no transform are running (mouse moving is False then) and no animation playback
        # for performance reasons

        if self.current_mesh and not bpy.context.screen.is_animation_playing and self.is_mouse_moving == "True":
            if self.current_mesh.name in self.objects_data and self.current_vgroup:
                if self.current_vgroup[:3] == 'fs_' or self.current_vgroup[:3] == 'fs:':
                    # start_time1 = time.time()
                    mesh_evaluation_method = 1

                    if mesh_evaluation_method == 0:
                        mesh_baked = self.current_mesh.to_mesh(preserve_all_data_layers=False,
                                                               depsgraph=bpy.context.evaluated_depsgraph_get())
                        _verts = mesh_baked.vertices
                    else:
                        """
                        mesh_baked = bmesh.new()
                        depsg = bpy.context.evaluated_depsgraph_get()
                        mesh_baked.from_object(self.current_mesh, depsg, deform=True, face_normals=False)
                        mesh_baked.verts.ensure_lookup_table()
                        _verts = mesh_baked.verts
                        """
                        deps = bpy.context.evaluated_depsgraph_get()
                        object_eval = self.current_mesh.evaluated_get(deps)
                        mesh_baked = object_eval.to_mesh(preserve_all_data_layers=False,
                                                         depsgraph=bpy.context.evaluated_depsgraph_get())
                        _verts = mesh_baked.vertices

                    # start_time1 = time.time()
                    mw = self.current_mesh.matrix_world
                    object_data = self.objects_data[self.current_mesh.name]

                    verts_list = object_data["vertex_groups_dict"][self.current_vgroup]
                    # verts_co = [mw @ Vector((round(_verts[v].co[0], 2), round(_verts[v].co[1], 2), round(_verts[
                    # v].co[2], 2))) for v in verts_list]
                    verts_co = [mw @ _verts[v].co for v in verts_list]

                    vertex_colors = [self.highlight_color for _ in range(len(verts_co))]

                    if mesh_evaluation_method == 0:
                        try:
                            bpy.data.meshes.remove(mesh_baked)
                        except:
                            pass

                    # print('Computed verts in', time.time() - start_time1)
                    # batch and shader
                    batch = batch_for_shader(self.shader, 'TRIS', {"pos": verts_co, "color": vertex_colors},
                                             indices=object_data["indices_groups_dict"][self.current_vgroup])

                    # Render
                    if self.backface_cull:
                        bgl.glEnable(bgl.GL_CULL_FACE)

                    bgl.glEnable(bgl.GL_BLEND)
                    bgl.glDepthMask(bgl.GL_TRUE)

                    # bgl.glDepthFunc(bgl.GL_LEQUAL)
                    # bgl.glDepthRange(0.1, 1.0)
                    # bgl.glClearDepth(1.0)
                    # bgl.glPolygonMode(bgl.GL_FRONT, bgl.GL_FILL)
                    # bgl.glClear(bgl.GL_DEPTH_BUFFER_BIT)
                    batch.draw(self.shader)

                    bgl.glDisable(bgl.GL_BLEND)
                    # bgl.glDisable(bgl.GL_CULL_FACE)

    def modal(self, context, event):
        # activate the drawing only if 3 frames are true
        if event.type == 'MOUSEMOVE':
            if self.is_mouse_moving == "False":
                self.is_mouse_moving = "Activating1"
            elif self.is_mouse_moving == "Activating1":
                self.is_mouse_moving = "Activating2"
            else:
                self.is_mouse_moving = "True"
        else:
            if event.type != bpy.context.scene.skin_sel_mouse_select:
                self.is_mouse_moving = "False"

        # do not run when animation playback for performances reasons
        if not context.screen.is_animation_playing:

            if context.area:
                context.area.tag_redraw()

            # exit operator conditions
            if event.type == "ESC" or context.scene.skin_sel_active == False:
                end_skin_select(context, self)
                return {'FINISHED'}

            if self.current_mesh:
                if 'EDIT' in context.mode:
                    end_skin_select(context, self)
                    return {'FINISHED'}

            region = context.region
            rv3d = context.region_data
            coord = event.mouse_region_x, event.mouse_region_y
            try:
                self._view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
                self._ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
                self._ray_target = self._ray_origin + self._view_vector
            except AttributeError:
                pass
            # ON CLICK

            if event.type == context.scene.skin_sel_mouse_select and event.value == "PRESS":
                if coord[0] < region.width and coord[0] > 0 and coord[1] > 0 and coord[
                    1] < region.height:  # only if the mouse cursor is in the viewport area
                    print("Active object:", bpy.context.active_object.name)

                    self.highlight_color = (bpy.context.scene.skin_sel_color[0], bpy.context.scene.skin_sel_color[1],
                                            bpy.context.scene.skin_sel_color[2], bpy.context.scene.skin_sel_alpha)
                    self.backface_cull = bpy.context.scene.skin_sel_backcull

                    if not self.armature:
                        if bpy.context.active_object.type != "MESH":
                            if len(self.objects_data) > 0:
                                mesh_name = [v for i, v in enumerate(self.objects_data) if i == 0][0]
                                try:
                                    bpy.ops.object.select_all(action='DESELECT')
                                except:
                                    pass
                                set_active_object(mesh_name)

                    # if the armature is not selected, look for it and select it
                    if bpy.context.active_object.type == "MESH":
                        print("A mesh is selected")

                        if not self.armature:
                            print("Find armature...")
                            self.armature = bpy.context.active_object.find_armature()
                            if not self.armature:  # a non-skinned mesh is selected, get the armature from another
                                # skinned mesh found
                                if len(self.objects_data) > 0:
                                    mesh_name = [v for i, v in enumerate(self.objects_data) if i == 0][0]
                                    self.armature = bpy.data.objects.get(mesh_name).find_armature()

                        if self.armature:
                            print("Armature found", self.armature.name)
                            bpy.ops.object.select_all(action='DESELECT')
                            set_active_object(self.armature.name)
                            bpy.ops.object.mode_set(mode='POSE')
                            print("Select armature and switched to pose mode")

                    # select bone
                    if self.armature:
                        # get the bones
                        if self.current_vgroup:
                            group_bones = self.current_vgroup[3:].replace(" ", "").split(',')
                            side = self.current_vgroup[-2:]

                            if context.mode != 'POSE':
                                bpy.ops.object.mode_set(mode='POSE')

                            # Map inputs keys
                            map_input_keys(event, self)

                            if not self.multiple_input:  # do not deselect if multiple selection key is pressed
                                bpy.ops.pose.select_all(action='DESELECT')

                            target_bone_name = group_bones[0]

                            if self.second_input and len(group_bones) >= 2:
                                target_bone_name = group_bones[1]
                                print("activate second input")
                            elif self.third_input and len(group_bones) == 3:
                                target_bone_name = group_bones[2]
                                print("activate third input")

                            if target_bone_name[-2:] != side:
                                target_bone_name += side

                            print("Selected bone:", target_bone_name)
                            self.current_bone = self.armature.data.bones.get(target_bone_name)
                            if self.current_bone:
                                self.current_bone.select = True
                                self.armature.data.bones.active = self.current_bone
                            else:
                                print("Bone:", target_bone_name, "not found")

            # ON MOUSE OVER
            obj, idx = get_object_and_face_mouse(context, event, self)
            if obj and idx:
                self.current_mesh = obj
                if self.current_mesh:

                    if not obj.name in self.objects_data:
                        # if build_mesh_data must be called, first display the text info and go to the next
                        # modal/frame loop
                        if self.build_data:
                            build_mesh_data(self)
                            self.build_data = False
                            self.text_report = ""
                        else:
                            try:
                                self.text_report = 'caching [' + obj.name + ']...'
                                self.build_data = True
                                return {'PASS_THROUGH'}
                                # build_mesh_data(self)
                            except ReferenceError:
                                pass

                    # find the corresponding vertex group
                    vgroup_name = search_value_in_dict(self.objects_data[self.current_mesh.name]["faces_groups_dict"],
                                                       idx)
                    if vgroup_name:
                        # print("Found vgroup", vgroup_name)
                        self.current_vgroup = vgroup_name
                        # self.current_mesh.vertex_groups.active_index = self.current_mesh.vertex_groups[
                        # vgroup_name].index

                        if self.current_vgroup:
                            group_bones = self.current_vgroup[3:].replace(" ", "").split(',')
                            map_input_keys(event, self)
                            self.text_report = group_bones[0]

                            if self.second_input and len(group_bones) >= 2:
                                self.text_report = group_bones[1]
                            elif self.third_input and len(group_bones) == 3:
                                self.text_report = group_bones[2]

                        if bpy.context.active_object.type == "ARMATURE":
                            self.armature = bpy.data.objects[bpy.context.active_object.name]

                            # trigger the bone selection again (already done on click event) in case
                            # it's deselected when clicking in a void area
                            if self.current_bone:
                                if not self.current_bone.select:
                                    self.current_bone.select = True

                        else:
                            self.armature = None

                    else:
                        self.current_vgroup = None

        return {'PASS_THROUGH'}

    def execute(self, context):
        args = (self, context)

        # enable skin selection
        if context.scene.skin_sel_active == False:
            # draw handler
            if self.draw_handler:
                bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')

            self.draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_3_args, args, 'WINDOW',
                                                                       'POST_VIEW')
            self.text_draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_text, args, 'WINDOW',
                                                                            'POST_PIXEL')
            # self.timer_handler = context.window_manager.event_timer_add(1, window=context.window)

            context.window_manager.modal_handler_add(self)
            print("Start modal")

            """
            # Buggy currently...
            self.mouse_select = 'LEFTMOUSE'
            if bpy.context.window_manager.keyconfigs[0].preferences['select_mouse'] == 1:
                self.mouse_select = 'RIGHTMOUSE'
            """
            # restrict selection to armature
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.show_object_select_mesh = False
                            space.show_object_select_light = False
                            space.show_object_select_empty = False
                            space.show_object_select_camera = False

            # restrict visibility to meshes (no overlays)
            if context.scene.skin_sel_auto:
                self.show_overlay = bpy.context.space_data.overlay.show_bones
                bpy.context.space_data.overlay.show_bones = False
                bpy.context.space_data.overlay.show_extras = False

            context.scene.skin_sel_active = True
            return {'RUNNING_MODAL'}

            # disable skin selection
        else:
            context.scene.skin_sel_active = False
            return {'FINISHED'}

    def draw_callback_3_args(self, op, context):
        try:
            self.draw(self)
        except ReferenceError:
            pass

    def draw_callback_text(self, op, context):
        try:
            self.draw_text(self)
        except ReferenceError:
            pass


class SS_PT_skin_select_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Alchemy"
    bl_label = "Interactive Mode"
    bl_idname = "SS_PT_skin_select"

    def draw(self, context):
        active_armature = ""

        if len(context.selected_objects) > 0:
            if context.selected_objects[0].type == 'ARMATURE':
                active_armature = context.selected_objects[0].data.name
            else:
                if len(context.selected_objects) > 1:
                    if context.selected_objects[1].type == 'ARMATURE':
                        active_armature = context.selected_objects[1].data.name

        layout = self.layout
        row = layout.row(align=True)
        if context.scene.skin_sel_active == False:
            btn = row.operator(SS_OT_skins_selection.bl_idname, text="Start", icon='PLAY')
            # btn.disable = False
        if context.scene.skin_sel_active == True:
            btn = row.operator(SS_OT_skins_selection.bl_idname, text="Stop", icon='PAUSE')
            # btn.disable = True
        layout.separator()

        layout.label(text="Vertex Groups Creation:")
        col = layout.column(align=True)

        row = col.row(align=True)
        if active_armature != "":
            row.enabled = True
            row.prop_search(context.scene, "skin_sel_vgroup1", bpy.data.armatures[active_armature], "bones", text="")
        else:
            row.enabled = False
            row.prop(context.scene, "skin_sel_vgroup1", text="")

        btn = row.operator("id.ss_pick_controller", text="", icon='EYEDROPPER')
        btn.value = 1

        row = col.row(align=True)
        if active_armature != "":
            row.enabled = True
            row.prop_search(context.scene, "skin_sel_vgroup2", bpy.data.armatures[active_armature], "bones", text="")
        else:
            row.enabled = False
            row.prop(context.scene, "skin_sel_vgroup2", text="")
        btn = row.operator("id.ss_pick_controller", text="", icon='EYEDROPPER')
        btn.value = 2

        row = col.row(align=True)
        if active_armature != "":
            row.enabled = True
            row.prop_search(context.scene, "skin_sel_vgroup3", bpy.data.armatures[active_armature], "bones", text="")
        else:
            row.enabled = False
            row.prop(context.scene, "skin_sel_vgroup3", text="")
        btn = row.operator("id.ss_pick_controller", text="", icon='EYEDROPPER')
        btn.value = 3

        row = col.row(align=True)
        row.operator("id.ss_add_vgroup", text="Create VGroup", icon="PLUS")
        row = col.row(align=True)
        row.operator("id.ss_mirror_vgroup", text="Mirror Selected VGroup", icon="MOD_MIRROR")
        layout.separator()

        layout.label(text="Display:")
        layout.prop(context.scene, "skin_sel_color")
        layout.prop(context.scene, "skin_sel_alpha", slider=True)
        layout.prop(context.scene, "skin_sel_auto")
        layout.prop(context.scene, "skin_sel_backcull")
        """
        layout.prop(context.scene, "skin_sel_backf")
        layout.prop(context.scene, "skin_sel_xray")
        layout.prop(context.scene, "skin_sel_highl_qual", "")       
        layout.prop(context.scene, "skin_sel_display_error", "Show Info Message")        
        """

        layout.separator()
        layout.label(text="Key Input:")
        layout.prop(context.scene, "skin_sel_mouse_select", text="Mouse", expand=False)
        layout.prop(context.scene, "skin_sel_second_input", text="2")
        layout.prop(context.scene, "skin_sel_third_input", text="3")


classes = (SS_OT_skins_selection, SS_PT_skin_select_panel, SS_OT_pick_controller, SS_OT_add_vgroup, SS_OT_mirror_vgroup)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.skin_sel_vgroup1 = bpy.props.StringProperty(name="Vertex Group Name1", default="")
    bpy.types.Scene.skin_sel_vgroup2 = bpy.props.StringProperty(name="Vertex Group Name2", default="")
    bpy.types.Scene.skin_sel_vgroup3 = bpy.props.StringProperty(name="Vertex Group Name3", default="")
    bpy.types.Scene.skin_sel_active = bpy.props.BoolProperty(name="Skin Selection Active", default=False)
    bpy.types.Scene.skin_sel_color = bpy.props.FloatVectorProperty(name="Color", subtype="COLOR_GAMMA",
                                                                   default=(0.348837, 0.748951, 0.8), min=0.0, max=1.0,
                                                                   description="Selection highlight color")
    bpy.types.Scene.skin_sel_alpha = bpy.props.FloatProperty(name="Alpha", default=0.17, min=0.0, max=1.0,
                                                             description="Color alpha")
    bpy.types.Scene.skin_sel_auto = bpy.props.BoolProperty(name="Auto Only Render", default=True,
                                                           description="Enable Only Render when enabled")
    bpy.types.Scene.skin_sel_backcull = bpy.props.BoolProperty(name="Backface Cull", default=True,
                                                               description="Highlights will used backface culling")
    bpy.types.Scene.skin_sel_second_input = bpy.props.EnumProperty(name="Second Input", items=(
        ('SHIFT', 'Shift', 'Shift key to select the second mapped controller'),
        ('ALT', 'Alt', 'Alt key to select the second mapped controller'),
        ('CTRL', 'Ctrl', 'Ctrl key to select the second mapped controller')), default='CTRL')
    bpy.types.Scene.skin_sel_third_input = bpy.props.EnumProperty(name="Third Input", items=(
        ('SHIFT', 'Shift', 'Shift key to select the third mapped controller'),
        ('ALT', 'Alt', 'Alt key to select the third mapped controller'),
        ('CTRL', 'Ctrl', 'Ctrl key to select the third mapped controller')), default='ALT')
    bpy.types.Scene.skin_sel_display_error = bpy.props.BoolProperty(name="Display Error", default=True,
                                                                    description="Display an information message if "
                                                                                "the second or third controller is "
                                                                                "not set for the selected area")
    bpy.types.Scene.skin_sel_mouse_select = bpy.props.EnumProperty(name="Mouse Selection", items=(
        ('LEFTMOUSE', 'Left', 'Left button to select'), ('RIGHTMOUSE', 'Right', 'Right button to select')),
                                                                   default='LEFTMOUSE')


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.skin_sel_vgroup1
    del bpy.types.Scene.skin_sel_vgroup2
    del bpy.types.Scene.skin_sel_vgroup3
    del bpy.types.Scene.skin_sel_active
    del bpy.types.Scene.skin_sel_color
    del bpy.types.Scene.skin_sel_auto
    del bpy.types.Scene.skin_sel_backcull
    del bpy.types.Scene.skin_sel_alpha
    del bpy.types.Scene.skin_sel_second_input
    del bpy.types.Scene.skin_sel_third_input
    del bpy.types.Scene.skin_sel_display_error
    del bpy.types.Scene.skin_sel_mouse_select

if __name__ == '__main__':

    register()
