import abc

class AbstractUnitOfWork(abc.ABC):
    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, ex_type, ex_value, traceback):
        if not ex_type:
            self.publish_events()
            self.commit()
        else:
            self.rollback()

    @abc.abstractmethod
    def publish_events(self):
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError