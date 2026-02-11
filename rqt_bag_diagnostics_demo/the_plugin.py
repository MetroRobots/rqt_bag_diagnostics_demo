from rqt_bag.plugins.plugin import Plugin
from python_qt_binding.QtCore import Qt
from python_qt_binding.QtWidgets import QWidget
from python_qt_binding.QtGui import QBrush, QPainter, QPen
from diagnostic_msgs.msg import DiagnosticStatus
from rqt_bag import TopicMessageView, TimelineRenderer
from rclpy.time import Time
from rclpy.serialization import deserialize_message
from rqt_bag.bag_helper import to_sec


def get_color(diagnostic):
    if diagnostic.level == DiagnosticStatus.OK:
        return Qt.green
    elif diagnostic.level == DiagnosticStatus.WARN:
        return Qt.yellow
    else:  # ERROR or STALE
        return Qt.red


class DiagnosticPanel(TopicMessageView):
    name = 'Awesome Diagnostic'

    def __init__(self, timeline, parent, topic):
        super(DiagnosticPanel, self).__init__(timeline, parent, topic)
        self.widget = QWidget()
        parent.layout().addWidget(self.widget)
        self.msg = None
        self.widget.paintEvent = self.paintEvent

    def message_viewed(self, bag, entry, ros_message, msg_type_name, topic):
        super(DiagnosticPanel, self).message_viewed(bag=bag, entry=entry,
                                                    ros_message=ros_message, msg_type_name=msg_type_name, topic=topic)
        self.msg = ros_message
        self.widget.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self.widget)

        rect = event.rect()

        if self.msg is None:
            qp.fillRect(0, 0, rect.width(), rect.height(), Qt.white)
        else:
            color = get_color(self.msg)
            qp.setBrush(QBrush(color))
            qp.drawEllipse(0, 0, rect.width(), rect.height())
        qp.end()


class DiagnosticTimeline(TimelineRenderer):
    def __init__(self, timeline, height=80):
        TimelineRenderer.__init__(self, timeline, msg_combine_px=height)

    def draw_timeline_segment(self, painter: QPainter, topic, start: float, end: float,
                              x: float, y: int, width: float, height: int):
        bag_timeline = self.timeline.scene()
        start_t = Time(seconds=start)
        end_t = Time(seconds=end)

        for bag, entry in bag_timeline.get_entries_with_bags([topic], start_t, end_t):
            topic, raw_data, t = bag_timeline.read_message(bag, entry.timestamp, topic)
            msg = deserialize_message(raw_data, DiagnosticStatus)
            color = get_color(msg)
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color, 5))

            p_x = int(self.timeline.map_stamp_to_x(to_sec(Time(nanoseconds=t))))
            painter.drawLine(p_x, y, p_x, y + height - 1)


class DiagnosticBagPlugin(Plugin):
    def __init__(self):
        pass

    def get_view_class(self):
        return DiagnosticPanel

    def get_renderer_class(self):
        return DiagnosticTimeline

    def get_message_types(self):
        return ['diagnostic_msgs/msg/DiagnosticStatus']
