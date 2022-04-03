# Color By Axis - Blender Add-on

Color by Axis is a Blender add-on that allows you to check whether the edges of an object are aligned with the X, Y or Z axis, by creating a color overlay.

⚠ This add-on is still a work in progress.

## How it works

The add-on will create a Panel in the N-Panel, called Color by Axis. The panel has three items:
- Color by Axis button:
  - **It only works in "Edit Mode".**
  - Activates the operator that creates the overlay.  
  - Once created, it will allow will to navigate the viewport, but will be turned off as soon as you type or click.

- Axis type option:
  - GLOBAL: Compare your object's edges with global axis.
  - LOCAL: Compare your object's edges with its local axis.
  - REFERENCE: Compare your object's edges with a selected reference object. Won't work if no object is selected.

- Reference object:
  - Select the object which will be used by the REFERENCE axis type.

## Quick example
Add a default cube and enter "Edit Mode". Click the button "Color by Axis" in the N-panel. The edges of the cube will be colored according to the axis that they are parallel to.

![image](https://user-images.githubusercontent.com/57102715/161439473-ae5717c5-a9fa-4a25-97b7-5742043c8559.png)


By rotating 30 degrees in the Z axis, in "Object Mode", there are no edges parallel to X or Y axis anymore:

![image](https://user-images.githubusercontent.com/57102715/161439519-97e539c1-ef47-40c7-8391-e4f5ba142a74.png)



If "LOCAL" Axis Type is selected, it will color the edges based on the local coordinates of the objects.

![image](https://user-images.githubusercontent.com/57102715/161439508-34dec154-33b3-4e0d-b759-da63e94fa1ee.png)



If "REFERENCE" Axis Type is selected, you have to choose another object for reference. It will color the edges based on the local coordinates of the reference object.

![image](https://user-images.githubusercontent.com/57102715/161439576-6d7333f0-56b6-46c5-b556-405328303110.png)


Works with multiple objects:

![image](https://user-images.githubusercontent.com/57102715/161440880-1ca8313a-a73a-4634-b632-d00d1297649e.png)

![image](https://user-images.githubusercontent.com/57102715/161440922-6f03169d-1318-4b7f-9c63-46877d1ba97c.png)

![image](https://user-images.githubusercontent.com/57102715/161440939-6b4eec40-20f8-4108-ad16-f995d46f9cbb.png)






