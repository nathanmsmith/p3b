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
    def __init__(self, indirection_level, address, inode_number):
        self.indirection_level = indirection_level
        self.address = address
        self.inode_number = inode_number

        offset = 0
        if self.indirection_level == 1:
            offset = 12
        elif self.indirection_level == 2:
            offset = 256 + 12
        elif self.indirection_level == 3:
            offset = 256**2 + 256 + 12
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
totol_inode_number: int

block_size: int
inode_size: int

free_block_numbers: List[int] = []
blocks: List[Block] = []
free_inode_numbers: List[int] = []
inodes: List[Inode] = []

directories = []


def process_file(file):
    global total_block_number, total_inode_number

    for line in file_list:
        if line[0] == "SUPERBLOCK":
            total_block_number = int(line[1])
            total_inode_number = int(line[2])
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

            # Process Blocks
            block_addresses = [int(a) for a in line[12:]]
            length = len(block_addresses)
            for index, block_address in enumerate(block_addresses):
                if block_address != 0:
                    indirection_level = 0
                    if index == length - 3:
                        indirection_level = 1
                    elif index == length - 2:
                        indirection_level = 2
                    elif index == length - 1:
                        indirection_level = 3
                    blocks.append(
                        Block(indirection_level, block_address, inode_number))


def block_audit():
    for block in blocks:
        if block.address > total_block_number - 1:
            print("INVALID {} {} IN INODE {} AT OFFSET {}".format(
                block.indir_str(), block.address, block.inode_number,
                block.offset))
        elif block.address < 8:
            print("RESERVED {} {} IN INODE {} AT OFFSET {}".format(
                block.indir_str(), block.address, block.inode_number,
                block.offset))

    # block_addresses = [block.address for block in blocks]
    # for block_address in range(8, total_block_number):
    #     if block_address not in free_block_numbers and block not in block_addresses:
    #         print("UNREFERENCED BLOCK {}".format(block.address))
    #     elif block_address in free_block_numbers and block in block_addresses:
    #         print("ALLOCATED BLOCK {} ON FREELIST".format(block.address))


def inode_audit():
    global allocated_inodes

    for inode in inodes:
        if inode.allocated and inode.number in free_inode_numbers:
            print("ALLOCATED INODE {} ON FREELIST".format(inode.number))
        elif not inode.allocated and inode.number not in free_inode_numbers:
            print("UNALLOCATED INODE {} NOT ON FREELIST".format(inode.number))


def get_directory_from_inode_number(inode_number):
    for directory in directories:
        if directory.inode_number == inode_number:
            return directory
    return None

def directory_audit():
    for directory in directories:
        if directory.inode_number > total_inode_number:
            print("DIRECTORY INODE {} NAME {} INVALID INODE {}".format(
                directory.parent_inode, directory.file_name, directory.inode_number
            ))
        elif directory.inode_number in free_inode_numbers:
            print("DIRECTORY INODE {} NAME {} UNALLOCATED INODE {}".format(
                directory.parent_inode, directory.file_name,
                directory.inode_number))
        else:
            directory.link_count += 1

    for inode in inodes:
        directory = get_directory_from_inode_number(inode.number)
        if directory is not None:
            if inode.link_count != directory.link_count:
                print("INODE {} HAS {} LINKS BUT LINKCOUNT IS {}".format(
                    inode.number, directory.link_count, inode.link_count))


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
