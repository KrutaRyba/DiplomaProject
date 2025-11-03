from os import path, mkdir
from shutil import rmtree

class LinearFolderManager:
    
    def __init__(self, folder = "."):
        self.folders = [folder]
        if (not path.exists(folder)): mkdir(folder)

    def create_folder(self, folder, level):
        self.folders.append(folder)
        new_path = self.get_path(folder, level)
        if (not path.exists(new_path)): mkdir(new_path)

    def get_path(self, file, level):
        ret = path.join(*(self.folders[0:level + 1]))
        return path.join(ret, file)
    
    def __get_path(self, level):
        return path.join(*self.folders[0:level + 1])
    
    def cleanup(self):
        rmtree(self.folders[0])