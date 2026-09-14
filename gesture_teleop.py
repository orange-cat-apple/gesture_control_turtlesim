import math
import cv2
import mediapipe as mp
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

class GestureTeleop(Node):
    def __init__(self):
        super().__init__('gesture_teleop')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(1.0 / 30.0, self.publish_twist)
        self.cmd = Twist()

    def set_cmd(self, lx, az):
        self.cmd.linear.x = float(lx)
        self.cmd.angular.z = float(az)

    def publish_twist(self):
        self.pub.publish(self.cmd)

def main(args=None):
    rclpy.init(args=args)
    node = GestureTeleop()
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    
    while rclpy.ok():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        cx, cy = w // 2, h // 2
        dz = 40
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)
        
        lx = 0.0
        az = 0.0
        
        cv2.line(frame, (cx, 0), (cx, h), (200, 200, 200), 1)
        cv2.line(frame, (0, cy), (w, cy), (200, 200, 200), 1)
        cv2.rectangle(frame, (cx - dz, cy - dz), (cx + dz, cy + dz), (0, 255, 255), 2)
        
        if res.multi_hand_landmarks:
            for hand_lm in res.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_lm, mp_hands.HAND_CONNECTIONS)
                lm = hand_lm.landmark
                
                tips = [8, 12, 16, 20]
                pips = [6, 10, 14, 18]
                
                def dist(p1, p2):
                    return math.hypot(p1.x - p2.x, p1.y - p2.y)
                
                is_fist = True
                for t, p in zip(tips, pips):
                    if dist(lm[t], lm[0]) >= dist(lm[p], lm[0]):
                        is_fist = False
                        break
                        
                if is_fist:
                    cv2.putText(frame, "[STOP - FIST]", (cx - 110, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                else:
                    wx, wy = int(lm[0].x * w), int(lm[0].y * h)
                    cv2.circle(frame, (wx, wy), 8, (0, 255, 0), -1)
                    
                    dx = wx - cx
                    dy = cy - wy
                    
                    if dy > dz:
                        lx = min((dy - dz) / (cy - dz) * 2.5, 2.5)
                    elif dy < -dz:
                        lx = max((dy + dz) / (cy - dz) * 1.5, -1.5)
                        
                    if dx > dz:
                        az = max(-(dx - dz) / (cx - dz) * 2.5, -2.5)
                    elif dx < -dz:
                        az = min(-(dx + dz) / (cx - dz) * 2.5, 2.5)
                        
        node.set_cmd(lx, az)
        
        bar_y = cy - int((lx / 2.5) * (cy - dz)) if lx >= 0 else cy - int((lx / 1.5) * (cy - dz))
        cv2.rectangle(frame, (30, min(cy, bar_y)), (50, max(cy, bar_y)), (0, 255, 0), -1)
        cv2.rectangle(frame, (30, cy - (cy - dz)), (50, cy + (cy - dz)), (255, 255, 255), 2)
        
        bar_x = cx - int((az / 2.5) * (cx - dz))
        cv2.rectangle(frame, (min(cx, bar_x), h - 50), (max(cx, bar_x), h - 30), (255, 0, 0), -1)
        cv2.rectangle(frame, (cx - (cx - dz), h - 50), (cx + (cx - dz), h - 30), (255, 255, 255), 2)
        
        cv2.putText(frame, f"Linear: {lx:.2f} m/s", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Angular: {az:.2f} rad/s", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow("Gesture Teleop", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
            
        rclpy.spin_once(node, timeout_sec=0)
        
    cap.release()
    cv2.destroyAllWindows()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
