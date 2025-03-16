import unittest
from unittest.mock import Mock, patch
import sys
from contextlib import contextmanager

# 假设被测模块为 `launch`（需根据实际导入路径调整）
import launch

class TestLaunch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Mock 全局依赖（如 config 或其他模块）
        pass

    @patch('launch.mumu_info.get_mumu_window_position')
    @patch('launch.main.execute_process_que')
    @patch('launch.main.execute_process_ans')
    @patch('launch.keyboard.Key')
    def test_on_press_f10(self, mock_key, mock_execute_ans, mock_execute_que, mock_get_pos):
        """测试 F10 按键触发 execute_process_que"""
        # 安排 Mock
        mock_key.f10 = keyboard.Key.f10
        mock_get_pos.return_value = (0, 0, 100, 100, 'test_image_path')
        
        # 调用被测函数
        launch.on_press(mock_key.f10)
        
        # 验证
        mock_execute_que.assert_called_once_with(
            'test_image_path',
            launch.client,
            launch.endpoint_id,
            launch.QandA_path,
            0, 0
        )

    @patch('launch.mumu_info.get_mumu_window_position')
    @patch('launch.main.execute_process_ans')
    @patch('launch.keyboard.Key')
    def test_on_press_f11(self, mock_key, mock_execute_ans, mock_get_pos):
        """测试 F11 按键触发 execute_process_ans"""
        mock_key.f11 = keyboard.Key.f11
        mock_get_pos.return_value = (0, 0, 100, 100, 'test_image_path')
        
        launch.on_press(mock_key.f11)
        
        mock_execute_ans.assert_called_once_with(
            'test_image_path',
            launch.client,
            launch.endpoint_id,
            launch.QandA_path
        )

    @patch('launch.keyboard.Key')
    def test_on_press_f12(self, mock_key):
        """测试 F12 按键返回 False 停止监听器"""
        mock_key.f12 = keyboard.Key.f12
        
        result = launch.on_press(mock_key.f12)
        self.assertFalse(result)  # 应返回 False

    @patch('launch.keyboard.Key')
    def test_on_press_other_key(self, mock_key):
        """测试非 F10/F11/F12 按键不触发操作"""
        mock_key.esc = keyboard.Key.esc  # 模拟其他按键
        
        # 验证无异常
        launch.on_press(mock_key.esc)
        # 无断言，仅确保不抛出异常

    @patch('launch.keyboard.Listener')
    def test_start_listener(self, mock_listener):
        """测试 start_listener 正常启动监听器"""
        # Mock Listener 实例
        mock_listener.return_value = Mock()
        
        # 调用被测函数
        launch.start_listener()
        
        # 验证 Listener 被调用
        mock_listener.assert_called_once()
        mock_listener().join.assert_called_once()

    @patch('launch.keyboard.Listener')
    def test_start_listener_interrupt(self, mock_listener):
        """测试 KeyboardInterrupt 中断监听器"""
        # 模拟 join() 抛出 KeyboardInterrupt
        mock_listener.return_value = Mock()
        mock_listener().join.side_effect = KeyboardInterrupt
        
        # 调用被测函数
        with self.assertRaises(KeyboardInterrupt):
            launch.start_listener()
        
        mock_listener().stop.assert_called_once()

if __name__ == '__main__':
    unittest.main()
