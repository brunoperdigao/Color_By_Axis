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
from .color_by_axis import CBA_OT_Color_by_Axis
from .color_by_axis_permanent import CBA_Permanent
from .error_message import CBA_OT_ErrorMessage
from .ui import CBA_PT_Main_Panel

classes = (
    CBA_OT_Color_by_Axis,
    CBA_OT_ErrorMessage,
    CBA_PT_Main_Panel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    items = [
    ("GLOBAL", "Global", "", 1),
    ("LOCAL", "Local", "", 2),
    ("REFERENCE", "Reference", "", 3)
    ]

    bpy.types.Scene.axis_type = bpy.props.EnumProperty(items=items, name="Axis type", description="Choose axis type that will affect the overlay")
    bpy.types.Scene.axis_ref = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.draw_permanent = bpy.props.BoolProperty(name="Always ON")
    CBA_Permanent.draw_handler = bpy.types.SpaceView3D.draw_handler_add(
        CBA_Permanent.draw, (), "WINDOW", "POST_VIEW"
    )


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

    bpy.types.SpaceView3D.draw_handler_remove(CBA_Permanent.draw_handler, "WINDOW")
    del bpy.types.Scene.draw_permanent
    del bpy.types.Scene.axis_type
    del bpy.types.Scene.axis_ref

if __name__ == "__main__":
    register()
