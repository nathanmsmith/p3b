#!/usr/bin/env python3

# NAME: Dawei Huang, Nathan Smith
# EMAIL: daweihuang@ucla.edu, nathan.smith@ucla.edu
# ID: 304792166, 704787554

import sys
import os
import csv


def print_reserved_blocks(block_bitmap, indirection_level, block_address, inode_number, first_non_reserved_num):
    if block_address < first_non_reserved_num and block_address not in block_bitmap:
        print("RESERVED " + indir_str(indirection_level) + " " + block_address +
              " IN INODE " + inode_number + " AT OFFSET " + indir_offset(indirection_level))
        block_bitmap[block_address] = ("reserved", indirection_level, inode_number, False)


def print_invalid_blocks(block_bitmap, indirection_level, block_address, inode_number, limit):

    if block_address < 0 or block_address >= limit:
        print("INVALID " + indir_str(indirection_level) + " " + block_address +
              " IN INODE " + inode_number + " AT OFFSET " + indir_offset(indirection_level))
        block_bitmap[block_address] = ("invalid", indirection_level, inode_number, False)

def print_duplicate_blocks(block_address, indirection_level, inode_number):
    print("DUPLICATE " + indir_str(indirection_level) + " " + block_address + " IN INODE " + inode_number + " AT OFFSET " + indir_offset(indirection_level))

def indir_str(indirection_level):
    indir_str = ""
    if indirection_level == 1:
        indir_str = "INDIRECT"
    elif indirection_level == 2:
        indir_str = "DOUBLE INDIRECT"
    elif indirection_level == 3:
        indir_str = "TRIPLE INDIRECT"
    indir_str = indir_str + " BLOCK"
    return indir_str

def indir_offset(indirection_level):
    offset = 0
    if indirection_level == 1:
        offset = 12
    elif indirection_level == 2:
        offset = 256 + 12
    elif indirection_level == 3:
        offset = 256 * 256 + 256 + 12
    return offset

def block_audit(file_list):
    block_size = 0
    inode_size = 0
    num_of_blocks_in_this_group = 0
    num_of_inodes_in_this_group = 0
    first_block_inode = 0
    first_non_reserved_num = 0
    indirection_level = 0
    block_address = 0
    inode_number = 0
    block_bitmap = {}
    offset = 0
    duplicate_map = {}

    # print(type(file_list))

    for line in file_list:
        # print(type(line))
        if line[0] == "SUPERBLOCK":
            block_size = int(line[3])
            inode_size = int(line[4])

        if line[0] == "GROUP":
            num_of_blocks_in_this_group = int(line[2])
            num_of_inodes_in_this_group = int(line[3])
            first_block_inode = int(line[8])
            first_non_reserved_num = first_block_inode + \
                inode_size * num_of_inodes_in_this_group / block_size

        if line[0] == "BFREE":
            block_address = line[1]
            block_bitmap[block_address] = ("free")

        if line[0] == "INODE":
            block_addresses = line[12:]
            inode_number = line[1]
            length = len(block_addresses)
            for index, block_address in enumerate(block_addresses):
                block_address = int(block_address)
                if block_address == 0:
                    continue

                indirection_level = 0
                if index == length - 3:
                    indirection_level = 1
                elif index == length - 2:
                    indirection_level = 2
                elif index == length - 1:
                    indirection_level = 3
                
                if block_address in block_bitmap:
                    if block_bitmap[block_address][0] == "free":
                        print("ALLOCATED BLOCK " +
                              block_address + " ON FREELIST")
                    else:
                        # how to handle duplicate
                        print_duplicate_blocks(block_address, indirection_level, inode_number)
                        # [3] checks to see if this duplicate block has been printed out before
                        if block_bitmap[block_address][3] == False:
                            block_bitmap[block_address][3] = True
                            print_duplicate_blocks(block_address, block_bitmap[block_address][1], block_bitmap[block_address][2])

                # how to find invalid blocks
                print_invalid_blocks(block_bitmap, indirection_level, block_address,
                                     inode_number, num_of_blocks_in_this_group)

                # how to find reserved blocks
                print_reserved_blocks(
                    block_bitmap, indirection_level, block_address, inode_number, first_non_reserved_num)

        if line[0] == "INDIRECT":
            inode_number = line[1]
            indirection_level = line[2]
            block_address = line[5]

            if block_address in block_bitmap:
                if block_bitmap[block_address][0] == "free":
                    print("ALLOCATED BLOCK " +
                              block_address + " ON FREELIST")
                else:
                     # how to handle duplicate
                    print_duplicate_blocks(block_address, indirection_level, inode_number)
                    # [3] checks to see if this duplicate block has been printed out before
                    if block_bitmap[block_address][3] == False:
                        block_bitmap[block_address][3] = True
                        print_duplicate_blocks(block_address, block_bitmap[block_address][1], block_bitmap[block_address][2])

            # how to find invalid blocks
            print_invalid_blocks(block_bitmap, indirection_level, block_address,
                                     inode_number, num_of_blocks_in_this_group)

            # how to find reserved blocks
            print_reserved_blocks(
                    block_bitmap, indirection_level, block_address, inode_number, first_non_reserved_num)

        # how to find unreferenced blocks
        for block_number in range(first_non_reserved_num, num_of_blocks_in_this_group):
            if block_number not in block_bitmap:
                print("UNREFERENCED BLOCK " + str(block_number))

def inode_audit(file_list):
    inode_bitmap = {}
    for line in file_list:
        if line[0] == "SUPERBLOCK":
            inode_number = 
        
        

if __name__ == "__main__":
    if len(sys.argv[1:]) != 1:
        print("[Error]: Incorrect number of arguments.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print("[Error]: File does not exist.", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) != 2:
        sys.stderr.write("Must have one arguments\n")
        exit(1)

    file_system = sys.argv[1]
    with open(file_system, 'r') as file:
        file_list = csv.reader(file)
        block_audit(file_list)
        inode_audit(file_list)

    # Block Consistency Audits
    # I-node Allocation Audits
    # Directory Consistency Audits
