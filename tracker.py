class SimpleTracker:
    def __init__(self):
        self.track_id = 0
        self.center_points = {}
        self.tracked_ids = set()

    def update(self, objects_rect):
        objects_bbs_ids = []
        for rect in objects_rect:
            x, y, w, h = rect
            cx = x + w // 2
            cy = y + h // 2

            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = abs(cx - pt[0]) + abs(cy - pt[1])
                if dist < 50:
                    self.center_points[id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            if not same_object_detected:
                self.center_points[self.track_id] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.track_id])
                self.track_id += 1

        return objects_bbs_ids