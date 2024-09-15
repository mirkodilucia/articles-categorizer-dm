# provides functions to store and load objects from files
import pickle


class Serializer:
    @staticmethod
    def save_object(obj, file_name):
        """"Save an object using the pickle library on a file

        :param obj: undefined. Object to save
        :param file_name: str. Name of the file of the object to save
        """
        print("Saving " + file_name)
        with open(file_name + ".pkl", 'wb') as fid:
            pickle.dump(obj, fid)

    @staticmethod
    def load_object(file_name):
        """"Load an object from a file

        :param file_name: str. Name of the file of the object to load
        :return: obj: undefined. Object loaded
        """
        try:
            with open(file_name + '.pkl', 'rb') as fid:
                obj = pickle.load(fid)
                return obj
        except IOError:
            print("File not found")
            return None
