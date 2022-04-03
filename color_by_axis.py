from calendar import c
import bpy
import bmesh
import bgl
import gpu
import copy
import mathutils
from gpu_extras.batch import batch_for_shader

class OT_color_by_axis(bpy.types.Operator):
    bl_idname = "object.color_by_axis"
    bl_label = "Color By Axis"
    bl_description = "Operator to color edges by axis"
    bl_options = {'REGISTER'}

    def __init__(self):
        self.draw_handle = None
        self.draw_handle_x = None
        self.draw_handle_y = None
        self.draw_handle_z = None
        self.draw_event = None

        self.widgets = []

    def invoke(self, context, event):

        #self.create_batch()
        self.create_batch_x()
        self.create_batch_y()
        self.create_batch_z()

        args = (self, context)
        self.register_handlers(args, context)

        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}


    def register_handlers(self, args, context):
        #self.draw_handle= bpy.types.SpaceView3D.draw_handler_add(
        #    self.draw_callback, args, "WINDOW", "POST_VIEW"
        #)

        self.draw_handle_x= bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_x, args, "WINDOW", "POST_VIEW"
        )

        self.draw_handle_y= bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_y, args, "WINDOW", "POST_VIEW"
        )

        self.draw_handle_z= bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_z, args, "WINDOW", "POST_VIEW"
        )

        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)

    def unregister_handlers(self, context):

        context.window_manager.event_timer_remove(self.draw_event)

        #bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, "WINDOW")
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle_x, "WINDOW")
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle_y, "WINDOW")
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle_z, "WINDOW")

        #self.draw_handle = None
        self.draw_handle_x = None
        self.draw_handle_y = None
        self.draw_handle_z = None
        self.draw_event = None

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        if event.type in {"ESC"}:
            self.unregister_handlers(context)
            return {'CANCELLED'}

        return {"PASS_THROUGH"}

    def finish(self):
        self.unregister_handlers(context)
        return {"FINISHED"}

    def get_verts(self):
        verts = []
        verts_by_edges = []
        for o in bpy.context.objects_in_mode:
            world_matrix = o.matrix_world
            bm = bmesh.from_edit_mesh(o.data)
            for e in bm.edges:
                #if e.select:
                for v in e.verts:
                #        if v.select:
                    v =  world_matrix @ v.co
                    verts.append(v)
        return verts

    def get_x_verts(self):
        verts = []
        verts_by_edges = []
        

        for o in bpy.context.objects_in_mode:
            
            # Here I get the object location, scale and rotation, so I can mix with the rotation of a reference object.
            # That way I can compare the vertices locations based on the reference axis
            
            obj_location = o.matrix_world.to_translation()
            obj_scale = o.matrix_world.to_scale()
            obj_rotation = o.matrix_world.to_euler()

            # Get the reference rotation
            custom_euler = copy.copy(bpy.context.scene.objects['Empty'].matrix_world.to_euler())
            
            # TO DO
            # Checar se isso ainda é válido
            custom_euler[0] = custom_euler[0] - obj_rotation[0]
            if custom_euler[0] < 0:
                custom_euler[0] = custom_euler[0] * -1
            custom_euler[1] = custom_euler[1] - obj_rotation[1]
            if custom_euler[1] < 0:
                custom_euler[1] = custom_euler[1] * -1
            custom_euler[2] = custom_euler[2] - obj_rotation[2]
            if custom_euler[2] < 0:
                custom_euler[2] = custom_euler[2] * -1

            # Object global matrix
            world_matrix = o.matrix_world

            # Custom matrix, mixed with the reference rotation
            custom_matrix = mathutils.Matrix.LocRotScale(obj_location, custom_euler, obj_scale)
            bm = bmesh.from_edit_mesh(o.data)
            for e in bm.edges:
                #if e.select:
                v1 = e.verts[0].co
                v2 = e.verts[1].co
                
                v1_global = world_matrix @ e.verts[0].co
                v2_global = world_matrix @ e.verts[1].co
                
                v1_custom = custom_matrix @ e.verts[0].co
                v2_custom = custom_matrix @ e.verts[1].co

                # Have to do this rounding for precision problems
                # I noticed this when the object location were 180 degress different from the reference.
                v1_y_round = round(v1_custom[1], 4)
                v1_z_round = round(v1_custom[2], 4)
                v2_y_round = round(v2_custom[1], 4)
                v2_z_round = round(v2_custom[2], 4)                
                
                if (v1_y_round == v2_y_round) & (v1_z_round == v2_z_round): # Compare the rounded numbers
                    v1 = v1_global
                    v2 = v2_global
                    verts.append(v1)    
                    verts.append(v2)  
            
        return verts

    def get_y_verts(self):
        verts = []
        verts_by_edges = []
        for o in bpy.context.objects_in_mode:
            world_matrix = o.matrix_world
            bm = bmesh.from_edit_mesh(o.data)
            for e in bm.edges:
                #if e.select:
                v1 = e.verts[0]                    
                v2 = e.verts[1]
                if (v1.co[0] == v2.co[0]) & (v1.co[2] == v2.co[2]):
                    v1 =  world_matrix @ v1.co
                    v2 =  world_matrix @ v2.co 
                    verts.append(v1)
                    verts.append(v2)
        return verts

    def get_z_verts(self):
        verts = []
        verts_by_edges = []
        for o in bpy.context.objects_in_mode:
            world_matrix = o.matrix_world
            bm = bmesh.from_edit_mesh(o.data)
            for e in bm.edges:
                #if e.select:
                v1 = e.verts[0]                    
                v2 = e.verts[1]
                if (v1.co[0] == v2.co[0]) & (v1.co[1] == v2.co[1]):
                    v1 =  world_matrix @ v1.co
                    v2 =  world_matrix @ v2.co
                    verts.append(v1)
                    verts.append(v2)
        return verts


    def create_batch(self):
        
        vertices = self.get_verts()
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'LINES', {"pos": vertices})

    def create_batch_x(self):
        
        vertices = self.get_x_verts()
        self.shader_x = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch_x = batch_for_shader(self.shader_x, 'LINES', {"pos": vertices})

    def create_batch_y(self):
        
        vertices = self.get_y_verts()
        self.shader_y = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch_y = batch_for_shader(self.shader_y, 'LINES', {"pos": vertices})

    def create_batch_z(self):
        
        vertices = self.get_z_verts()
        self.shader_z = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch_z = batch_for_shader(self.shader_z, 'LINES', {"pos": vertices})
        

    def draw_callback(self, op, context):
        self.shader.bind()
        self.shader.uniform_float("color", (1, 1, 1, 1))
        self.batch.draw(self.shader)

    def draw_callback_x(self, op, context):
        bgl.glLineWidth(5)
        self.shader_x.bind()
        self.shader_x.uniform_float("color", (1, 0, 0, 1))
        self.batch_x.draw(self.shader_x)

    def draw_callback_y(self, op, context):
        bgl.glLineWidth(5)
        self.shader_y.bind()
        self.shader_y.uniform_float("color", (0, 1, 0, 1))
        self.batch_y.draw(self.shader_y)

    def draw_callback_z(self, op, context):
        bgl.glLineWidth(5)          
        self.shader_z.bind()
        self.shader_z.uniform_float("color", (0, 0, 1, 1))
        self.batch_z.draw(self.shader_z)