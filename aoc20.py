import queue
from math import lcm

with open('aoc20.txt') as f:
    lines = [line[:-1] if line.endswith('\n') else line for line in f if line != '\n']

class Module:

    def __init__(self, destinations, name):
        self.destinations = destinations
        self.name = name
        self.inputs = {}

    def readSignal(self,signal):
        pass

    def readPulse(self, pulse):
        match pulse:
            case 'LOW':
                return self.onLowPulse()
            case 'HIGH':
                return self.onHighPulse()

    def onLowPulse(self):
        pass

    def onHighPulse(self):
        pass

    def send(self, pulse):
        return [(pulse, d, self.name) for d in self.destinations]

    def addSource(self, name):
        self.inputs[name] = ''

class FlipFlopModule(Module):

    def __init__(self, destinations,name):
        super().__init__(destinations,name)
        self.switch_on = False

    def readSignal(self,signal):
        return self.readPulse(signal[0])

    def onLowPulse(self):

        if self.switch_on:
            self.switch_on = not self.switch_on
            return self.send('LOW')
        else:
            self.switch_on = not self.switch_on
            return self.send('HIGH')

class ConjunctionModule(Module):

    def __init__(self, destinations,name):
        super().__init__(destinations,name)
        self.inputs = {}

    def readSignal(self,signal):
        pulse, _, sourcename = signal
        self.inputs[sourcename] = pulse

        if all(x == 'HIGH' for x in self.inputs.values() ):
            return self.send('LOW')
        else:
            return self.send('HIGH')

    def addSource(self, name):
        self.inputs[name] = 'LOW'

class Broadcaster(Module):

    def onLowPulse(self):
        return self.send('LOW')

    def onHighPulse(self):
        return self.send('HIGH')

    def readSignal(self,signal):
        return self.readPulse(signal[0])

class PassiveModule(Module):

    def __init__(self, destinations, name):
        super().__init__(destinations, name)
        self.hasbeenacc = False

    def readSignal(self, signal):
        self.hasbeenacc = self.hasbeenacc or signal[0]=='LOW'
        return []

class ModuleManager:

    SYMBOL_MODULE = {'%': FlipFlopModule, '&':ConjunctionModule, 'broadcaster':Broadcaster}

    def __init__(self,lines):
        self.queue = queue.Queue()
        self.modules = {}
        self._parse_lines(lines)
        self._init_all_sources()

        #this is for part 1
        self.lowsignals_sent = 0
        self.highsignals_sent = 0

        #this is for part 2
        self.current_loop = 0
        self.rx_ancestor = [k for k in moduleManager.modules['rx'].inputs][0]
        self.rx_ancestor_2 = [k for k in moduleManager.modules[self.rx_ancestor].inputs]
        self.counts_ancestors = {k:[] for k in self.rx_ancestor_2}

    def _parse_lines(self,lines):
        for l in lines:
            u,v = l.split(' -> ')
            if u[0] == 'b':
                self.modules[u] = self.SYMBOL_MODULE[u](v.split(', ') , u)
            else:
                self.modules[u[1:]] = self.SYMBOL_MODULE[u[0]](v.split(', ') , u[1:])

    def _init_all_sources(self):
        outputModules = []
        for m in self.modules.values():
            for d in m.destinations:
                if d not in self.modules and d not in outputModules:
                    outputModules.append(d)

        for om in outputModules:
            self.modules[om] = PassiveModule([], om)

        for module in self.modules.values():
            for d in module.destinations:
                self.modules[d].addSource(module.name)

    def handleNextSignal(self):
        pulse, dest, source = self.queue.get()

        if source in self.rx_ancestor_2 and pulse == 'HIGH':
            self.counts_ancestors[source].append(self.current_loop)

        match pulse:
            case 'LOW':
                self.lowsignals_sent+=1
            case 'HIGH':
                self.highsignals_sent+=1

        generatedSignals = self.modules[dest].readSignal((pulse,dest,source))

        if generatedSignals is not None:
            for gs in generatedSignals:
                self.queue.put(gs)

    def pushButton(self):
        self.current_loop+=1
        self.queue.put(('LOW', 'broadcaster', 'button'))

        while not self.queue.empty():
            self.handleNextSignal()

    def run(self, n):
        for i in range(n):
            self.pushButton()
        return self.lowsignals_sent*self.highsignals_sent

moduleManager = ModuleManager(lines)


res = moduleManager.run(1000)
moduleManager.highsignals_sent*moduleManager.lowsignals_sent

###part 2

res = moduleManager.run(50000)
lcm(*[v[0] for v in moduleManager.counts_ancestors.values()])



