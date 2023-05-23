from abc import ABC, abstractmethod

class ExtractorInterface(ABC):

    @abstractmethod
    def get_response(self, role):
        pass

    @abstractmethod
    def get_soup(self, role):
        pass

    @abstractmethod
    def get_target_url(self, role):
        pass

    @abstractmethod
    def save_json(self, output_file, json_data):
        pass