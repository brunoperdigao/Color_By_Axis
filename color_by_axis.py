from calendar import c
import bpy
import bmesh
import bgl
import gpu
import copy
import mathutils
from gpu_extras.batch import batch_for_shader
from .error_message import CBA_OT_ErrorMessage

class CBA_OT_Color_by_Axis(bpy.types.Operator):
    bl_idname = "object.color_by_axis"
    bl_label = "Color By Axis"
    bl_description = "Operator to color edges by axis"
    bl_options = {'REGISTER'}

    axis_type: bpy.props.StringProperty(name="Axis Type")
    

    def __init__(self):
        self.draw_handle = None
        self.draw_event = None

    

    def invoke(self, context, event):
        
        # Error message
        for o in context.objects_in_mode:
            if o.type  != 'MESH':
                msg1 = 'This operator only work with meshes.'
                msg2 = 'Please check if there are other kind of objects in selection.'
                bpy.ops.message.error_message('INVOKE_DEFAULT', message_line1=msg1, message_line2=msg2)
                return {"CANCELLED"}

        # Error message
        if context.mode != 'EDIT_MESH':
            msg = 'This operator only works in Edit Mode'
            bpy.ops.message.error_message('INVOKE_DEFAULT', message_line1=msg)
            return {"CANCELLED"}                           

        # Error message
        if self.axis_type == 'REFERENCE' and not context.scene.axis_ref:
                msg = 'Please choose a reference object.'
                bpy.ops.message.error_message('INVOKE_DEFAULT', message_line1=msg)
                return {"CANCELLED"}


        self.create_batch()

        args = (self, context)
        self.register_handlers(args, context)

        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def register_handlers(self, args, context):
        self.draw_handle= bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback, args, "WINDOW", "POST_VIEW"
        )

        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)

    def unregister_handlers(self, context):

        context.window_manager.event_timer_remove(self.draw_event)

        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, "WINDOW")
        
        self.draw_handle = None
        self.draw_event = None

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        if event.type in {'ESC', 'RET', 'NUMPAD_ENTER', 'TAB', 'SPACE', 'RIGHTMOUSE', 'LEFTMOUSE'} or event.ascii:
            self.unregister_handlers(context)
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def finish(self):
        self.unregister_handlers(context)
        return {"FINISHED"}
    
    def get_verts(self):
        verts_x = []
        verts_y = []
        verts_z = []        

        for o in bpy.context.objects_in_mode:
            
            # Get the object location, scale and rotation, to mix with the rotation of a reference object.
            # This is used when axis_type == 'REFERENCE'
            obj_location = o.matrix_world.to_translation()
            obj_scale = o.matrix_world.to_scale()
            obj_rotation = o.matrix_world.to_euler()

            # Object global matrix
            world_matrix = o.matrix_world
            custom_matrix = None

            bm = bmesh.from_edit_mesh(o.data)

            # Calling the property directly from the context
            axis_reference = bpy.context.scene.axis_ref

            if self.axis_type == 'REFERENCE' and axis_reference:   
                # Get the reference rotation
                custom_euler = copy.copy(axis_reference.matrix_world.to_euler())

                # To get the rotation relative to the reference, subtract the reference euler by the object euler, and avoid negative numbers
                custom_euler[0] = custom_euler[0] - obj_rotation[0]
                custom_euler[1] = custom_euler[1] - obj_rotation[1]
                custom_euler[2] = custom_euler[2] - obj_rotation[2]
                for v in custom_euler:
                    if v < 0:
                        v = v * (-1)

                # Custom matrix, mixed with the reference rotation
                custom_matrix = mathutils.Matrix.LocRotScale(obj_location, custom_euler, obj_scale)
            
            
            for e in bm.edges:
                # Vertices local coordinates
                v1 = e.verts[0].co
                v2 = e.verts[1].co

                v1_x_round = round(v1[0], 4)
                v1_y_round = round(v1[1], 4)
                v1_z_round = round(v1[2], 4)
                v2_x_round = round(v2[0], 4)
                v2_y_round = round(v2[1], 4)
                v2_z_round = round(v2[2], 4)
                
                # Vertices global coordinates
                v1_global = world_matrix @ e.verts[0].co
                v2_global = world_matrix @ e.verts[1].co

                v1_global_x_round = round(v1_global[0], 4)
                v1_global_y_round = round(v1_global[1], 4)
                v1_global_z_round = round(v1_global[2], 4)
                v2_global_x_round = round(v2_global[0], 4)
                v2_global_y_round = round(v2_global[1], 4)
                v2_global_z_round = round(v2_global[2], 4)
                
                if not custom_matrix:
                    pass
                else:
                    # Vertices reference coordinates
                    v1_custom = custom_matrix @ e.verts[0].co
                    v2_custom = custom_matrix @ e.verts[1].co

                    # Rounding to avoid precision problems
                    v1_custom_x_round = round(v1_custom[0], 4)
                    v1_custom_y_round = round(v1_custom[1], 4)
                    v1_custom_z_round = round(v1_custom[2], 4)
                    v2_custom_x_round = round(v2_custom[0], 4)
                    v2_custom_y_round = round(v2_custom[1], 4)
                    v2_custom_z_round = round(v2_custom[2], 4)

                    if (v1_custom_y_round == v2_custom_y_round) & (v1_custom_z_round == v2_custom_z_round): # Compare the rounded numbers
                        v1 = v1_global
                        v2 = v2_global
                        verts_x.append(v1)    
                        verts_x.append(v2)  

                    elif (v1_custom_x_round == v2_custom_x_round) & (v1_custom_z_round == v2_custom_z_round): 
                        v1 = v1_global
                        v2 = v2_global
                        verts_y.append(v1)    
                        verts_y.append(v2)
                
                    elif (v1_custom_x_round == v2_custom_x_round) & (v1_custom_y_round == v2_custom_y_round): 
                        v1 = v1_global
                        v2 = v2_global
                        verts_z.append(v1)    
                        verts_z.append(v2)
                
                if self.axis_type == 'GLOBAL':
                    if (v1_global_y_round == v2_global_y_round) & (v1_global_z_round == v2_global_z_round): # Compare the rounded numbers
                        v1 = v1_global
                        v2 = v2_global
                        verts_x.append(v1)    
                        verts_x.append(v2)  

                    elif (v1_global_x_round == v2_global_x_round) & (v1_global_z_round == v2_global_z_round): 
                        v1 = v1_global
                        v2 = v2_global
                        verts_y.append(v1)    
                        verts_y.append(v2)
                    
                    elif (v1_global_x_round == v2_global_x_round) & (v1_global_y_round == v2_global_y_round): 
                        v1 = v1_global
                        v2 = v2_global
                        verts_z.append(v1)    
                        verts_z.append(v2)

                if self.axis_type == 'LOCAL':
                    if (v1_y_round == v2_y_round) & (v1_z_round == v2_z_round): # Compare the rounded numbers
                        v1 = v1_global
                        v2 = v2_global
                        verts_x.append(v1)    
                        verts_x.append(v2)  

                    elif (v1_x_round == v2_x_round) & (v1_z_round == v2_z_round): 
                        v1 = v1_global
                        v2 = v2_global
                        verts_y.append(v1)    
                        verts_y.append(v2)
                    
                    elif (v1_x_round == v2_x_round) & (v1_y_round == v2_y_round): 
                        v1 = v1_global
                        v2 = v2_global
                        verts_z.append(v1)    
                        verts_z.append(v2)
            
        return verts_x, verts_y, verts_z
    
    def create_batch(self):
        
        vertices_x, vertices_y, vertices_z = self.get_verts()
        self.shader_x = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch_x = batch_for_shader(self.shader_x, 'LINES', {"pos": vertices_x})
                
        self.shader_y = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch_y = batch_for_shader(self.shader_y, 'LINES', {"pos": vertices_y})
        
        self.shader_z = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch_z = batch_for_shader(self.shader_z, 'LINES', {"pos": vertices_z})

    def draw_callback(self, op, context):
        bgl.glLineWidth(2)

        self.shader_x.bind()
        self.shader_x.uniform_float("color", (1, 0, 0, 1))
        self.batch_x.draw(self.shader_x)

        self.shader_y.bind()
        self.shader_y.uniform_float("color", (0, 1, 0, 1))
        self.batch_y.draw(self.shader_y)

        self.shader_z.bind()
        self.shader_z.uniform_float("color", (0, 0, 1, 1))
        self.batch_z.draw(self.shader_z)

 
