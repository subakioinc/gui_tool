#
# Copyright (C) 2016  UAVCAN Development Team  <uavcan.org>
#
# This software is distributed under the terms of the MIT License.
#
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import sys
import logging
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QCheckBox
from PyQt5.QtCore import QTimer, Qt

logger = logging.getLogger(__name__)

try:
    # noinspection PyUnresolvedReferences
    from qtconsole.rich_jupyter_widget import RichJupyterWidget
    # noinspection PyUnresolvedReferences
    from qtconsole.inprocess import QtInProcessKernelManager

    JUPYTER_AVAILABLE = True
except ImportError:
    JUPYTER_AVAILABLE = False
    logger.info('Jupyter is not available', exc_info=True)


if JUPYTER_AVAILABLE:
    class JupyterWidget(RichJupyterWidget):
        def __init__(self, parent, kernel_manager, banner=None):
            super(JupyterWidget, self).__init__(parent)

            self.kernel_manager = kernel_manager

            self.kernel_client = kernel_manager.client()
            self.kernel_client.start_channels()

            self.exit_requested.connect(self._do_stop)

            if banner:
                self.banner = banner.strip() + '\n\n'

            try:
                # noinspection PyUnresolvedReferences
                import matplotlib
            except ImportError:
                pass
            else:
                self._execute('%matplotlib inline', True)

        def write(self, text):
            self._append_plain_text(text, True)

        def flush(self):
            pass

        def _do_stop(self):
            self.kernel_client.stop_channels()


def _make_jupyter_log_handler(target_widget):
    def filter_record(record):
        name = record.name.lower()
        skip = ['ipy', 'jupyter', 'qtconsole']
        for s in skip:
            if s in name:
                return False
        return True

    handler = logging.StreamHandler(target_widget)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    handler.setFormatter(formatter)
    handler.addFilter(filter_record)
    return handler


