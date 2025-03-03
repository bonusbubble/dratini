import ast as _ast
from random import randint
from types import CodeType
import os

from dratini.utils import load_text_file, throw_feature_not_supported


# dirname__ will be the absolute directory that current .py file is in
__dirname__ = os.path.dirname(os.path.abspath(__file__))


class DratiniCompiler:
    @property
    def decls(self) -> list[str]:
        return [*(self.function_decls)]

    @property
    def defs(self) -> list[str]:
        return [*(self.function_defs)]

    @property
    def function_decls(self) -> list[str]:
        return self._function_decls

    @property
    def function_defs(self) -> list[str]:
        return self._function_defs

    @property
    def scope_level(self) -> int:
        return self._scope_level

    @property
    def scopes(self) -> int:
        return self._scopes

    @property
    def target_format(self) -> str:
        return self._target_format

    @target_format.setter
    def target_format(self, value: str):
        self._target_format = str(value)

    def __init__(self, arg_delimiter: str=", ", ignore_noop: bool=True, line_delimiter: str="\n", one_statement_per_line: bool=True, statement_delimiter: str="\n", statement_prefix: str="", statement_suffix: str="", target_format: str="dra"):
        # Define public attributes.
        self.arg_delimiter = arg_delimiter
        self.ignore_noop = ignore_noop
        self.line_delimiter = line_delimiter
        self.one_statement_per_line = one_statement_per_line
        self.statement_delimiter = statement_delimiter
        self.statement_prefix = statement_prefix
        self.statement_suffix = statement_suffix
        self.target_format = target_format
        # Define private attributes.
        self._function_decls = []
        self._function_defs = []

    def link(self, target_source_code: str) -> bytes:
        # Generate source code in the target language.
        target_source_code = self.compile(target_source_code)
        # Link the generated target source code.
        return bytes()

    def compile(self, source_code: str) -> str:
        # Parse the Dratini source code.
        module = self.parse(source_code)
        # Generate source code in the target language.
        target_source_code = self.generate_module(module)
        # Return the generated target source code.
        return target_source_code

    def translate(self, source_code: str) -> str:
        # Parse the Dratini source code.
        module = self.parse(source_code)
        # Generate source code in the target language.
        target_source_code = self.generate_module(module)
        # Return the generated target source code.
        return target_source_code

    def parse(self, source_code: str) -> _ast.AST:
        # Parse the Dratini source code.
        module = _ast.parse(source_code)
        # Return the module.
        return module

    def generate_ann_assign(self, module: _ast.Module, ann_assign: _ast.AnnAssign) -> str:
        self._throw_feature_not_supported("ann_assign", module)
        return ""

    def generate_arguments(self, module: _ast.Module, args: _ast.arguments) -> str:
        self._throw_feature_not_supported("args", module)
        return ""

    def generate_assign(self, module: _ast.Module, ann_assign: _ast.AnnAssign) -> str:
        self._throw_feature_not_supported("assign", module)
        return ""

    def generate_bin_op(self, module: _ast.Module, bin_op: _ast.BinOp) -> str:
        self._throw_feature_not_supported("bin_op", module)
        return ""

    def generate_call(self, module: _ast.Module, call: _ast.Call) -> str:
        self._throw_feature_not_supported("call", module)
        return ""

    def generate_class_def(self, module: _ast.Module, class_def: _ast.ClassDef) -> str:
        self._throw_feature_not_supported("class_def", module)
        return ""

    def generate_constant(self, module: _ast.Module, constant: _ast.Constant) -> str:
        self._throw_feature_not_supported("constant", module)
        return ""

    def generate_decls(self) -> str:
        if len(self.function_decls) < 1:
            return ""
        delimiter = self.line_delimiter + self.statement_delimiter
        return delimiter.join(self.function_decls)

    def generate_defs(self) -> str:
        if len(self.function_defs) < 1:
            return ""
        return self.line_delimiter.join(self.function_defs)

    def generate_expression(self, module: _ast.Module, expression: _ast.Expr) -> str:
        self._throw_feature_not_supported("expression", module)
        return ""

    def generate_expressions(self, module: _ast.Module, expressions: list[_ast.Expr]) -> str:
        self._throw_feature_not_supported("expressions", module)
        return ""

    def generate_function_body(self, module: _ast.Module, body: list[_ast.stmt]):
        source_code = ""
        statement_delimiter = self.statement_delimiter
        if self.one_statement_per_line:
            statement_delimiter += self.line_delimiter
        statement_prefix = self.statement_prefix
        statement_suffix = self.statement_suffix
        for statement in body:
            statement_source_code = self.generate_statement(module, statement)
            if isinstance(statement_source_code, str) and len(statement_source_code) > 0:
                if not self.ignore_noop or statement_source_code != self.generate_noop():
                    source_code += statement_prefix + statement_source_code + statement_suffix + statement_delimiter
        source_code = self.decorate_function_body(module, source_code)
        return source_code

    def generate_module(self, module: _ast.Module) -> str:
        line_delimiter = self.line_delimiter
        source_code = self.load_header_file() + line_delimiter
        source_code += self.generate_module_body(module) + line_delimiter
        source_code += self.load_footer_file() + line_delimiter
        return source_code

    def generate_module_body(self, module: _ast.Module) -> str:
        source_code = self.generate_function_body(module, module.body)
        source_code = self.decorate_module_body(module, source_code)
        decl_source_code = self.generate_decls() + self.statement_delimiter + self.line_delimiter
        defs_source_code = self.line_delimiter + self.generate_defs()
        source_code = decl_source_code + source_code + defs_source_code
        return source_code

    def generate_name(self, module: _ast.Module, name: _ast.Name) -> str:
        if isinstance(name, _ast.Name):
            name = name.id
        if type(name) is str:
            if name.startswith("__"):
                return name
            if name.startswith("_"):
                return self.obfuscate_name(module, name)
            return name
        self._throw_feature_not_supported("name", name)

    def generate_noop(self) -> str:
        self._throw_feature_not_supported("noop", module)
        return ""

    def generate_statement(self, module: _ast.Module, statement: _ast.stmt) -> str:
        source_code = _ast.unparse(statement)
        return ""

    def load_component(self, component_name: str) -> str:
        target_format: str = self.target_format
        component_file_name: str = component_name + "." + target_format
        component_file_path: str = os.path.join(__dirname__, "components", target_format, component_file_name)
        return load_text_file(component_file_path)

    def load_footer_file(self) -> str:
        return self.load_component("footer")

    def load_header_file(self) -> str:
        return self.load_component("header")

    def decorate_function_body(self, module: _ast.Module, source_code: str) -> str:
        return source_code

    def decorate_module_body(self, module: _ast.Module, source_code: str) -> str:
        return source_code

    def module_key(self, module: _ast.Module) -> int:
        return hash(str(module))

    def hash_name(self, module: _ast.Module, name: str) -> str:
        hash_code = 11
        hash_code *= self.module_key(module)
        hash_code *= 13
        hash_code *= hash(name)
        return hash_code

    def obfuscate_name(self, module: _ast.Module, name: str) -> str:
        hash_code = self.hash_name(module, name)
        obfuscation_id = abs(hash_code)
        obfuscated_name = "_" + str(obfuscation_id)
        obfuscated_name = obfuscated_name[:12]
        return obfuscated_name

    def random_id(self) -> int:
        return round(abs(randint(0x00000000, 0xFFFFFFFF)))

    def random_name(self) -> str:
        return "_" + str(self.random_id())

    def _throw_feature_not_supported(self, category: str, feature: object):
        namespace = "generator/" + self.target_format
        throw_feature_not_supported(feature, namespace=namespace, category=category)
