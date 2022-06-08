from PyQt5.QtOpenGL import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sys


class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        self.setAcceptDrops(True)
        self.container = QVBoxLayout()
        self.setLayout(self.container)

        self.label = QLabel("Select on the checkbox to draw, click on 'Clear' to clear the window")
        self.label.setFont(QtGui.QFont("", 10, 1))
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.container.addWidget(OpenGLWindow(self), 12)
        self.container.addStretch(1)
        self.container.addWidget(self.label)
        self.container.addWidget(SelectionWindow(self), 1)

        self.setWindowTitle("Functions graph")
        self.setGeometry(200, 150, 700, 800)


class SelectionWindow(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.number_of_selected = 0

        self.inner_layout = QHBoxLayout()
        self.inner_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(self.inner_layout)

        self.graph1 = QCheckBox('sinx')
        self.inner_layout.addWidget(self.graph1)

        self.graph2 = QCheckBox('cosx')
        self.inner_layout.addWidget(self.graph2)

        self.graph3 = QCheckBox('x^2')
        self.inner_layout.addWidget(self.graph3)

        self.graph4 = QCheckBox('|x|')
        self.inner_layout.addWidget(self.graph4)

        self.graph5 = QCheckBox('x^3')
        self.inner_layout.addWidget(self.graph5)

        self.graph6 = QCheckBox('2^x')
        self.inner_layout.addWidget(self.graph6)

        self.graph1.stateChanged.connect(lambda: self.change_state(self.graph1))
        self.graph2.stateChanged.connect(lambda: self.change_state(self.graph2))
        self.graph3.stateChanged.connect(lambda: self.change_state(self.graph3))
        self.graph4.stateChanged.connect(lambda: self.change_state(self.graph4))
        self.graph5.stateChanged.connect(lambda: self.change_state(self.graph5))
        self.graph6.stateChanged.connect(lambda: self.change_state(self.graph6))

        self. graphs = [self.graph1,self.graph2, self.graph3, self.graph4, self.graph5, self.graph6]

        self.clear = QPushButton("Clear", self)
        self.inner_layout.addWidget(self.clear)
        self.clear.clicked.connect(self.clearer)

    def clearer(self):
        self.number_of_selected = 0
        OpenGLWindow.selecteds = [0]*6
        for g in self.graphs:
            g.setDisabled(False)
            g.setChecked(False)

    def change_state(self, button):
        on_off = OpenGLWindow.selecteds
        if button.text() == 'sinx':
            on_off[0] = 1 if button.isChecked() else 0
        elif button.text() == 'cosx':
            on_off[1] = 1 if button.isChecked() else 0
        elif button.text() == 'x^2':
            on_off[2] = 1 if button.isChecked() else 0
        elif button.text() == '|x|':
            on_off[3] = 1 if button.isChecked() else 0
        elif button.text() == 'x^3':
            on_off[4] = 1 if button.isChecked() else 0
        elif button.text() == '2^x':
            on_off[5] = 1 if button.isChecked() else 0

        select = 0
        for n in on_off:
            if n: select += 1
        if select >= 2:
            for g in self.graphs:
                g.setDisabled(True)


class OpenGLWindow(QGLWidget):
    selecteds = [0, 0, 0, 0, 0, 0]

    def __init__(self, parent=None):
        QGLWidget.__init__(self, parent)
        self.x_axis = np.array([-4, 4])
        self.y_axis = np.array([-4, 4])
        self.colors = [[0.3, 0.7, 0.5], [0.3, 0.2, 0.8], [0.5, 0.4, 0.5], [0.9, 0.7, 0.5], [0.9, 0.7, 0.9], [0.3, 1.0, 0.5]]
        self.x = np.linspace(-3, 3, 300)
        self.graphs = [np.sin(self.x), np.cos(self.x), np.power(self.x, 2), np.abs(self.x), np.power(self.x, 3), np.power(2, self.x)]

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(0.3, 0.5, 0.6)

        glLineWidth(1)
        glBegin(GL_LINE_STRIP)
        glVertex2f(self.x_axis[0], 0)
        glVertex2f(self.x_axis[1], 0)
        glEnd()
        glBegin(GL_LINE_STRIP)
        glVertex2f(0, self.y_axis[0])
        glVertex2f(0, self.y_axis[1])
        glEnd()

        glLineWidth(2)
        for idx in range(6):
            if OpenGLWindow.selecteds[idx] == 1:
                glBegin(GL_LINE_STRIP)
                glColor(self.colors[idx])
                for x, y in zip(self.x, self.graphs[idx]):
                    glVertex2f(x, y)
                glEnd()
        glFlush()
        self.update()

    def resizeGL(self, w, h):
        glLoadIdentity()
        gluOrtho2D(-4.6, 4.6, -4.6, 4.6)
        glViewport(0, 0, w, h)

    def initializeGL(self):
        glClearColor(0.2, 0.2, 0.2, 0.9)
        gluOrtho2D(-4.6, 4.6, -4.6, 4.6)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit((app.exec_()))
