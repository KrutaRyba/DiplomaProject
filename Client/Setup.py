from cx_Freeze import setup, Executable

excludes = ["Tkinter"]
includefiles = ["ClientConfig.json"]

setup(name = "VectorTilesClient" ,
      version = "0.1" ,
      description = "" ,
      options = {"build_exe": {"excludes":excludes,"include_files":includefiles}},
      executables = [Executable("Client.py")])