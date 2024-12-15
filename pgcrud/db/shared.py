from psycopg.rows import BaseRowFactory, scalar_row, tuple_row, dict_row, class_row, args_row, kwargs_row

from pgcrud.config import ConfigDict, config
from pgcrud.optional_dependencies import is_pydantic_installed, is_pydantic_model, is_msgspec_installed, is_msgspec_model, msgspec_kwargs_fun_generator, pydantic_kwargs_fun_generator, pydantic_args_fun_generator, msgspec_args_fun_generator, pydantic_scalar_row_generator, msgspec_scalar_row_generator
from pgcrud.types import T, ValidationType


__all__ = [
    'get_params',
    'get_row_factory',
]


warning_message = 'Validation is not performed because no validation library is configured. This may lead to unexpected behavior.'


def get_params(item: type[T] | tuple[type[T], ConfigDict]) -> tuple[type[T], ValidationType, bool]:

    if isinstance(item, tuple):
        row_type = item[0]
        config_dict = item[1]
    else:
        row_type = item
        config_dict: ConfigDict = {}

    validate = config_dict.get('validation_library') or config.validation_library
    strict = config_dict.get('strict_validation') or config.strict_validation

    return row_type, validate, strict


def get_row_factory(row_type: type[T], validate: ValidationType, strict: bool) -> BaseRowFactory[T]:

    if is_msgspec_installed and is_msgspec_model(row_type):
        if validate == 'pydantic':
            return kwargs_row(pydantic_kwargs_fun_generator(row_type, strict))
        elif validate == 'msgspec':
            return kwargs_row(msgspec_kwargs_fun_generator(row_type, strict))
        else:
            return class_row(row_type)

    elif is_pydantic_installed and is_pydantic_model(row_type):
        if validate == 'pydantic':
            return class_row(row_type)
        elif validate == 'msgspec':
            return kwargs_row(msgspec_kwargs_fun_generator(row_type, strict))
        else:
            ## always validates because it is the only way to construct the model recursively
            return class_row(row_type) # type: ignore

    elif issubclass(getattr(row_type, '__origin__', row_type), dict):
        if validate == 'pydantic':
            return kwargs_row(pydantic_kwargs_fun_generator(row_type, strict))
        elif validate == 'msgspec':
            return kwargs_row(msgspec_kwargs_fun_generator(row_type, strict))
        else:
            return dict_row  # type: ignore

    elif issubclass(getattr(row_type, '__origin__', row_type), (tuple, list, set)):
        if validate == 'pydantic':
            return args_row(pydantic_args_fun_generator(row_type, strict))
        elif validate == 'msgspec':
            return args_row(msgspec_args_fun_generator(row_type, strict))
        else:
            return tuple_row  # type: ignore

    else:
        if validate == 'pydantic':
            return pydantic_scalar_row_generator(row_type, strict)
        elif validate == 'msgspec':
            return msgspec_scalar_row_generator(row_type, strict)
        else:
            return scalar_row
