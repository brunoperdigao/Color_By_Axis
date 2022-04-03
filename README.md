# Color By Axis - Blender Add-on

Color by Axis is a Blender add-on that allows you to check whether the edges of an object are aligned with the X, Y or Z axis, by creating a color overlay.

## How it works

The addon will create a Panel in the N-Panel, called Coloy by Axis. The panel has three items:
    - Color by Axis button:
      - Creates the overlay, but only works in "Edit Mode".
      - Once created, it will allow will to navigate the viewport, but will be turned off as soon as you type or click.
    - Axis type option:
      - GLOBAL: Compare your objects edges with global axis.
      - LOCAL: Compare your objects edges with its local axis.
      - REFERENCE: Compare your objects edges with a selected reference object. Won't work if no object is selected.
    - Reference object:
      - Select the object which will be used by the REFERENCE axis type.

## Quick example
    Add a default cube and enter "Edit Mode". Click the button "Color by Axis" in the N-panel. The edges of the cube will be colored according with the axis that they are parallel to.

    If "LOCAL" Axis Type is selected, it will color the edges based on the local coordinates of the objects.
    
    If "REFERENCE" Axis Type is selected, you have to choose another object for reference. it will color the edges based on the local coordinates of the reference object.
