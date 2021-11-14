from ..restricted import Restricted
from os import linesep
import pytest


class TestRestricted:
    def test_new(self):
        """Create new instance of Restricted class"""
        r = Restricted({'attr_a': 'a', 'attr_b': 'b', 'attr_z': 'z'})
        assert r.attr_a == 'a'
        print("STDOUT of the test")

    @pytest.fixture()
    def restricted(self):
        return Restricted({'attr_a': 'a', 'attr_b': 'b', 'attr_c': 'c'})

    def test_prop_access(self, restricted):
        """Access to object attributes"""
        assert restricted.attr_a == 'a'
        assert restricted.attr_b == 'b'
        assert restricted.attr_c == 'c'
        assert restricted['attr_a'] == 'a'
        assert restricted['attr_b'] == 'b'
        assert restricted['attr_c'] == 'c'

    def test_eq(self):
        """Equal method"""
        restricted1 = Restricted({'attr_a': 'a', 'attr_b': 'b', 'attr_c': 'c'})
        restricted2 = Restricted({'attr_a': 'a', 'attr_b': 'b', 'attr_c': 'c'})
        restricted3 = Restricted({'attr_a': 'a', 'attr_b': 'b'})
        assert restricted1 == restricted2
        assert restricted1 != restricted3

    def test_contains(self, restricted):
        """Contains method"""
        assert 'attr_a' in restricted
        assert 'attr_z' not in restricted

    def test_setattr(self, restricted):
        """Assignment method"""
        restricted.attr_a = 'aa'
        assert restricted.attr_a == 'aa'
        restricted['attr_b'] = 'bb'
        assert restricted['attr_b'] == 'bb'

    def test_str(self, restricted):
        """Object to string"""
        expected = 'Restricted' + linesep
        expected += '    attr_a: a' + linesep
        expected += '    attr_b: b' + linesep
        expected += '    attr_c: c'
        assert str(restricted) == expected

    def test_attribute_error(self, restricted):
        """Exceptions, not allowed attribute"""
        with pytest.raises(AttributeError):
            restricted.attr_z

        with pytest.raises(AttributeError):
            restricted.attr_z = 'z'

        with pytest.raises(AttributeError):
            restricted['attr_z']

        with pytest.raises(AttributeError):
            restricted['attr_z'] = 'z'
