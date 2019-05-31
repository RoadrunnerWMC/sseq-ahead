import ndspy.soundSequence


def checkStepAmount(amount):
    """
    Helper function to do sanity checks on the provided step amount
    """
    if not isinstance(amount, int):
        raise ValueError('step amount must be integral')
    if amount < 0:
        raise ValueError('step amount must be non-negative')


def checkTimeAmount(amount):
    """
    Helper function to do sanity checks on the provided time amount
    """
    if amount < 0:
        raise ValueError('time amount must be non-negative')


class SSEQGlobalState:
    """
    Should maybe be a data class?
    """
    volume = 127 # TODO: this is the actual default, right
    tempo = 100 # TODO: just completely made this up out of nowhere


class SSEQTrackState:
    """
    ibid
    """
    restTimer = 0

    volume = 127 # TODO: this is the actual default, right
    bankID = 0 # TODO: this is the actual default, right
    instrumentID = 0 # TODO: this is the actual default, right


class SSEQTrackPlayer:
    """
    Plays one track
    """
    globalState = None
    trackState = None
    events = None
    _idx = 0
    _processedPC = False

    def __init__(self, globalState, trackState, events, initialIndex=0):
        self.globalState = globalState
        self.trackState = trackState
        self.events = events
        self._idx = initialIndex

    @property
    def pc(self):
        """
        The event either currently being processed, or which will be processed next
        """
        return self.events[self._idx]

    def step(self, amount):
        """
        Step by `amount` time steps. A nonzero value will end with
        self.pc on or immediately following a rest event, and "0" will
        step through all pending events with zero duration.
        """
        checkStepAmount(amount)

        continueIfZero = (amount == 0)

        def progress():
            """
            Attempt to make progress, and return True if we should go again
            """
            nonlocal amount

            keepGoing = True

            # Process the current event if we haven't done so yet
            if not self._processedPC:
                self._processPC()
                self._processedPC = True

            # Handle rest timers
            if self.trackState.restTimer > 0:
                if amount >= self.trackState.restTimer:
                    # We can cover the whole rest period, so do so
                    self.trackState.restTimer = 0
                    amount -= self.trackState.restTimer
                else:
                    # We can't cover the entire rest period. Stop here.
                    self.trackState.restTimer -= amount
                    return False

            # If we're not waiting for anything, move to the next event
            if self.trackState.restTimer == 0:
                self._moveNext()
                self._processedPC = False

                if not continueIfZero:
                    keepGoing = False

            return keepGoing

        while progress():
            pass


    def _processPC(self):
        """
        Process the effects of self.pc. This must happen only once per
        sequence event!
        This function will not modify self.pc. To do that, call
        _moveNext().
        """
        e = self.pc

        if isinstance(e, ndspy.soundSequence.NoteSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.RestSequenceEvent):
            self.trackState.restTimer = e.duration
        elif isinstance(e, ndspy.soundSequence.InstrumentSwitchSequenceEvent):
            self.trackState.bankID = e.bankID
            self.trackState.instrumentID = e.instrumentID
        elif isinstance(e, ndspy.soundSequence.BeginTrackSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.JumpSequenceEvent):
            pass
        elif isinstance(e, ndspy.soundSequence.CallSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.RandomSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.FromVariableSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.IfSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VariableAssignmentSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VariableAdditionSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VariableSubtractionSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VariableMultiplicationSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VariableDivisionSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VariableShiftSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VariableRandSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VariableUnknownB7SequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VariableEqualSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VariableGreaterThanOrEqualSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VariableGreaterThanSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VariableLessThanOrEqualSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VariableLessThanSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VariableNotEqualSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.PanSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.TrackVolumeSequenceEvent):
            self.trackState.volume = e.value
            # print('Set track volume to', e.value)
        elif isinstance(e, ndspy.soundSequence.GlobalVolumeSequenceEvent):
            self.globalState.volume = e.value
        elif isinstance(e, ndspy.soundSequence.TransposeSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.PortamentoSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.PortamentoRangeSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.TrackPrioritySequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.MonoPolySequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.TieSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.PortamentoFromSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VibratoDepthSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VibratoSpeedSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VibratoTypeSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VibratoRangeSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.PortamentoOnOffSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.PortamentoDurationSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.AttackRateSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.DecayRateSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.SustainRateSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.ReleaseRateSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.BeginLoopSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.ExpressionSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.PrintVariableSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.VibratoDelaySequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.TempoSequenceEvent):
            self.globalState.tempo = e.value
        elif isinstance(e, ndspy.soundSequence.SweepPitchSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.EndLoopSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.ReturnSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.DefineTracksSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.EndTrackSequenceEvent):
            ...
        elif isinstance(e, ndspy.soundSequence.RawDataSequenceEvent):
            ...
        else:
            raise ValueError('Unexpected sequence event:', e)


    def _moveNext(self):
        """
        Move self.pc to whatever follows it, respecting jumps and the
        like.
        """
        e = self.pc

        if isinstance(e, ndspy.soundSequence.BeginTrackSequenceEvent):
            raise NotImplementedError
        elif isinstance(e, ndspy.soundSequence.JumpSequenceEvent):
            self._idx = self.events.index(e.destination)
        elif isinstance(e, ndspy.soundSequence.CallSequenceEvent):
            raise NotImplementedError
        elif isinstance(e, ndspy.soundSequence.EndLoopSequenceEvent):
            raise NotImplementedError
        elif isinstance(e, ndspy.soundSequence.ReturnSequenceEvent):
            raise NotImplementedError
        elif isinstance(e, ndspy.soundSequence.EndTrackSequenceEvent):
            raise NotImplementedError
        else:
            self._idx += 1


