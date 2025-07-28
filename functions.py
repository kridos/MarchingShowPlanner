def returnLinearFunction(start, end, duration):

    def linearOutput(currentTime):
        return ((end - start) / duration) * currentTime + start

    return linearOutput