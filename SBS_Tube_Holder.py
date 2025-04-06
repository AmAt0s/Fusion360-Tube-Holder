import adsk.core, adsk.fusion, adsk.cam, traceback

def create_tube_holder():
    # Get the active Fusion 360 document
    app = adsk.core.Application.get()
    doc = app.activeDocument
    design = doc.design
    
    # Create a new component
    root_comp = design.rootComponent
    tube_holder_comp = root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    tube_holder_body = tube_holder_comp.component.bRepBodies.add(adsk.fusion.BRepBody.create())
    
    # Parameters for the tube holder
    tube_diameter = 16.0  # 16 mm tube diameter
    tube_height = 50.0    # 50 mm tube height
    groove_width = 2.0    # Groove for cap back
    
    # Create the main block for the holder
    holder_width = 100.0   # Holder width (enough for multiple tubes)
    holder_length = 80.0   # Length of the holder
    holder_height = 20.0   # Height of the holder
    
    # Create the main block for the tube holder
    sketches = tube_holder_comp.component.sketches
    sketch = sketches.add(tube_holder_comp.component.xYConstructionPlane)
    sketch.name = "Tube Holder Sketch"
    
    rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(adsk.core.Point2D.create(0, 0), adsk.core.Point2D.create(holder_width, holder_length))
    outer_rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(adsk.core.Point2D.create(0, 0), adsk.core.Point2D.create(holder_width, holder_length))
    
    profile = sketch.profiles.item(0)
    extrude = tube_holder_comp.component.features.extrudeFeatures.add(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude.setDistanceExtent(False, adsk.core.ValueInput.createByString(str(holder_height)))
    
    # Create tubes and grooves
    num_tubes = 6  # Number of tubes to hold
    tube_spacing = holder_width / num_tubes  # Space between each tube
    
    for i in range(num_tubes):
        x_pos = (i * tube_spacing) + tube_spacing / 2  # Space each tube
        create_tube(tube_holder_comp, x_pos, holder_length / 2, tube_diameter, tube_height, groove_width)
        
def create_tube(comp, x_pos, y_pos, tube_diameter, tube_height, groove_width):
    # Create a single tube at the specified location
    sketches = comp.component.sketches
    sketch = sketches.add(comp.component.xYConstructionPlane)
    
    circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point2D.create(x_pos, y_pos), tube_diameter / 2)
    profile = sketch.profiles.item(0)
    extrude = comp.component.features.extrudeFeatures.add(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude.setDistanceExtent(False, adsk.core.ValueInput.createByString(str(tube_height)))
    
    # Create groove for the tube cap
    groove_radius = tube_diameter / 2 - groove_width
    groove_depth = 2.0  # Groove depth
    
    groove_sketch = comp.component.sketches.add(comp.component.xYConstructionPlane)
    groove_sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point2D.create(x_pos, y_pos), groove_radius)
    groove_profile = groove_sketch.profiles.item(0)
    
    groove_extrude = comp.component.features.extrudeFeatures.add(groove_profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
    groove_extrude.setDistanceExtent(False, adsk.core.ValueInput.createByString(str(groove_depth)))

# Run the tube holder creation function
create_tube_holder()
