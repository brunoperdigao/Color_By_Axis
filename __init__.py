bl_info = {
    "name": "Color by Axis",
    "author": "Bruno Perdigão",
    "description": "Color by Axis is a Blender add-on that allows you to check whether the edges of an object are aligned with the X, Y or Z axis, by creating a color overlay.",
    "blender": (3, 00, 0),
    "location": "",
    "warning": "",
    "category": "Mesh"
}

import bpy
from .color_by_axis_edges import CBA_Edges
from .ui import CBA_PT_Main_Panel

classes = (
    CBA_PT_Main_Panel,
    CBA_Edges
)

def register():
    from bpy.utils import register_class
    # for cls in classes:
    #     register_class(cls)
    register_class(CBA_PT_Main_Panel)
    
    items = [
    ("GLOBAL", "Global", "", 1),
    ("LOCAL", "Local", "", 2),
    ("REFERENCE", "Reference", "", 3)
    ]

    bpy.types.Scene.axis_type = bpy.props.EnumProperty(items=items, name="Axis type", description="Choose axis type that will affect the overlay")
    bpy.types.Scene.axis_ref = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.line_width = bpy.props.FloatProperty(name="Line Width", min=0.5, max=6.0, step=5, default=3.0)
    bpy.types.Scene.draw_permanent = bpy.props.BoolProperty(name="Color by Axis")
    bpy.types.Scene.draw_in_front = bpy.props.BoolProperty(name="In Front")
    CBA_Edges.draw_handler = bpy.types.SpaceView3D.draw_handler_add(
        CBA_Edges.draw, (), "WINDOW", "POST_VIEW"
    )
    
    


def unregister():
    from bpy.utils import unregister_class
    # for cls in classes:
    #     unregister_class(cls)
    unregister_class(CBA_PT_Main_Panel)

    bpy.types.SpaceView3D.draw_handler_remove(CBA_Edges.draw_handler, "WINDOW")
    del bpy.types.Scene.draw_permanent
    del bpy.types.Scene.draw_in_front
    del bpy.types.Scene.axis_type
    del bpy.types.Scene.axis_ref
    del bpy.types.Scene.line_width

if __name__ == "__main__":
    register()
