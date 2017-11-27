#!/usr/bin/env python3

# NAME: Dawei Huang, Nathan Smith
# EMAIL: daweihuang@ucla.edu, nathan.smith@ucla.edu
# ID: 304792166, 704787554

import sys
import os


def block_audit(file_list):
    block_size = 0
    inode_size = 0
    num_of_blocks_in_this_group = 0
    num_of_inodes_in_this_group = 0
    first_block_inode = 0
    first_non_reserved_num = 0
    indirection_level = 0
    block_num = 0
    inode_num = 0
    block_list = []
    
    #print(type(file_list))
    
    for line in file_list:
        #print(type(line))
        if line[0] == "SUPERBLOCK":
            block_size = int(line[3])
            inode_size = int(line[4])

        if line[0] == "GROUP":
            num_of_blocks_in_this_group = int(line[2])
            num_of_inodes_in_this_group = int(line[3])
            first_block_inode = int(line[8])
            first_non_reserved_num = first_block_inode + inode_size*num_of_inodes_in_this_group/block_size

        if line[0] == "BFREE":
            block_num = line[1]
            block_list.append(block_num)

        if line[0] == "INODE":
            block_addresses = line[12:]
            inode_number = line[1]
            len_ = len(block_addresses)
            for index, block_address in enumerate(block_addresses):
                block_address = int(block_address)
                if block_address == 0:
                    continue

                if block_address in block_bitmap:
                    print("ALLOCATED BLOCK " + block_address + " ON FREELIST")

                indir_str = ""
                if index == len_ - 3:
                    indir_str = "INDIRECT"
                if index == len_ - 2:
                    indir_str = "DOUBLE INDIRECT"
                if index == len_ - 1:
                    indir_str = "TRIPLE INDIRECT"
                indir_str = indir_str + " BLOCK"
                

if __name__ == "__main__":
    if len(sys.argv[1:]) != 1:
        print("[Error]: Incorrect number of arguments.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print("[Error]: File does not exist.", file=sys.stderr)
        sys.exit(1)if len(sys.argv) != 2:
        sys.stderr.write("Must have one arguments\n")
        exit(1)

    file_system = sys.argv[1]
    with open(file_system, 'r') as file:
        file_list = csv.reader(file)
        block_audit(file_list)

    # Block Consistency Audits
    # I-node Allocation Audits
    # Directory Consistency Audits
