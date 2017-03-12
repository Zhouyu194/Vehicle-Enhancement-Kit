class StateMachine(object):
    def __init__(self, period, tickFct):
        self.state = "init_state"
        self.period = period
        self.elapsedTime = 0
        self.TickFunction = tickFct

