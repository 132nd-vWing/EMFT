# coding=utf-8
import typing


class Val:

    @staticmethod
    def _convert_case(name: str) -> str:
        components = name.split('_')
        return components[0] + "".join(x.title() for x in components[1:])

    def __init__(self, parser: callable, mandatory: bool = True):
        self.owner = None
        self.name = None
        self.parser = parser
        self.mandatory = mandatory

    def __set_name__(self, owner: object, name: str):
        self.owner = owner
        self.name = self._convert_case(name)

    def __get__(self, instance: 'GenericBuild', owner: object) -> typing.Union[str, int, list, 'Val', None]:
        if not instance:
            return self

        if owner is not self.owner:
            raise RuntimeError(f'owners differ: "{owner}" vs "{self.owner}"')

        try:
            return self.parser(getattr(instance, '_json')[self.name])
        except KeyError:
            if self.mandatory:
                raise
            return None
