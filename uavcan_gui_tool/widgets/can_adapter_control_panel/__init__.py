#
# Copyright (C) 2016  UAVCAN Development Team  <uavcan.org>
#
# This software is distributed under the terms of the MIT License.
#
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

from PyQt5.QtWidgets import QProgressDialog, QMessageBox
from . import slcan_cli


def spawn_window(parent, node, iface_name):
    driver = node.can_driver

    if not slcan_cli.CLIInterface.is_backend_supported(driver):
        mbox = QMessageBox(parent)
        mbox.setWindowTitle('Unsupported CAN Backend')
        mbox.setText('현재 CAN 백엔드와 CAN Adapter Control Panel을 사용할 수 없습니다.')
        mbox.setInformativeText('The current backend is %r.' % type(driver).__name__)
        mbox.setIcon(QMessageBox.Information)
        mbox.setStandardButtons(QMessageBox.Ok)
        mbox.show()     # Not exec() because we don't want it to block!
        return

    progress_dialog = QProgressDialog(parent)
    progress_dialog.setWindowTitle('CAN Adapter Control Panel 초기화')
    progress_dialog.setLabelText('CAN 아답터 탐색 중...')
    progress_dialog.setMinimumDuration(800)
    progress_dialog.setCancelButton(None)
    progress_dialog.setRange(0, 0)
    progress_dialog.show()

    def supported_callback(supported):
        progress_dialog.close()

        if not supported:
            mbox = QMessageBox(parent)
            mbox.setWindowTitle('호환되지 않는 CAN Adapter')
            mbox.setText('연결된 아답터와 CAN Adapter Control Panel을 사용할 수 없습니다.')
            mbox.setInformativeText('연결된 SLCAN adapter는 CLI를 지원하지 않습니다.')
            mbox.setIcon(QMessageBox.Information)
            mbox.setStandardButtons(QMessageBox.Ok)
            mbox.show()     # Not exec() because we don't want it to block!
            return

        slcp = slcan_cli.ControlPanelWindow(parent, slcan_iface, iface_name)
        slcp.show()

    slcan_iface = slcan_cli.CLIInterface(driver)
    slcan_iface.check_is_interface_supported(supported_callback)
