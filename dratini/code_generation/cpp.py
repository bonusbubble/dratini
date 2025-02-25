import ast as _ast

from dratini.code_generation.code_generator import DratiniCompiler
from dratini.utils import load_text_file, print_dump


class CppCodeGenerator(DratiniCompiler):
    '''
    A code generator that outputs C++ source code.
    '''

    def __init__(self):
        super().__init__(
                target_format="cpp",
                statement_delimiter=";\n"
        )

    def generate_ann_assign(self, module: _ast.Module, ann_assign: _ast.AnnAssign) -> str:
        target = self.generate_name(module, ann_assign.target)
        value = self.generate_expression(module, ann_assign.value)
        annotation = self.generate_name(module, ann_assign.annotation)
        source_code = annotation + " " + target + " = " + value
        return source_code

    def generate_assign(self, module: _ast.Module, assign: _ast.Assign) -> str:
        value = self.generate_expression(module, assign.value)
        statement_source_codes = []
        i = 0
        for target_node in assign.targets:
            target = self.generate_name(module, target_node)
            statement_source_code = target + " = " + value
            statement_source_codes.append(statement_source_code)
            i += 1
        source_code = ";\n".join(statement_source_codes)
        return source_code

    def generate_bin_op(self, module: _ast.Module, bin_op: _ast.BinOp) -> str:
        left_expression = self.generate_expression(module, bin_op.left)
        right_expression = self.generate_expression(module, bin_op.right)
        operator_node = bin_op.op
        operator = None
        if isinstance(operator_node, _ast.Add):
            operator = "+"
        if isinstance(operator_node, _ast.Sub):
            operator = "-"
        if isinstance(operator_node, _ast.Mult):
            operator = "*"
        if isinstance(operator_node, _ast.Pow):
            operator = "**"
        if isinstance(operator_node, _ast.Div):
            operator = "/"
        if isinstance(operator_node, _ast.FloorDiv):
            operator = "//"
        if operator is None:
            self._throw_feature_not_supported("bin_op/operator", operator_node)
        if operator == "**":
            source_code = "pow(" + left_expression + ", " + right_expression + ")"
        elif operator == "//":
            source_code = "floor(" + left_expression + " / " + right_expression + ")"
        else:
            source_code = left_expression + " " + operator + " " + right_expression
        return source_code

    def generate_call(self, module: _ast.Module, call: _ast.Call) -> str:
        function_name = self.generate_name(module, call.func)
        function_call_args = self.generate_expressions(module, call.args)
        source_code = function_name + "(" + function_call_args + ")"
        return source_code

    def generate_constant(self, module: _ast.Module, constant: _ast.Constant) -> str:
        constant_value = constant.value
        if isinstance(constant_value, bool):
            return str(constant_value).lower()
        if isinstance(constant_value, float):
            return str(constant_value)
        if isinstance(constant_value, int):
            return str(constant_value)
        if isinstance(constant_value, str):
            return "\"" + str(constant_value) + "\""
        self._throw_feature_not_supported("constant", constant)

    def generate_expression(self, module: _ast.Module, expression: _ast.Expr) -> str:
        if isinstance(expression, _ast.BinOp):
            return self.generate_bin_op(module, expression)
        if isinstance(expression, _ast.Call):
            return self.generate_call(module, expression)
        if isinstance(expression, _ast.Constant):
            return self.generate_constant(module, expression)
        if isinstance(expression, _ast.Name):
            return self.generate_name(module, expression)
        self._throw_feature_not_supported("expression", expression)

    def generate_expressions(self, module: _ast.Module, expressions: list[_ast.Expr]) -> str:
        expression_source_codes = []
        for expression in expressions:
            expression_source_code = self.generate_expression(module, expression)
            expression_source_codes.append(expression_source_code)
        source_code = ", ".join(expression_source_codes)
        return source_code

    def generate_name(self, module: _ast.Module, name: _ast.Name) -> str:
        if isinstance(name, _ast.Name):
            return name.id
        self._throw_feature_not_supported("name", name)

    def generate_statement(self, module: _ast.Module, statement: _ast.stmt) -> str:
        source_code = None
        if isinstance(statement, _ast.AnnAssign):
            source_code = self.generate_ann_assign(module, statement)
        if isinstance(statement, _ast.Assign):
            source_code = self.generate_assign(module, statement)
        if isinstance(statement, _ast.Expr):
            expression = statement.value
            source_code = self.generate_expression(module, expression)
        if source_code is None:
            self._throw_feature_not_supported("statement", statement)
        return source_code


def generate_cpp(module: _ast.Module) -> str:
    '''
    Generate C++ source code from a Python module.
    '''
    # Create the code generator.
    code_generator: DratiniCompiler = CppCodeGenerator()
    # Generate the source code.
    source_code = code_generator.generate_module(module)
    # Return the source code.
    return source_code
