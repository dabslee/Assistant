import cx_Freeze

executables = [cx_Freeze.Executable("game.py")]

cx_Freeze.setup(
    name="Rina",
    options={"build_exe": {"packages":[],
                           "include_files":[]}},
    executables = executables

    )
