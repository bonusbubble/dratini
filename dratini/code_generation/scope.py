from random import randint


class Scope:
    '''
    The context under which the code is currently executing at the point of reference.
    '''

    @property
    def id(self) -> int:
        '''
        The ID of the `Scope`.
        '''
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def name(self) -> str:
        '''
        The name of the `Scope`.
        '''
        return "_" + hex(self.id)[:2]

    @property
    def local_names(self) -> list[str]:
        '''
        A list of local variable names declared in this `Scope`.
        '''
        return self._local_names

    @local_names.setter
    def local_names(self, value: list[str]):
        self._local_names = value

    def __init__(self, parent_scope: object):
        self._parent = parent_scope
        self._id = randint(0x00000000, 0xFFFFFFFF)
        self._local_names: list[str] = []
