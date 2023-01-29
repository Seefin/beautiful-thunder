#!/usr/bin/env python3


import pprint
from enum import IntFlag, StrEnum
from io import BufferedReader

############### TYPE ENUMS ##################################
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

################## METHOD CONSTANTS ###############
file_path = "./Main.class"
pp = pprint.PrettyPrinter(indent=4)

############# USEFUL PARSING FUNCTIONS ############
def GetInt(count: int, f: BufferedReader) -> int:
    return int.from_bytes(f.read(count), 'big')

def GetHex(count: int, f: BufferedReader) -> str:
    return hex(int.from_bytes(f.read(count), 'big'))

def ParseFileToDict(filename: str) -> dict:
    clazz = {}
    with open(filename, "rb") as f:
        clazz['magic'] = GetHex(4,f)
        clazz['minor'] = GetInt(2, f)
        clazz['major'] = GetInt(2, f)
        constant_pool_count = GetInt(2, f)
        constant_pool = []
        for _ in range(constant_pool_count-1):
            cp_info = {}
            tag = GetInt(1, f)
            if tag == ConstantPoolTypes.Methodref:
                cp_info['tag'] = ConstantPoolStrings.Methodref
                cp_info['class_index'] = GetInt(2, f)
                cp_info['name_and_type_index'] = GetInt(2,f)
            elif tag == ConstantPoolTypes.Class:
                cp_info['tag'] = ConstantPoolStrings.Class
                cp_info['name_index'] = GetInt(2, f)
            elif tag == ConstantPoolTypes.NameAndType:
                cp_info['tag'] = ConstantPoolStrings.NameAndType
                cp_info['name_index'] = GetInt(2, f)
                cp_info['descriptor_index'] = GetInt(2,f)
            elif tag == ConstantPoolTypes.Utf8:
                cp_info['tag'] = ConstantPoolStrings.Utf8
                cp_info['length'] = GetInt(2,f)
                cp_info['bytes'] = f.read(cp_info['length'])
            elif tag == ConstantPoolTypes.Fieldref:
                cp_info['tag'] = ConstantPoolStrings.Fieldref
                cp_info['class_index'] = GetInt(2, f)
                cp_info['name_and_type_index'] = GetInt(2, f)
            elif tag == ConstantPoolTypes.String:
                cp_info['tag'] = ConstantPoolStrings.String
                cp_info['string_index'] = GetInt(2, f)
            else:
                print(f"Nothing for {tag} yet")
            if cp_info: #Ignore the not implemented stuff
                constant_pool.append(cp_info)
        clazz['constant_pool'] = constant_pool
    return clazz

############## MAIN PARSING LOOP ###################
clazz = ParseFileToDict(file_path)
print(f"File {file_path} references these classes:")
for cp_info in clazz['constant_pool']:
    if cp_info['tag'] == ConstantPoolStrings.Class:
        print(f"       {clazz['constant_pool'][cp_info['name_index'] -1]['bytes']}")
