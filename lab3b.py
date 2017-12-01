#!/usr/bin/env python3

# NAME: Dawei Huang, Nathan Smith
# EMAIL: daweihuang@ucla.edu, nathan.smith@ucla.edu
# ID: 304792166, 704787554

import sys
import os
import csv
from typing import List

# def print_reserved_blocks(blocks, indirection_level, block_address,
#                           inode_number, first_non_reserved_num):
#     if block_address < first_non_reserved_num and block_address not in blocks:
#         print("RESERVED {} {} IN INODE {} AT OFFSET {}".format(
#             indir_str(indirection_level), block_address, inode_number,
#             indir_offset(indirection_level)))

#     blocks[block_address] = ("reserved", indirection_level, inode_number,
#                                    False)


# def print_invalid_blocks(blocks, indirection_level, block_address,
#                          inode_number, limit):
#     if block_address < 0 or block_address >= limit:
#         print("INVALID {} {} IN INODE {} AT OFFSET {}".format(
#             indir_str(indirection_level), block_address, inode_number,
#             indir_offset(indirection_level)))

#     blocks[block_address] = ("reserved", indirection_level, inode_number,
#                                    False)


# def print_duplicate_blocks(block_address, indirection_level, inode_number):
#     print("DUPLICATE {} {} IN INODE {} AT OFFSET {}".format(
#         indir_str(indirection_level), block_address, inode_number,
#         indir_offset(indirection_level)))


# def indir_str(indirection_level):
#     indir_str = ""
#     if indirection_level == 1:
#         indir_str = "INDIRECT "
#     elif indirection_level == 2:
#         indir_str = "DOUBLE INDIRECT "
#     elif indirection_level == 3:
#         indir_str = "TRIPLE INDIRECT "
#     indir_str = indir_str + "BLOCK"
#     return indir_str


# def indir_offset(indirection_level):
#     offset = 0
#     if indirection_level == 1:
#         offset = 12
#     elif indirection_level == 2:
#         offset = 256 + 12
#     elif indirection_level == 3:
#         offset = 256**2 + 256 + 12
#     return offset


# def block_audit(file_list):
#     block_size = 0
#     inode_size = 0
#     num_of_blocks_in_this_group = 0
#     num_of_inodes_in_this_group = 0
#     first_block_inode = 0
#     first_non_reserved_num = 0
#     indirection_level = 0
#     block_address = 0
#     inode_number = 0
#     blocks = {}

#     # print(type(file_list))

#     for line in file_list:
#         if line[0] == "SUPERBLOCK":
#             block_size = int(line[3])
#             inode_size = int(line[4])
#         elif line[0] == "GROUP":
#             num_of_blocks_in_this_group = int(line[2])
#             num_of_inodes_in_this_group = int(line[3])
#             first_block_inode = int(line[8])
#             first_non_reserved_num = int(first_block_inode + (
#                 (inode_size * num_of_inodes_in_this_group) / block_size))
#         elif line[0] == "BFREE":
#             block_address = int(line[1])
#             blocks[block_address] = ("free")
#         elif line[0] == "INODE":
#             block_addresses = line[12:]
#             inode_number = int(line[1])
#             length = len(block_addresses)
#             for index, block_address in enumerate(block_addresses):
#                 block_address = int(block_address)

#                 if block_address == 0:
#                     continue

#                 indirection_level = 0
#                 if index == length - 3:
#                     indirection_level = 1
#                 elif index == length - 2:
#                     indirection_level = 2
#                 elif index == length - 1:
#                     indirection_level = 3

#                 if block_address in blocks:
#                     if blocks[block_address][0] == "free":
#                         print("ALLOCATED BLOCK {} ON FREELIST".format(
#                             block_address))
#                     else:
#                         # how to handle duplicate
#                         print_duplicate_blocks(block_address,
#                                                indirection_level, inode_number)
#                         # [3] checks to see if this duplicate block has been printed out before
#                         if blocks[block_address][3] is False:
#                             blocks[block_address][3] = True
#                             print_duplicate_blocks(
#                                 block_address, blocks[block_address][1],
#                                 blocks[block_address][2])

#                 # how to find invalid blocks
#                 print_invalid_blocks(blocks, indirection_level,
#                                      block_address, inode_number,
#                                      num_of_blocks_in_this_group)

#                 # how to find reserved blocks
#                 print_reserved_blocks(blocks, indirection_level,
#                                       block_address, inode_number,
#                                       first_non_reserved_num)

#         elif line[0] == "INDIRECT":
#             inode_number = int(line[1])
#             indirection_level = int(line[2])
#             block_address = int(line[5])

#             if block_address in blocks:
#                 if blocks[block_address][0] == "free":
#                     print(
#                         "ALLOCATED BLOCK {} ON FREELIST".format(block_address))
#                 else:
#                     # how to handle duplicate
#                     print_duplicate_blocks(block_address, indirection_level,
#                                            inode_number)
#                     # [3] checks to see if this duplicate block has been printed out before
#                     if blocks[block_address][3] is False:
#                         blocks[block_address][3] = True
#                         print_duplicate_blocks(block_address,
#                                                blocks[block_address][1],
#                                                blocks[block_address][2])

#             # how to find invalid blocks
#             print_invalid_blocks(blocks, indirection_level,
#                                  block_address, inode_number,
#                                  num_of_blocks_in_this_group)

