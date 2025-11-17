from cx_Freeze import setup, Executable

excludes = ["Tkinter"]
includefiles = ["ServerConfig.json"]

setup(name = "VectorTilesServer" ,
      version = "0.1" ,
      description = "" ,
      options = {"build_exe": {"excludes":excludes,"include_files":includefiles}},
      executables = [Executable("Server.py")])