import unittest

from system_monitor.system_info import format_bytes, get_system_info


class TestSystemInfo(unittest.TestCase):

    def test_format_bytes(self):
        self.assertEqual(format_bytes(1023), "1023 B")
        self.assertEqual(format_bytes(1024), "1.00 KB")
        self.assertEqual(format_bytes(1048576), "1.00 MB")
        self.assertEqual(format_bytes(1073741824), "1.00 GB")

    def test_get_system_info(self):
        cpu_usage, memory_usage, disk_usage, net_sent, net_recv = get_system_info()
        self.assertIsInstance(cpu_usage, float)
        self.assertIsInstance(memory_usage, float)
        self.assertIsInstance(disk_usage, float)
        self.assertIsInstance(net_sent, int)
        self.assertIsInstance(net_recv, int)


if __name__ == "__main__":
    unittest.main()
