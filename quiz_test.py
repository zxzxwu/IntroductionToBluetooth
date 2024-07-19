import asyncio
import unittest
import rootcanal.binaries

import bumble.device
import bumble.transport


class QuizTest(unittest.IsolatedAsyncioTestCase):
    devices: list[bumble.device.Device] = []
    rootcanal_process: asyncio.subprocess.Process

    async def asyncSetUp(self) -> None:
        self.rootcanal_process = await asyncio.create_subprocess_shell(
            rootcanal.binaries.get_package_binary_resource_path("rootcanal")
        )

        for _ in range(2):
            transport = await bumble.transport.open_transport(
                "tcp-client:127.0.0.1:6402"
            )
            device = bumble.device.Device.from_config_with_hci(
                bumble.device.DeviceConfiguration(classic_enabled=True),
                hci_sink=transport.sink,
                hci_source=transport.source,
            )
            await device.power_on()
            self.devices.append(device)

    async def asyncTearDown(self) -> None:
        self.rootcanal_process.kill()

    async def test_send_command(self) -> None:
        pass
