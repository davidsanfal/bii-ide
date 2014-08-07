from PyQt4 import QtCore


class ShowEventFilter(QtCore.QObject):
    def __init__(self, to_do):
        self.to_do = to_do
        super(ShowEventFilter, self).__init__()

    def eventFilter(self, filteredObj, event):
        if event.type() == QtCore.QEvent.Show:
            self.to_do()
        return QtCore.QObject.eventFilter(self, filteredObj, event)
