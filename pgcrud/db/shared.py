import warnings

from psycopg.rows import BaseRowFactory, scalar_row, tuple_row, dict_row, class_row, args_row, kwargs_row

from pgcrud.config import config
from pgcrud.optional_dependencies import is_pydantic_installed, is_pydantic_model, is_msgspec_installed, is_msgspec_model, msgspec_kwargs_fun_generator, pydantic_kwargs_fun_generator, pydantic_args_fun_generator, msgspec_args_fun_generator, pydantic_scalar_row_generator, msgspec_scalar_row_generator
from pgcrud.types import T


__all__ = [
    'get_params',
    'get_row_factory',
]


warning_message = 'Validation is not performed because no validation library is configured. This may lead to unexpected behavior.'


def get_params(item: type[T] | tuple[type[T]] | tuple[type[T], bool] | tuple[type[T], bool, bool]) -> tuple[type[T], bool, bool]:

    if not isinstance(item, tuple):
        item = (item, config.validation_default, config.strict_default)
    elif len(item) == 1:
        item += (config.validation_default, config.strict_default)
    elif len(item) == 2:
        item += (config.strict_default,)

    row_type, validate, strict = item
    row_type: type[T]  # Pyright is not correctly inferring the type

    return row_type, validate, strict


def get_row_factory(row_type: type[T], validate: bool, strict: bool) -> BaseRowFactory[T]:

    if is_msgspec_installed and is_msgspec_model(row_type):
        if validate:
            if config.validation_library == 'pydantic':
                return kwargs_row(pydantic_kwargs_fun_generator(row_type, strict))
            elif config.validation_library == 'msgspec':
                return kwargs_row(msgspec_kwargs_fun_generator(row_type, strict))
            else:
                warnings.warn(warning_message)
                return class_row(row_type)
        else:
            return class_row(row_type)

    elif is_pydantic_installed and is_pydantic_model(row_type):
        if validate:
            if config.validation_library == 'pydantic':
                return class_row(row_type)
            elif config.validation_library == 'msgspec':
                return kwargs_row(msgspec_kwargs_fun_generator(row_type, strict))
            else:
                warnings.warn(warning_message)
                return class_row(row_type) # TODO: needs to be implemented
        else:
            return kwargs_row(row_type.model_construct)  # type: ignore

    elif issubclass(getattr(row_type, '__origin__', row_type), dict):
        if validate:
            if config.validation_library == 'pydantic':
                return kwargs_row(pydantic_kwargs_fun_generator(row_type, strict))
            elif config.validation_library == 'msgspec':
                return kwargs_row(msgspec_kwargs_fun_generator(row_type, strict))
            else:
                warnings.warn(warning_message)
                return dict_row  # type: ignore
        else:
            return dict_row  # type: ignore

    elif issubclass(getattr(row_type, '__origin__', row_type), (tuple, list, set)):
        if validate:
            if config.validation_library == 'pydantic':
                return args_row(pydantic_args_fun_generator(row_type, strict))
            elif config.validation_library == 'msgspec':
                return args_row(msgspec_args_fun_generator(row_type, strict))
            else:
                warnings.warn(warning_message)
                return tuple_row  # type: ignore
        else:
            return tuple_row  # type: ignore

    else:
        if validate:
            if config.validation_library == 'pydantic':
                return pydantic_scalar_row_generator(row_type, strict)
            elif config.validation_library == 'msgspec':
                return msgspec_scalar_row_generator(row_type, strict)
            else:
                warnings.warn(warning_message)
                return scalar_row
        else:
            return scalar_row
