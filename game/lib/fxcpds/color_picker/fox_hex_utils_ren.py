# Copyright 2023 Elizabeth Paige Harper
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# From: https://github.com/Foxcapades/renpy-util-hex
# Version: 2.1.0

from fox_requirement_ren import FoxRequire

"""renpy
init -10 python:
"""


class FoxHex(object):

    @staticmethod
    def ubyte_to_hex(byte: int, upper: bool = False) -> str:
        """
        UByte to Hex

        Converts the given ubyte value to a hex character pair in a string.

        Arguments
        ---------
        byte : int
            UByte value to convert to hex.  This value must be between 0 and 255
            (inclusive) or an exception will be raised.
        upper : bool
            Flag indicating whether the returned hex should be uppercase.

        Returns
        -------
        str
            A 2 character hex string representing the given ubyte value.
        """
        byte = FoxRequire.enforce_int('byte', byte)
        upper = FoxRequire.require_bool('upper', upper)

        if byte > 255 or byte < 0:
            raise Exception('"byte" must be between 0 and 255 (inclusive)')

        return FoxHex.__seg_to_hex(byte >> 4, upper) + FoxHex.__seg_to_hex(byte & 15, upper)

    @staticmethod
    def ubytes_to_hex(bytes: any, prefix: str = '', upper: bool = False) -> str:
        """
        UByte Iterable to Hex

        Takes the given list, tuple, or other iterable and translates the ubyte
        values fetched from that iterable into a singular hex string.

        The iterable is expected to return the ubytes in big-endian order.

        Arguments
        ---------
        bytes : any
            A list, tuple, or other iterable type from which ubyte values will be
            retrieved.
        prefix : str
            Optional prefix that will be prepended to the output hex string.  Common
            examples are '#' or '0x'.
        upper : bool
            Flag indicating whether the returned hex should be uppercase.

        Returns
        -------
        str
            A hex string built from the bytes retrieved from the given list, tuple,
            or iterable.
        """

        FoxRequire.require_str('prefix', prefix)
        FoxRequire.require_bool('upper', upper)

        if hasattr(bytes, '__iter__'):
            return prefix + FoxHex.__bytes_to_hex(bytes, upper)

        else:
            raise Exception('"bytes" must be a list, tuple, or other iterable of ubyte values.')

    @staticmethod
    def int_to_hex(
        value: int,
        min_width: int = 2,
        prefix: str = '',
        upper: bool = False
    ) -> str:
        """
        Int to Hex

        Converts the given int value into a hex string with an optional prefix.

        Int values must be greater than or equal to zero.

        Arguments
        ---------
        value : int
            Positive int value to convert to a hex string.
        min_width : int
            Positive int value that specifies the minimum width of the returned hex
            string (minus the prefix).  If the int value is not large enough to meet
            this minimum width, the hex string will be padded with zeros.

            Default = 2
        prefix : str
            Optional prefix value that will be prepended onto the returned hex
            value.  Common examples include '#' and '0x'.

            Default = ''
        upper : bool
            Whether the returned hex string should be uppercased.

            Default = False

        Returns
        -------
        str
            Generated hex string.
        """

        value = FoxRequire.enforce_int('value', value)
        if value < 0:
            raise Exception('negative values not supported')

        min_width = FoxRequire.enforce_int('min_width', min_width)
        if min_width < 0:
            raise Exception('min_width must be greater than or equal to zero')

        FoxRequire.require_str('prefix', prefix)
        FoxRequire.require_bool('upper', upper)

        # If the value is zero, then no need to do any math, just return a string
        # of zeros.
        if value == 0:
            return prefix + ('0' * min_width)

        out = ''

        # Convert the int value to a hex string.
        while value > 0:
            byte = value & 255
            value = value >> 8

            out = FoxHex.ubyte_to_hex(byte, upper) + out

        # Figure out if we need to pad the string with zeros to get to the target
        # width.
        rem_width = min_width - len(out)

        if rem_width > 0:
            out = ('0' * rem_width) + out

        # Prepend the prefix and return the value.
        return prefix + out

    @staticmethod
    def hex_to_ubytes(value: str, prefix: str = '') -> list[int]:
        """
        Hex to UBytes

        Converts the given hex string into a list of ubyte values.

        Arguments
        ---------
        value : str
            Hex string that will be parsed into a list of ubytes.
        prefix : str
            Prefix that will be stripped off the given value before it is parsed.

        Returns
        -------
        list[int]
            A list of ubyte values parsed from the given hex string.
        """
        FoxRequire.require_str('value', value)
        FoxRequire.require_str('prefix', prefix)

        value = FoxHex.__trim_and_validate_hex_string(value, prefix)

        if len(value) == 0:
            return []

        o = []
        l = len(value)
        i = 0

        while i < l:
            o.append(FoxHex.__hex_to_byte(value[i], value[i + 1]))
            i += 2

        return o

    @staticmethod
    def hex_to_int(value: str, prefix: str = '') -> int:
        """
        Hex to Int

        Converts the given hex string into an int value.  Hex string is considered
        big-endian.

        Arguments
        ---------
        value : str
            Hex string that will be parsed into an int value.
        prefix : str
            Prefix that will be stripped off the given value before it is parsed.

        Returns
        -------
        int
            The int value parsed from the given hex string.
        """

        FoxRequire.require_str('value', value)
        FoxRequire.require_str('prefix', prefix)

        value = FoxHex.__trim_and_validate_hex_string(value, prefix)

        if len(value) == 0:
            raise Exception('cannot parse an int value from an empty hex string')

        o = 0
        l = len(value)
        i = 0

        while i < l:
            o = (o << 4) | FoxHex.__hex_to_seg(value[i])
            o = (o << 4) | FoxHex.__hex_to_seg(value[i + 1])
            i += 2

        return o

    @staticmethod
    def hex_is_valid(hex: str) -> bool:
        """
        Tests if the given string is a valid hex string.  This assumes any prefixes
        have been removed before testing.

        :param hex: String to test.

        :returns: Whether the given value was a valid hex string.
        """
        if not isinstance(hex, str):
            return False

        for c in hex:
            if not FoxHex.__is_hex_digit(c):
                return False

        return True

    ############################################################################
    #
    #    Internal Functions
    #
    ############################################################################

    @staticmethod
    def __trim_and_validate_hex_string(value: str, prefix: str = '') -> str:
        if len(prefix) > 0 and value.startswith(prefix):
            value = value[len(prefix):]

        for c in value:
            if not FoxHex.__is_hex_digit(c):
                raise Exception(f"character '{c}' is not a valid hex digit")

        if len(value) % 2 == 1:
            value = '0' + value

        return value

    @staticmethod
    def __bytes_to_hex(bytes: any, upper: bool = False) -> str:
        out = ""

        for byte in bytes:
            out += FoxHex.ubyte_to_hex(byte, upper)

        if len(out) == 0:
            raise Exception('cannot build a hex string without at least one byte')

        return out

    @staticmethod
    def __seg_to_hex(seg: int, upper: bool = False) -> str:
        if seg < 10:
            return chr(seg + 48)
        elif seg < 16:
            return chr((seg - 10) + (65 if upper else 97))
        else:
            raise Exception("illegal state")

    @staticmethod
    def __hex_to_byte(seg1: str, seg2: str) -> int:
        return (FoxHex.__hex_to_seg(seg1) << 4) | FoxHex.__hex_to_seg(seg2)

    @staticmethod
    def __hex_to_seg(hex: str) -> int:
        if '0' <= hex <= '9':
            return ord(hex) - 48
        elif 'A' <= hex <= 'F':
            return ord(hex) - 55
        elif 'a' <= hex <= 'f':
            return ord(hex) - 87
        else:
            raise Exception("invalid hex digit '{}'".format(hex))

    @staticmethod
    def __is_hex_digit(digit: str) -> bool:
        c = ord(digit)
        return 48 <= c <= 57 or 65 <= c <= 70 or 97 <= c <= 102
