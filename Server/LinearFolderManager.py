from os import path, mkdir
from shutil import rmtree

class LinearFolderManager:
    
    def __init__(self, folder: str = ".") -> None:
        self.folders: list[str] = [folder]
        if (not path.exists(folder)): mkdir(self.folders[0])

    def create_folder(self, folder: str, level: int) -> None:
        self.folders.append(folder)
        new_path = self.get_path(folder, level)
        if (not path.exists(new_path)): mkdir(new_path)

    def get_path(self, file: str, level: int) -> str:
        ret = path.join(*(self.folders[0:level + 1]))
        return path.join(ret, file)

    def cleanup(self) -> None:
        rmtree(self.folders[0])