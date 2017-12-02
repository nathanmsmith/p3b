#!/usr/bin/env python3

# NAME: Dawei Huang, Nathan Smith
# EMAIL: daweihuang@ucla.edu, nathan.smith@ucla.edu
# ID: 304792166, 704787554

import sys
import os
import csv
from typing import List


class Inode:
    def __init__(self, number, allocated, link_count):
        self.number = number
        self.allocated = allocated
        self.link_count = link_count
        self.has_links = True if link_count > 0 else False


class Block:
    def __init__(self, indirection_level, number, inode_number, offset):
        self.indirection_level = indirection_level
        self.number = number
        self.inode_number = inode_number
        self.offset = offset

    def indir_str(self):
        indir_str = ""
        if self.indirection_level == 1:
            indir_str = "INDIRECT "
        elif self.indirection_level == 2:
            indir_str = "DOUBLE INDIRECT "
        elif self.indirection_level == 3:
            indir_str = "TRIPLE INDIRECT "
        indir_str = indir_str + "BLOCK"
        return indir_str


class Directory:
    def __init__(self, parent_inode, inode_number, file_name):
        self.parent_inode = parent_inode
        self.inode_number = inode_number
        self.file_name = file_name
        self.link_count = 0


errors = 0
total_block_number: int
total_inode_number: int

first_inode_number: int
block_size: int
inode_size: int

free_block_numbers: List[int] = []
blocks: List[Block] = []
free_inode_numbers: List[int] = []
inodes: List[Inode] = []

directories = []


def process_file(file):
    global total_block_number, total_inode_number, first_inode_number

    for line in file_list:
        if line[0] == "SUPERBLOCK":
            total_block_number = int(line[1])
            total_inode_number = int(line[2])
            first_inode_number = int(line[7])
            block_size = int(line[3])
            inode_size = int(line[4])
        # elif line[0] == "GROUP":
        #     num_of_blocks_in_this_group = int(line[2])
        #     num_of_inodes_in_this_group = int(line[3])
        #     first_block_inode = int(line[8])
        #     first_non_reserved_num = int(first_block_inode + (
        #         (inode_size * num_of_inodes_in_this_group) / block_size))
        elif line[0] == "BFREE":
            free_block_number = int(line[1])
            free_block_numbers.append(free_block_number)
        elif line[0] == "IFREE":
            free_inode_number = int(line[1])
            free_inode_numbers.append(free_inode_number)
        elif line[0] == "DIRENT":
            parent_inode = int(line[1])
            inode_number = int(line[3])
            file_name = line[6]
            directories.append(
                Directory(parent_inode, inode_number, file_name))
        elif line[0] == "INODE":
            # Process Inode
            inode_number = int(line[1])
            allocated = True if line[2] != "0" else False
            link_count = int(line[6])
            inodes.append(Inode(inode_number, allocated, link_count))

            # Process Direct Blocks and First Single, Double, and Triple Indirect Blocks
            block_numbers = [int(a) for a in line[12:24]]
            single_indirect_block_number = int(line[24])
            double_indirect_block_number = int(line[25])
            triple_indirect_block_number = int(line[26])

            for offset, block_number in enumerate(block_numbers):
                if block_number != 0:
                    blocks.append(Block(0, block_number, inode_number, offset))

            if single_indirect_block_number != 0:
                blocks.append(
                    Block(1, single_indirect_block_number, inode_number, 12))
            if double_indirect_block_number != 0:
                blocks.append(
                    Block(2, double_indirect_block_number, inode_number,
                          12 + 256))
            if triple_indirect_block_number != 0:
                blocks.append(
                    Block(3, triple_indirect_block_number, inode_number,
                          12 + 256 + 256**2))
        elif line[0] == "INDIRECT":
            # Indirect
            indirection_level = int(line[2])
            block_number = int(line[5])
            inode_number = int(line[1])
            offset = int(line[3])
            blocks.append(
                Block(indirection_level, block_number, inode_number, offset))
    # print([inode.number for inode in inodes])


def block_audit():
    for block in blocks:
        if block.number > total_block_number - 1:
            print("INVALID {} {} IN INODE {} AT OFFSET {}".format(
                block.indir_str(), block.number, block.inode_number,
                block.offset))
        elif block.number < 8:
            print("RESERVED {} {} IN INODE {} AT OFFSET {}".format(
                block.indir_str(), block.number, block.inode_number,
                block.offset))

    block_numbers = [block.number for block in blocks]
    for block_number in range(8, total_block_number):
        if block_number not in free_block_numbers and block_number not in block_numbers:
            print("UNREFERENCED BLOCK {}".format(block_number))
        elif block_number in free_block_numbers and block_number in block_numbers:
            print("ALLOCATED BLOCK {} ON FREELIST".format(block_number))

    # Find duplicate blocks
    # Use separate loop so we can remove block numbers
    for block_number in range(8, total_block_number):
        if block_number in block_numbers and block_numbers.count(
                block_number) > 1:
            duplicate_blocks = filter(
                lambda block: block.number == block_number, blocks)

            for duplicate_block in duplicate_blocks:
                print("DUPLICATE {} {} IN INODE {} AT OFFSET {}".format(
                    duplicate_block.indir_str(), duplicate_block.number,
                    duplicate_block.inode_number, duplicate_block.offset))


def inode_audit():
    global allocated_inodes

    for inode in inodes:
        if inode.allocated and inode.number in free_inode_numbers:
            print("ALLOCATED INODE {} ON FREELIST".format(inode.number))
        elif not inode.allocated and inode.number not in free_inode_numbers:
            print("UNALLOCATED INODE {} NOT ON FREELIST".format(inode.number))

    for inode_number in range(first_inode_number, total_inode_number):
        inode_numbers = [inode.number for inode in inodes]
        if inode_number not in inode_numbers and inode_number not in free_inode_numbers:
            print("UNALLOCATED INODE {} NOT ON FREELIST".format(inode_number))


def get_directory_from_inode_number(inode_number):
    for directory in directories:
        if directory.inode_number == inode_number:
            return directory
    return None


def directory_audit():

    # for directory in directories:
    #     print("{}: {}".format(directory.inode_number, directory.link_count))
    # print(type(directories))

    directory_list = [directory.inode_number for directory in directories]
    # print(directory_list)
    
    for inode in inodes:
        if inode.link_count != directory_list.count(inode.number):
            print("INODE {} HAS {} LINKS BUT LINKCOUNT IS {}".format(
                inode.number, directory_list.count(inode.number), inode.link_count))

    for directory in directories:
        if directory.inode_number > total_inode_number:
            print("DIRECTORY INODE {} NAME {} INVALID INODE {}".format(
                directory.parent_inode, directory.file_name,
                directory.inode_number))
        elif directory.inode_number in free_inode_numbers:
            print("DIRECTORY INODE {} NAME {} UNALLOCATED INODE {}".format(
                directory.parent_inode, directory.file_name,
                directory.inode_number))
        else:
            directory.link_count += 1




if __name__ == "__main__":
    if len(sys.argv[1:]) != 1:
        print("[Error]: Incorrect number of arguments.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print("[Error]: File does not exist.", file=sys.stderr)
        sys.exit(1)

    file_system = sys.argv[1]
    try:
        with open(file_system, 'r') as file:
            file_list = csv.reader(file)
            process_file(file_list)

            block_audit()
            inode_audit()
            directory_audit()
    except EnvironmentError:
        print("[Error]: Error reading file.", file=sys.stderr)
        sys.exit(1)

    # if errors > 0:
    #     exit(2)
    # else:
    #     exit(0)
