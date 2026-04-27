



from abc import ABC , abstractmethod


class Persistence(ABC):

    @abstractmethod
    def save(self,data:str):
        pass


class FileStorage(Persistence):
    def save(self,data:str):
        try:
            with open("document.txt", "w") as out_file:
                out_file.write(data)
            print("Document saved to document.txt")
        except Exception as e:
            print(f"Error: Unable to open file for writing. {e}")


class DBstorage(Persistence):
    def save(self, data):
        pass

    