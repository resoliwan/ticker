import inspect

from ticker import config
from ticker.adapters import orm
from ticker.adapters.vendor_proxy import (  # HttpVendorProxy,
    AbstractVendorProxy,
    MockVendorProxy,
    YFianceProxy,
)
from ticker.service_layer import handlers, messagebus, unit_of_work


def bootstrap(
    start_orm: bool = True,
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
    vendor_proxy: AbstractVendorProxy = YFianceProxy(),
) -> messagebus.MessageBus:

    config.print_all_envs()
    # if notifications is None:
    # notifications = EmailNotifications()

    if start_orm:
        orm.start_mappers()

    if config.use_mock_vendor_proxy():
        vendor_proxy = MockVendorProxy()

    dependencies = {
        "uow": uow,
        "vendor_proxy": vendor_proxy,
    }
    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies) for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return (
        messagebus.MessageBus(
            uow=uow,
            event_handlers=injected_event_handlers,
            command_handlers=injected_command_handlers,
        ),
        dependencies,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    # pylint: disable=unnecessary-lambda
    return lambda message: handler(message, **deps)
