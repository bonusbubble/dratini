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

    def __init__(self, target_format: str, statement_delimiter: str = "\n"):
        self.statement_delimiter = "\n"
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

    def generate_bin_op(self, module: _ast.Module, bin_op: _ast.BinOp) -> str:
        self._throw_feature_not_supported("bin_op", module)
        return ""

    def generate_call(self, module: _ast.Module, call: _ast.Call) -> str:
        self._throw_feature_not_supported("call", module)
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
        source_code = self.load_header_file()
        statement_delimiter = self.statement_delimiter
        for statement in module.body:
            print(type(statement))
            statement_source_code = self.generate_statement(module, statement) + statement_delimiter
            if isinstance(statement_source_code, str) and len(statement_source_code) > 0:
                source_code += statement_source_code
        source_code += self.load_footer_file()
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

    def _throw_feature_not_supported(self, category: str, feature: object):
        namespace = "generator/" + self.target_format
        throw_feature_not_supported(feature, namespace=namespace, category=category)
