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
                statement_delimiter=";",
                statement_prefix="    ",
                one_statement_per_line=True
        )

    def decorate_function_body(self, module: _ast.Module, source_code: str) -> str:
        header = "{" + self.line_delimiter
        footer = "}"
        return header + source_code + footer

    def decorate_module_body(self, module: _ast.Module, source_code: str) -> str:
        header = "int main() {" + self.line_delimiter
        header += self.decorate_statement("bgcx_start();")
        footer = self.decorate_statement("bgcx_stop();")
        footer += "}"
        return header + source_code + footer

    def decorate_statement(self, source_code: str) -> str:
        source_code = self.statement_prefix + source_code + self.statement_suffix
        if self.one_statement_per_line:
            source_code += self.line_delimiter
        return source_code

    def generate_ann_assign(self, module: _ast.Module, ann_assign: _ast.AnnAssign) -> str:
        target = self.generate_name(module, ann_assign.target)
        value = self.generate_expression(module, ann_assign.value)
        annotation = self.generate_name(module, ann_assign.annotation)
        source_code = annotation + " " + target + " = " + value
        return source_code

    def generate_arg(self, module: _ast.Module, arg: _ast.arg) -> str:
        arg_source_code = ""
        name = arg.arg
        type_name = self.generate_name(module, arg.annotation)
        if type_name and name:
            return type_name + " " + name;
        if name:
            return "any " + name;
        if type_name:
            return type_name + " " + self.random_name()
        return source_code

    def generate_args(self, module: _ast.Module, args: list[_ast.arg]) -> str:
        args_source_code = []
        for arg in args:
            arg_source_code = self.generate_arg(module, arg)
            args_source_code.append(arg_source_code)
        source_code = self.arg_delimiter.join(args_source_code)
        return source_code

    def generate_arguments(self, module: _ast.Module, args: _ast.arguments) -> str:
        # posonlyargs = args.posonlyargs
        # kwonlyargs = args.kwonlyargs
        # kw_defaults = args.kw_defaults
        # defaults = args.defaults
        args = self.generate_args(module, args.args)
        source_code = self.arg_delimiter.join([args])
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
            source_code = "pow(" + left_expression + self.arg_delimiter + right_expression + ")"
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

    def generate_class_decl(self, module: _ast.Module, class_def: _ast.ClassDef) -> str:
        return ""

    def generate_class_def(self, module: _ast.Module, class_def: _ast.ClassDef) -> str:
        self._throw_feature_not_supported("class_def", module)
        return ""

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
        if isinstance(expression, _ast.UnaryOp):
            return self.generate_unary_op(module, expression)
        self._throw_feature_not_supported("expression", expression)

    def generate_expressions(self, module: _ast.Module, expressions: list[_ast.Expr]) -> str:
        expression_source_codes = []
        for expression in expressions:
            expression_source_code = self.generate_expression(module, expression)
            expression_source_codes.append(expression_source_code)
        source_code = self.arg_delimiter.join(expression_source_codes)
        return source_code

    def generate_function_def(self, module: _ast.Module, function_def: _ast.FunctionDef) -> str:
        body = function_def.body
        # print_dump(function_def)
        # exit()
        decl_source_code = self._generate_function_decl(module, function_def)
        body_source_code = self.generate_function_body(module, body)
        source_code = decl_source_code + body_source_code
        self.function_defs.append(source_code)
        return self.generate_noop()

    def generate_noop(self) -> str:
        return "((void) 0)"

    def _generate_function_decl(self, module: _ast.Module, function_def: _ast.FunctionDef) -> str:
        name = self.generate_name(module, function_def.name)
        args = function_def.args
        decorators = function_def.decorator_list
        return_type = (function_def.returns and function_def.returns.id) or "void"
        # print_dump(function_def)
        # exit()
        source_code = return_type + " " + name + "(" + self.generate_arguments(module, args) + ")"
        self.function_decls.append(source_code)
        return source_code

    def generate_statement(self, module: _ast.Module, statement: _ast.stmt) -> str:
        source_code = ""
        if isinstance(statement, _ast.AnnAssign):
            source_code += self.generate_ann_assign(module, statement)
        if isinstance(statement, _ast.Assign):
            source_code += self.generate_assign(module, statement)
        if isinstance(statement, _ast.Expr):
            expression = statement.value
            source_code += self.generate_expression(module, expression)
        if isinstance(statement, _ast.FunctionDef):
            source_code += self.generate_function_def(module, statement)
        if isinstance(statement, _ast.While):
            test_source_code = self.generate_expression(module, statement.test)
            body_source_code = self.generate_function_body(module, statement.body)
            source_code += "while (" + test_source_code + ") " + body_source_code
        if source_code is None or len(source_code) < 1:
            self._throw_feature_not_supported("statement", statement)
        return source_code

    def generate_unary_op(self, module: _ast.Module, unary_op: _ast.UnaryOp) -> str:
        operand_expression = self.generate_expression(module, unary_op.operand)
        operator_node = unary_op.op
        operator = None
        if isinstance(operator_node, _ast.Not):
            operator = "!"
        if operator is None:
            self._throw_feature_not_supported("unary_op/operator", operator_node)
        if operator == "!":
            source_code = "(!(" + operand_expression + "))"
        else:
            source_code = operand_expression + " " + operator + " " + right_expression
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
