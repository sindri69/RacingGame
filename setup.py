import cx_Freeze

executables = [cx_Freeze.Executable("Control3DProgram.py")]

cx_Freeze.setup(
    name="racer300",
    options={"build_exe": {"packages":["pygame", "numpy", "opengl", "Playsound"],
                           "include_files":["models/birch_tree.mtl", "models/shelby.mtl", "models/shelby2.mtl", "models/shelby3.mtl", "models/gate.mtl", "models/birch_tree.obj", "models/shelby.obj", "models/shelby2.obj", "models/shelby3.obj", "models/gate.obj", "textures/skysphere.jpg", "textures/grass.jpg", "simple3D.frag", "simple3D.vert", "skysphere_shader.frag", "skysphere_shader.vert", "sounds/oh_yeah.mp3"]}},
    executables = executables

    )