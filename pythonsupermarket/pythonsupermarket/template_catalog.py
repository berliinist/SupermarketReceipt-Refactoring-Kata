from abc import ABCMeta, abstractmethod, abstractproperty


class TemplateCatalog(metaclass=ABCMeta):

    @abstractproperty
    def products(self):
        pass

    @abstractmethod
    def add_product(self, product):
        pass

    @abstractmethod
    def get_product(self, product):
        pass
