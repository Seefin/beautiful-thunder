#!/usr/bin/env python3


import pprint
from enum import IntFlag, StrEnum

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

class ConstantPoolStrings(StrEnum):
    Utf8               ="CONSTANT_Utf8"
    Integer            ="CONSTANT_Integer"
    Float              ="CONSTANT_Float"
    Long               ="CONSTANT_Long"
    Double             ="CONSTANT_Double"
    Class              ="CONSTANT_Class"
    String             ="CONSTANT_String"
    Fieldref           ="CONSTANT_Fieldref"
    Methodref          ="CONSTANT_Methodref"
    InterfaceMethodref ="CONSTANT_InterfaceMethodref"
    NameAndType        ="CONSTANT_NameAndType"
    MethodHandle       ="CONSTANT_MethodHandle"
    MethodType         ="CONSTANT_MethodType"
    Dynamic            ="CONSTANT_Dynamic"
    InvokeDynamic      ="CONSTANT_InvokeDynamic"
    Module             ="CONSTANT_Module"
    Package            ="CONSTANT_Package"

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
    constant_pool = []
    for i in range(constant_pool_count-1):
        cp_info = {}
        tag = GetInt(1, f)
        if tag == ConstantPoolTypes.Methodref:
            cp_info['tag'] = ConstantPoolStrings.Methodref
            cp_info['class_index'] = GetInt(2, f)
            cp_info['name_and_type_index'] = GetInt(2,f)
            constant_pool.append(cp_info)
        elif tag == ConstantPoolTypes.Class:
            cp_info['tag'] = ConstantPoolStrings.Class
            cp_info['name_index'] = GetInt(2, f)
            constant_pool.append(cp_info)
        else:
            print(f"Nothing for {tag} yet")
    print(f"clazz: {clazz}")
    pp.pprint(constant_pool)
