from __future__ import annotations
from typing import List, Optional, Dict
from enum import Enum
import copy
from backend.abstract import *

class SQLVariable():
    def __init__(self, name: str):
        self.name = name
        
class Column(SQLVariable):
    def __init__(self, tname: str, cname: str, dtype: str):
        super().__init__(f"{tname}.{cname}")
        self.tname = tname
        self.cname = cname
        self.dtype = dtype

class Table(SQLVariable):
    def __init__(self, name: str, columns: List[Column], struct: BackendType):
        super().__init__(name)
        self.columns = columns
        self.struct = struct
        

class Context():
    def __init__(self, tables: List[Table], rust_vars: List[BackendVariable]):
        self._def_code = []
        self._init_code = []
        self._process_code = []
        self._tables = {}
        for i in tables:
            self._tables[i.name] = i
        self._sql_vars = {}
        self._rust_vars = {}
        self.is_forward = False
    
    def explain(self):
        print("Tables:")
        for i in self.tables.values():
            print("\t", i.name)
            print("\t\t", i.struct.name)
           # print(i.columns)
        
        print("SQL Vars:") 
        for i in self.sql_vars.values():
            print("\t", i.name)
        
        print("Rust Vars:")
        for i in self.rust_vars.values():
            print("\t", i.name)
            print("\t\t", i.parent.name)
            print("\t\t", i.type)
            print("\t\t", i.init)
        
    
    def gen_struct_names(self) -> List[str]:
        ret = []
        for i in self.tables.values():
            if i.name == "input" or i.name == "output":
                continue
            ret.append(i.struct.name);
        return ret
    
    def gen_var_names(self) -> List[str]:
        ret = []
        for i in self.rust_vars.values():
            if i.parent is not None and (i.parent.name == "input" or i.parent.name == "output"):
                continue
            ret.append(i.name)
        return ret
    
    def gen_init_localvar(self) -> List[str]:
        ret = []
        for i in self.rust_vars.values():
            if i.parent is not None and (i.parent.name == "input" or i.parent.name == "output"):
                continue
            ret.append(i.gen_init_localvar())
        return ret
    
    def gen_struct_declaration(self) -> List[str]:
        ret = []
        for i in self.rust_vars.values():  
            if i.parent is not None and (i.parent.name == "input" or i.parent.name == "output"):
                continue
            ret.append(i.gen_struct_declaration())
        return ret
           
    def push_code(self, code: str):
        self.process_code.append(code)
    
    def pop_code(self) -> str:
        return self.process_code.pop()
    
    @property
    def def_code(self) -> List[str]:
        return self._def_code
    
    @def_code.setter
    def def_code(self, value: List[str]):
        self._def_code = value
        
    @property
    def init_code(self) -> List[str]:
        return self._init_code
    
    @init_code.setter
    def init_code(self, value: List[str]):
        self._init_code = value
    
    @property
    def process_code(self) -> List[str]:
        return self._process_code
    
    @process_code.setter
    def process_code(self, value: List[str]):
        self._process_code = value
        
    @property
    def tables(self) -> Dict[str, Table]:
        return self._tables
    
    @tables.setter
    def tables(self, value: Dict[str, Table]):
        self._tables = value
        
    @property
    def sql_vars(self) -> Dict[str, SQLVariable]:
        return self._sql_vars
    
    @sql_vars.setter
    def sql_vars(self, value: Dict[str, SQLVariable]):
        self._sql_vars = value
        
    @property
    def rust_vars(self) -> Dict[str, BackendVariable]:
        return self._rust_vars
    
    @rust_vars.setter
    def rust_vars(self, value: Dict[str, BackendVariable]):
        self._rust_vars = value