class SSEQPlayer:
    """
    ABC for a SSEQ player
    """
    globalState = None
    trackStates = None
    trackPlayers = None

    timeElapsed = 0.0 # seconds
    stepsElapsed = 0

    def step(self, amount):
        # We have to keep all track players in sync because they can
        # change global things within the requested `amount` (such as
        # tempo)
        checkStepAmount(amount)

        targetTotal = self.stepsElapsed + amount

        while True:

            self._singleStepUntilChangeOr(amount)
            amount = targetTotal - self.stepsElapsed

            # Putting the test here to make it like a do-while loop
            if amount <= 0:
                break

    def timeStep(self, amount):
        """
        amount is measured in seconds
        """
        # We have to keep all track players in sync because they can
        # change global things within the requested `amount` (such as
        # tempo)
        checkTimeAmount(amount)

        targetTotal = self.timeElapsed + amount

        while True:

            # steps = (seconds) * (mins/sec) * (beats/min) * (steps/beat)
            #       = secs * 1/60 * tempo * 48
            #       = secs * tempo * 48/60
            steps = int(amount * self.globalState.tempo * 48/60)
            if steps == 0 and amount > 0: steps = 1
            self._singleStepUntilChangeOr(steps)
            amount = targetTotal - self.timeElapsed

            # Putting the test here to make it like a do-while loop
            if amount <= 0:
                break

    def _singleStepUntilChangeOr(self, maxSteps):
        """
        Step all tracks simultaneously until either something changes,
        or maxSteps (whichever comes first)
        """
        # Check how many steps we can do at once before something changes
        steps = min(ts.restTimer for ts in self.trackStates.values())
        steps = min(steps, maxSteps)

        # Do that many steps
        for tp in self.trackPlayers.values():
            tp.step(steps)
        self.stepsElapsed += steps

        # seconds = steps * (beats/step) * (mins/beat) * (secs/min)
        #         = steps * 1/48 * 1/tempo * 60
        #         = steps / tempo * 60/48
        self.timeElapsed += steps / self.globalState.tempo * 60/48


class SSEQMusicPlayer(SSEQPlayer):
    """
    Plays a ndspy.extras.music.SSEQMusic
    """
    timeElapsed = 0.0 # seconds

    def __init__(self, music):
        self.music = music
        self.globalState = SSEQGlobalState()
        self.trackStates = {}
        self.trackPlayers = {}

        for id, t in music.tracks.items():
            self.trackStates[id] = SSEQTrackState()
            self.trackPlayers[id] = SSEQTrackPlayer(
                self.globalState, self.trackStates[id], t.events)


class ParsedSSEQPlayer(SSEQPlayer):
    """
    Plays a parsed ndspy.soundSequence.SSEQ
    """
    def __init__(self, sseq):
        self.sseq = sseq
        self.globalState = SSEQGlobalState()
        self.trackStates = {0: SSEQTrackState()}

        trackPlayer = SSEQTrackPlayer(
            self.globalState, self.trackStates[0], self.sseq.events)
        self.trackPlayers = {0: trackPlayer}


class UnparsedSSEQPlayer(SSEQPlayer):
    """
    Play an unparsed ndspy.soundSequence.SSEQ
    """
    ...


def player(item):
    """
    Return an appropriate SSEQPlayer subclass instance for the given item
    """
    if isinstance(item, ndspy.extras.music.SSEQMusic):
        return SSEQMusicPlayer(item)
    elif isinstance(item, ndspy.soundSequence.SSEQ):
        return (ParsedSSEQPlayer if item.parsed else UnparsedSSEQPlayer)(item)

    raise ValueError(f'No player available for {item}')
