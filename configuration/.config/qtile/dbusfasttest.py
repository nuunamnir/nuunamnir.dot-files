
import asyncio
from asyncio import timeout as asyncio_timeout

from dbus_fast import BusType, unpack_variants
from dbus_fast.message import Message
from dbus_fast.aio import MessageBus

async def get_dbus_managed_objects():
    bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
    msg = Message(
        destination="org.bluez",
        path="/",
        interface="org.freedesktop.DBus.ObjectManager",
        member="GetManagedObjects",
    )

    async with asyncio_timeout(1):
        reply = await bus.call(msg)
        mngd_objs = {path: unpack_variants(packed_data) for path, packed_data in reply.body[0].items()}
        for obj_path, obj_data in mngd_objs.items():
            status = obj_data.get('org.bluez.Device1', {}).get('Connected')
            print(status)

    bus.disconnect()

if __name__ == '__main__':
    asyncio.run(get_dbus_managed_objects())

'''
nc def _get_dbus_managed_objects() -> dict[str, Any]:
    try:
        bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
    except FileNotFoundError as ex:
        if is_docker_env():
            _LOGGER.debug(
                "DBus service not found; docker config may "
                "be missing `-v /run/dbus:/run/dbus:ro`: %s",
                ex,
            )
        _LOGGER.debug(
            "DBus service not found; make sure the DBus socket " "is available: %s",
            ex,
        )
        return {}
    except BrokenPipeError as ex:
        if is_docker_env():
            _LOGGER.debug(
                "DBus connection broken: %s; try restarting "
                "`bluetooth`, `dbus`, and finally the docker container",
                ex,
            )
        _LOGGER.debug(
            "DBus connection broken: %s; try restarting " "`bluetooth` and `dbus`", ex
        )
        return {}
    except ConnectionRefusedError as ex:
        if is_docker_env():
            _LOGGER.debug(
                "DBus connection refused: %s; try restarting "
                "`bluetooth`, `dbus`, and finally the docker container",
                ex,
            )
        _LOGGER.debug(
            "DBus connection refused: %s; try restarting " "`bluetooth` and `dbus`", ex
        )
        return {}
    msg = Message(
        destination="org.bluez",
        path="/",
        interface="org.freedesktop.DBus.ObjectManager",
        member="GetManagedObjects",
    )
    try:
        async with asyncio_timeout(REPLY_TIMEOUT):
            reply = await bus.call(msg)
    except EOFError as ex:
        _LOGGER.debug("DBus connection closed: %s", ex)
        return {}
    except asyncio.TimeoutError:
        _LOGGER.debug(
            "Dbus timeout waiting for reply to GetManagedObjects; try restarting "
            "`bluetooth` and `dbus`"
        )
        return {}
    bus.disconnect()
    if not reply or reply.message_type != MessageType.METHOD_RETURN:
        _LOGGER.debug(
            "Received an unexpected reply from Dbus while "
            "calling GetManagedObjects on org.bluez: %s",
            reply,
        )
        return {}
    results: dict[str, Any] = reply.body[0]
    return results
    '''