from rqt_bag.plugins.plugin import Plugin
from python_qt_binding.QtCore import Qt
from python_qt_binding.QtWidgets import QWidget
from python_qt_binding.QtGui import QBrush, QPainter, QPen
from diagnostic_msgs.msg import DiagnosticStatus
from rqt_bag import TopicMessageView, TimelineRenderer
from rclpy.time import Time
import math
from rclpy.serialization import deserialize_message


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
        self.qp = QPainter()
        self.qp.begin(self.widget)

        rect = event.rect()

        if self.msg is None:
            self.qp.fillRect(0, 0, rect.width(), rect.height(), Qt.white)
        else:
            color = get_color(self.msg)
            self.qp.setBrush(QBrush(color))
            self.qp.drawEllipse(0, 0, rect.width(), rect.height())
        self.qp.end()


class DiagnosticTimeline(TimelineRenderer):
    def __init__(self, timeline, height=80):
        TimelineRenderer.__init__(self, timeline, msg_combine_px=height)

    def draw_timeline_segment(self, painter, topic, start, end, x, y, width, height):
        def _convert_stamp(float_t):
            nano, sec = math.modf(float_t)
            return Time(seconds=int(sec), nanoseconds=int(nano * 1e9))

        bag_timeline = self.timeline.scene()
        start_t = _convert_stamp(start)
        end_t = _convert_stamp(end)

        for bag, entry in bag_timeline.get_entries_with_bags([topic], start_t, end_t):
            topic, raw_data, t = bag_timeline.read_message(bag, entry.timestamp, topic)
            msg = deserialize_message(raw_data, DiagnosticStatus)
            color = get_color(msg)
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color, 5))

            p_x = self.timeline.map_stamp_to_x(t / 1e9)
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
