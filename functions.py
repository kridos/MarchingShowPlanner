import math

def returnLinearFunction(start, end, duration, start_time = 0.0):

    def linearOutput(currentTime):
        x = ((end[0] - start[0]) / duration) * (currentTime - start_time) + start[0]
        y = ((end[1] - start[1]) / duration) * (currentTime - start_time) + start[1]
        return (x,y)

    return linearOutput



def returnCircularFunction(start, end, duration, center, start_time = 0.0):

    def circularOutput(currentTime):
        cx, cy = center
        r = math.sqrt((start[0] - cx)**2 + (start[1] - cy)**2)
        
        start_angle = math.atan2(start[1] - cy, start[0] - cx)
        end_angle = math.atan2(end[1] - cy, end[0] - cx)
        
        theta = start_angle + (end_angle - start_angle) * ((currentTime - start_time) / duration)
        
        x = cx + r * math.cos(theta)
        y = cy + r * math.sin(theta)
        
        return (x,y)
        

    return circularOutput