#             # how to find reserved blocks
#             print(block_address)
#             print_reserved_blocks(blocks, indirection_level,
#                                   block_address, inode_number,
#                                   first_non_reserved_num)

#     # how to find unreferenced blocks
#     for block_num in range(first_non_reserved_num,
#                            num_of_blocks_in_this_group):
#         if block_num not in blocks:
#             print("UNREFERENCED BLOCK {}".format(block_num))


# def inode_audit(file_list):
#     inode_free_list = {}
#     inode_allocated_list = []
#     first_non_reserved_inode = 0
#     total_num_of_inodes = 0
#     inode_allocated_list = {}

#     for line in file_list:
#         if line[0] == "SUPERBLOCK":
#             total_num_of_inodes = int(line[2])
#             first_non_reserved_inode = int(line[7])

#         elif line[0] == "IFREE":
#             inode_number = int(line[1])
#             inode_free_list[inode_number] = True

#         elif line[0] == "INODE":
#             inode_number = int(line[1])
#             if inode_number in inode_free_list and inode_free_list[inode_number] is True:
#                 print("ALLOCATED INODE {} ON FREELIST".format(inode_number))
#             inode_free_list[inode_number] = False

#     # how to find unallocated inodes
#     for inode_number in range(first_non_reserved_inode, total_num_of_inodes):
#         if inode_number not in inode_free_list:
#             print("UNALLOCATED INODE {} NOT ON FREELIST".format(inode_number))
#         else:
#             inode_allocated_list[inode_number] = (0, 0, 0)

#     return inode_allocated_list


# def directory_audit(file_list, inode_allocated_list):
#     total_num_of_inodes = 0
#     for line in file_list:
#         if line[0] == "SUPERBLOCK":
#             total_num_of_inodes = int(line[7])
#             break

#     for line in file_list:
#         if line[0] == "INODE":
#             i_num = int(line[1])
#             inode_allocated_list[i_num][1] = int(line[6])

#     for line in file_list:
#         if line[0] == "DIRENT":
#             directory_inode = int(line[1])
#             dirent_inode = int(line[3])
#             dir_str = line[6]

#             if dirent_inode not in inode_allocated_list:
#                 print("DIRECTORY INODE {} NAME {} UNALLOCATED INODE {}".format(
#                     directory_inode, dir_str, dirent_inode))
#             else:
#                 if dirent_inode < 1 or dirent_inode > total_num_of_inodes:
#                     print("DIRECTORY INODE {} NAME {} INVALID INODE {}".format(
#                         directory_inode, dir_str, dirent_inode))
#                 else:
#                     inode_allocated_list[dirent_inode][0] += 1
#                     if inode_allocated_list[dirent_inode][3] == 0:
#                         inode_allocated_list[dirent_inode][
#                             3] == directory_inode

#             if dir_str == "." and dirent_inode != directory_inode:
#                 print(
#                     "DIRECTORY INODE {} NAME {} LINK TO INODE {} SHOULD BE {}".
#                     format(directory_inode, dir_str, dirent_inode,
#                            directory_inode))
#             elif dir_str == ".." and inode_allocated_list[directory_inode][2] != dirent_inode:
#                 print(
#                     "DIRECTORY INODE {} NAME {} LINK TO INODE {} SHOULD BE {}".
#                     format(directory_inode, dir_str, dirent_inode,
#                            inode_allocated_list[directory_inode][2]))

#     for inode_number in inode_allocated_list:
#         if inode_allocated_list[inode_number][0] != inode_allocated_list[inode_number][1]:
#             print("INODE {} HAS {} LINKS BUT LINKCOUNT IS {}".format(
#                 inode_number, inode_allocated_list[inode_number][0],
#                 inode_allocated_list[inode_number][1]))


class Inode:
    def __init__(self, number, allocated):
        self.number = number
        self.allocated = allocated


class Block:
    def __init__(self, indirection_level, block_address, inode_number, offset):
        self.indirection_level = indirection_level
        self.block_address = block_address
        self.inode_number = inode_number
        self.offset = offset


block_size: int
inode_size: int

free_inode_numbers: List[int] = []
inodes: List[Inode] = []
directories = []


def process_file(file):
    for line in file_list:
        if line[0] == "SUPERBLOCK":
            block_size = int(line[3])
            inode_size = int(line[4])
        elif line[0] == "GROUP":
            num_of_blocks_in_this_group = int(line[2])
            num_of_inodes_in_this_group = int(line[3])
            first_block_inode = int(line[8])
            first_non_reserved_num = int(first_block_inode + (
                (inode_size * num_of_inodes_in_this_group) / block_size))
        elif line[0] == "IFREE":
            free_inode_number = int(line[1])
            free_inode_numbers.append(free_inode_number)
        # elif line[0] == "DIRENT":
        # directory_entry =
        elif line[0] == "INODE":
            inode_number = int(line[1])
            allocated = True if line[2] == 0 else False
            inodes.append(Inode(inode_number, allocated))


def inode_audit():
    for inode in inodes:
        if inode.allocated and inode.number in free_inode_numbers:
            print("ALLOCATED INODE {} ON FREELIST".format(inode.number))
        elif not inode.allocated and inode.number not in free_inode_numbers:
            print("UNALLOCATED INODE {} NOT ON FREELIST".format(inode.number))


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

            # block_audit(file_list)
            inode_audit()
            # directory_audit(file_list, inode_allocated_list)
    except EnvironmentError:
        print("[Error]: Error reading file.", file=sys.stderr)
        sys.exit(1)
