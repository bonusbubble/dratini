import ast as _ast
from types import CodeType

from dratini.utils import load_text_file, throw_feature_not_supported


class DratiniCompiler:
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

    def __init__(self, line_delimiter: str = "\n", one_statement_per_line: bool = True, statement_delimiter: str = "\n", statement_prefix: str = "", statement_suffix: str = "", target_format: str = "dra"):
        self.line_delimiter = line_delimiter
        self.one_statement_per_line = one_statement_per_line
        self.statement_delimiter = statement_delimiter
        self.statement_prefix = statement_prefix
        self.statement_suffix = statement_suffix
        self.target_format = target_format

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

    def generate_expression(self, module: _ast.Module, expression: _ast.Expr) -> str:
        self._throw_feature_not_supported("expression", module)
        return ""

    def generate_expressions(self, module: _ast.Module, expressions: list[_ast.Expr]) -> str:
        self._throw_feature_not_supported("expressions", module)
        return ""

    def generate_module(self, module: _ast.Module) -> str:
        line_delimiter = self.line_delimiter
        source_code = self.load_header_file() + line_delimiter
        source_code += self.generate_module_body(module) + line_delimiter
        source_code += self.load_footer_file() + line_delimiter
        return source_code

    def generate_module_body(self, module: _ast.Module) -> str:
        source_code = self.generate_module_body_inner(module)
        source_code = self.wrap_module_body(module, source_code)
        return source_code

    def generate_module_body_inner(self, module: _ast.Module) -> str:
        source_code = ""
        statement_delimiter = self.statement_delimiter
        if self.one_statement_per_line:
            statement_delimiter += self.line_delimiter
        statement_prefix = self.statement_prefix
        statement_suffix = self.statement_suffix
        for statement in module.body:
            statement_source_code = statement_prefix + self.generate_statement(module, statement) + statement_suffix + statement_delimiter
            if isinstance(statement_source_code, str) and len(statement_source_code) > 0:
                source_code += statement_source_code
        return source_code

    def generate_name(self, module: _ast.Module, name: _ast.Name) -> str:
        self._throw_feature_not_supported("name", module)
        return ""

    def generate_statement(self, module: _ast.Module, statement: _ast.stmt) -> str:
        source_code = _ast.unparse(statement)
        return ""

    def load_component(self, component_name: str) -> str:
        target_format: str = self.target_format
        component_file_name: str = component_name + "." + target_format
        component_file_path: str = "./dratini/code_generation/components/" + target_format + "/" + component_file_name
        return load_text_file(component_file_path)

    def load_footer_file(self) -> str:
        return self.load_component("footer")

    def load_header_file(self) -> str:
        return self.load_component("header")

    def wrap_module_body(self, module: _ast.Module, source_code: str) -> str:
        return source_code

    def _throw_feature_not_supported(self, category: str, feature: object):
        namespace = "generator/" + self.target_format
        throw_feature_not_supported(feature, namespace=namespace, category=category)
