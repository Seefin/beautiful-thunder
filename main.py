#!/usr/bin/env python3


import pprint
from enum import IntFlag

class ConstantPoolTypes(IntFlag):
    Utf8               =1
    Integer            =3
    Float              =4
    Long               =5
    Double             =6
    Class              =7
    String             =8
    Fieldref           =9
    Methodref          =10
    InterfaceMethodref =11
    NameAndType        =12
    MethodHandle       =15
    MethodType         =16
    Dynamic            =17
    InvokeDynamic      =18
    Module             =19
    Package            =20

file_path = "./Main.class"
pp = pprint.PrettyPrinter()

def GetInt(count: int, f) -> int:
    return int.from_bytes(f.read(count), 'big')

def GetHex(count: int, f):
    return hex(int.from_bytes(f.read(count), 'big'))

with open(file_path, "rb") as f:
    clazz = {}
    clazz['magic'] = GetHex(4,f)
    clazz['minor'] = GetInt(2, f)
    clazz['major'] = GetInt(2, f)
    constant_pool_count = GetInt(2, f)
    for i in range(constant_pool_count-1):
        cp_info = {}
        cp_info['tag'] = GetInt(1,f)
        if cp_info['tag'] == ConstantPoolTypes.Methodref:
            cp_info['class_index'] = GetInt(2, f)
            cp_info['name_and_type_index'] = GetInt(2,f)
            pp.pprint(cp_info)
        else:
            assert False, f"Unexpected tag {cp_info['tag']}"
            exit(0)
    pp.pprint(clazz)
