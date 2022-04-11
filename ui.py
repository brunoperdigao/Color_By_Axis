from re import L
import bpy

class CBA_PT_Main_Panel(bpy.types.Panel):
    bl_idname = "CBA_PT_Main_Panel"
    bl_label = "Color by Axis"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Color by Axis"


    def draw(self, context):

        @classmethod
        def poll(self, context):
            if context.mode != 'OBJECT':
                return True
            else:
                return False

        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'

        
        color_by_axis_button = layout.operator('object.color_by_axis', text='Color by Axis Overlay', icon='NONE')
        
        scene = bpy.context.scene
        col1 = layout.column()
        col1.label(text="Axis Type:")
        col1.prop(scene, 'axis_type', text='')
        col2 = layout.column()
        col2.label(text="Reference Object")
        col2.prop_search(scene, 'axis_ref', scene, 'objects', text="")
        layout.prop(scene, "draw_permanent", toggle=True)

        # Use the axis_type chosen in the UI as an input to the operator
        color_by_axis_button.axis_type = scene.axis_type




