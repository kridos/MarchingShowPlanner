def returnLinearFunction(start, end, duration, start_time = 0.0):

    def linearOutput(currentTime):
        return ((end - start) / duration) * (currentTime - start_time) + start

    return linearOutput