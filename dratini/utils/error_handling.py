from .hex2 import *


def throw_feature_not_supported(
        feature: object,
        namespace: str = None,
        category: str = None
):
    error_message = "Feature not yet supported: "
    if namespace is not None:
        namespace = str(namespace)
        error_message += namespace + "/"
    if category is not None:
        category = str(category)
        error_message += category + "/"
    error_message += feature.__class__.__name__
    abort(
            code = 0x111E_ED42,
            message = error_message
    )
