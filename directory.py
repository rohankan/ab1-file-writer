import os

from utils import int_to_16_bit, int_to_32_bit, short_list, pascal_string
from typing import NamedTuple, BinaryIO, List, Optional, Union


BYTES_PER_DIR: int = 28
BYTES_PER_SHORT: int = 2


class Directory(NamedTuple):
    tag_name: str
    tag_num: int
    element_type_code: int
    element_size: int
    num_elements: int
    data: Union[bytes, bytearray] = b""

    @property
    def data_size(self) -> int:
        """
        Returns size of data stored in directory in bytes.
        :return: Size of data in bytes
        """
        return self.element_size * self.num_elements

    def write_to(self, ab1: BinaryIO, offset: int) -> None:
        """
        Writes directory to BinaryIO.
        :param ab1: BinaryIO instance
        :param offset: Offset from start (in bits) to data
        """
        if len(self.tag_name) != 4:
            raise ValueError("Directory tag_name must be 4 characters!")

        ab1.write(self.tag_name.encode())
        ab1.write(int_to_32_bit(self.tag_num))
        ab1.write(int_to_16_bit(self.element_type_code))
        ab1.write(int_to_16_bit(self.element_size))
        ab1.write(int_to_32_bit(self.num_elements))
        ab1.write(int_to_32_bit(self.data_size))

        # -- Data offset --
        if self.data_size > 4:
            ab1.write(int_to_32_bit(offset))
        else:
            ab1.write(int_to_32_bit(0))
            ab1.seek(-4, os.SEEK_CUR)
            ab1.write(self.data)
            ab1.seek(0, os.SEEK_END)

        # -- Reserved / data handle --
        reserved = int_to_32_bit(0)
        ab1.write(reserved)

    @staticmethod
    def root(num_dirs: int) -> "Directory":
        return Directory(
            tag_name="tdir",
            tag_num=1,
            element_type_code=1023,
            element_size=BYTES_PER_DIR,
            num_elements=num_dirs,
        )

    @staticmethod
    def peak_locations(locations: List[int]) -> "Directory":
        return Directory(
            tag_name="PLOC",
            tag_num=1,
            element_type_code=4,
            element_size=BYTES_PER_SHORT,
            num_elements=len(locations),
            data=short_list(locations),
        )

    @staticmethod
    def base_order(order: Optional[List[str]] = None) -> "Directory":
        if order is None:
            order = ["G", "A", "T", "C"]

        return Directory(
            tag_name="FWO_",
            tag_num=1,
            element_type_code=2,
            element_size=1,
            num_elements=4,
            data=("".join(order).encode()),
        )

    @staticmethod
    def sample_name(name: str) -> "Directory":
        name = pascal_string(name)
        return Directory(
            tag_name="SMPL",
            tag_num=1,
            element_type_code=18,
            element_size=1,
            num_elements=len(name),
            data=name,
        )

    @staticmethod
    def comment(comment: str) -> "Directory":
        comment = pascal_string(comment)
        return Directory(
            tag_name="CMNT",
            tag_num=1,
            element_type_code=18,
            element_size=1,
            num_elements=len(comment),
            data=comment,
        )

    @staticmethod
    def channel_data(tag_number: int, data: List[int]) -> "Directory":
        return Directory(
            tag_name="DATA",
            tag_num=tag_number,
            element_type_code=4,
            element_size=BYTES_PER_SHORT,
            num_elements=len(data),
            data=short_list(data),
        )

    @staticmethod
    def lane(lane_number: int) -> "Directory":
        return Directory(
            tag_name="LANE",
            tag_num=1,
            element_type_code=4,
            element_size=BYTES_PER_SHORT,
            num_elements=1,
            data=lane_number.to_bytes(2, "big"),
        )

    @staticmethod
    def base_calls(tag_number: int, fasta_sequence: str) -> "Directory":
        return Directory(
            tag_name="PBAS",
            tag_num=tag_number,
            element_type_code=2,
            element_size=1,
            num_elements=len(fasta_sequence),
            data=fasta_sequence.encode(),
        )

    @staticmethod
    def dye_signal_strength(
        strength_1: int,
        strength_2: int,
        strength_3: int,
        strength_4: int,
    ) -> "Directory":
        return Directory(
            tag_name="S/N%",
            tag_num=1,
            element_type_code=4,
            element_size=BYTES_PER_SHORT,
            num_elements=4,
            data=short_list([strength_1, strength_2, strength_3, strength_4]),
        )

    @staticmethod
    def mobility_filename(tag_number: int, filename: str) -> "Directory":
        filename = pascal_string(filename)
        return Directory(
            tag_name="PDMF",
            tag_num=tag_number,
            element_type_code=18,
            element_size=1,
            num_elements=len(filename),
            data=filename,
        )
