from typing import Union


def model_save(
    auto_call_save: bool = True,
    update_fields: Union[str, list, tuple] = None,
    pass_through_save: bool = False,
):
    """Method decorator for Django models to facilitate calling save after the method was executed
    or skip the save in by passing the kwarg `save=False`.

    Please note: the kwarg `save` will, by default, be exclusively used within this decorator and
    popped from the given kwargs of the function call. If you want to use save within the wrapped
    method you need to set `pass_through_save=True` to this decorator.
    """

    def wrapper(f):
        def wrapper2(*args, save=True, **kwargs):
            if pass_through_save:
                kwargs["save"] = save
            _return = f(*args, **kwargs)
            if save or (auto_call_save and save is None):
                args[0].save(update_fields=update_fields)
            return _return

        return wrapper2

    return wrapper