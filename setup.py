import cx_Freeze

executables = [cx_Freeze.Executable("gamePong.py")]

cx_Freeze.setup(
    name="Pong",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["restart.png",'gameobjects']}},
    executables = executables
    )