class JupyterConsoleWindow(QDialog):
    def __init__(self, parent, kernel_manager, banner=None):
        super(JupyterConsoleWindow, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle('Jupyter 콘솔')

        self._jupyter_widget = JupyterWidget(self, kernel_manager, banner)

        self.on_close = lambda *_: None

        self._log_handler = _make_jupyter_log_handler(self._jupyter_widget)
        logging.root.addHandler(self._log_handler)

        self._log_level_selector = QComboBox(self)
        self._log_level_selector.setToolTip('Log entries of this severity and higher will appear in the console')
        self._log_level_selector.setEditable(False)
        self._log_level_selector.addItems(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
        self._log_level_selector.currentTextChanged.connect(
            lambda: self._log_handler.setLevel(self._log_level_selector.currentText()))
        self._log_level_selector.setCurrentIndex(1)

        self._style_selector = QComboBox(self)
        self._style_selector.setToolTip('Select standard color theme')
        self._style_selector.setEditable(False)
        self._style_selector.addItems(['lightbg', 'linux'])
        self._style_selector.currentTextChanged.connect(
            lambda: self._jupyter_widget.set_default_style(self._style_selector.currentText()))
        self._style_selector.setCurrentIndex(0)

        self._redirect_stdout_checkbox = QCheckBox('표준출력 리다이렉트', self)
        self._redirect_stdout_checkbox.setToolTip('콘솔에서 표준 출력 보여주기')
        self._redirect_stdout_checkbox.stateChanged.connect(self._update_stdout_redirection)
        self._redirect_stdout_checkbox.setChecked(True)

        layout = QVBoxLayout(self)
        controls_layout = QHBoxLayout(self)
        controls_layout.addWidget(QLabel('Log 레벨:', self))
        controls_layout.addWidget(self._log_level_selector)
        controls_layout.addWidget(QLabel('테마 색상:', self))
        controls_layout.addWidget(self._style_selector)
        controls_layout.addWidget(self._redirect_stdout_checkbox)
        controls_layout.addStretch(1)

        layout.addLayout(controls_layout)
        layout.addWidget(self._jupyter_widget)
        self.setLayout(layout)
        self.resize(1000, 600)

    def __del__(self):
        self._finalize()

    def _update_stdout_redirection(self):
        if self._redirect_stdout_checkbox.isChecked():
            sys.stdout = self._jupyter_widget
        else:
            sys.stdout = sys.__stdout__

    def closeEvent(self, qcloseevent):
        self._finalize()
        super(JupyterConsoleWindow, self).closeEvent(qcloseevent)
        self.on_close()

    def _finalize(self):
        sys.stdout = sys.__stdout__
        logging.root.removeHandler(self._log_handler)
        self._log_handler.close()
        logger.info('Jupyter window finalized successfully')


class InternalObjectDescriptor:
    def __init__(self, name, obj, usage_info):
        self.name = name
        self.object = obj
        self.usage_info = usage_info


class ConsoleManager:
    def __init__(self, context_provider=None):
        """
        Args:
            context_provider:   A callable that returns a list of InternalObjectDescriptor for variables that
                                will be accessible from the Jupyter console.
        """
        self._kernel_manager = None
        self._context_provider = context_provider or (lambda: [])
        self._context = None
        self._window = None

        if JUPYTER_AVAILABLE:
            # This is sort of experimental. Initialization of a kernel manager takes some time,
            # we don't want to do that in the main thread when the application is running. Do something about it.
            try:
                self._kernel_manager = self._get_kernel_manager()
            except Exception:
                logger.info('Could not initialize kernel manager', exc_info=True)

    # noinspection PyUnresolvedReferences
    def _get_context(self):
        # See http://ipython.readthedocs.org/en/stable/api/generated/IPython.core.interactiveshell.html
        if self._context is None:
            self._context = self._context_provider()

            try:
                import matplotlib as mpl
                import matplotlib.pyplot as plt
                self._context.append(InternalObjectDescriptor('mpl', mpl, 'Imported module "matplotlib"'))
                self._context.append(InternalObjectDescriptor('plt', plt, 'Imported module "matplotlib.pyplot"'))
            except ImportError:
                pass
            try:
                import numpy as np
                self._context.append(InternalObjectDescriptor('np', np, 'Imported module "numpy"'))
            except ImportError:
                pass
            try:
                import pylab
                self._context.append(InternalObjectDescriptor('pylab', pylab, 'Imported module "pylab"'))
            except ImportError:
                pass

            import functools
            self._context.append(InternalObjectDescriptor('functools', functools, 'Imported module "functools"'))
            self._context.append(InternalObjectDescriptor('partial', functools.partial, 'functools.partial'))
            self._context.append(InternalObjectDescriptor('reduce', functools.reduce, 'functools.reduce'))

        return self._context

    def _get_kernel_manager(self):
        if self._kernel_manager is None:
            if not JUPYTER_AVAILABLE:
                raise RuntimeError('Jupyter is not available on this system')

            # Initializing the kernel
            self._kernel_manager = QtInProcessKernelManager()
            self._kernel_manager.start_kernel()
            self._kernel_manager.kernel.gui = 'qt'

            # Initializing context
            self._kernel_manager.kernel.shell.push({x.name : x.object for x in self._get_context()})

        return self._kernel_manager

    def _make_banner(self):
        longest_name = max([len(x.name) for x in self._get_context()])

        banner = 'Available entities:\n'
        for obj in self._context:
            banner += '\t%- *s -> %s\n' % (longest_name, obj.name, obj.usage_info)

        banner += 'Pyuavcan docs:  http://uavcan.org/Implementations/Pyuavcan\n'
        banner += 'DSDL reference: http://uavcan.org/Specification/7._List_of_standard_data_types\n'
        return banner

    def show_console_window(self, parent):
        if self._window is None:
            km = self._get_kernel_manager()
            banner = self._make_banner()

            def on_close():
                self._window = None

            self._window = JupyterConsoleWindow(parent, km, banner)
            self._window.on_close = on_close

        # TODO: Jupyter takes a long time to start up, which may sometimes interfere with the node. Fix it somehow.
        # Here, by using the timer we can split the long start-up sequence into two shorter bursts, which kinda helps.
        # Ideally, the node should be running in a dedicated thread.
        # noinspection PyCallByClass,PyTypeChecker
        QTimer.singleShot(50, self._window.show)

    def close(self):
        if self._window is not None:
            self._window.close()
            self._window = None
