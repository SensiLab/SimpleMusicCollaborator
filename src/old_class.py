

import math
import rtmidi
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo, second2tick

class SimpleMusicCollaborator():

    def __init__(self, tempo=120, ppq=480) -> None:
        
        # create midi file
        self.midiin = rtmidi.MidiIn()
        self.mid = MidiFile()
        self.track = MidiTrack()
        self.mid.tracks.append(
            self.track
        )

        # set tempo
        self.track.append(MetaMessage("set_tempo", tempo=tempo))
        self.tempo = bpm2tempo(tempo)

    def record(self) -> None:
        '''
        Method starts recording midi from the input device.
        '''
        try:
            # find midi port to open
            ports = range(self.midiin.get_port_count())
            if ports:
                for i in ports:
                    print(self.midiin.get_port_name(i))
                print("Opening port 0!") 
                self.midiin.open_port(0)

                while True:
                    m = self.midiin.get_message()
                    if m:
                        note, deltatime = m
                        self.print_message(note, deltatime)
            else:
                print('NO MIDI INPUT PORTS!')
        except KeyboardInterrupt:
            self.mid.save("test.mid")
    
    def print_message(self, note, deltatime) -> None:
        '''
        Prints midi message for debugging purposes
        '''

        if note[0] == 144:
            _, pitch, velocity = note
            # ticks = math.floor(deltatime*self.time_per_tick*100)
            ticks = math.floor(second2tick(deltatime, self.mid.ticks_per_beat, self.tempo))
            self.track.append(Message("note_on", note=pitch, velocity=velocity, time=ticks))
            print(f'Note On: {pitch} Velocity: {velocity} deltatime (s)={deltatime} deltatime (ticks)={ticks}')
        elif note[0] == 128:
            _, pitch, velocity = note
            # ticks = math.floor(deltatime*self.time_per_tick*100)tT
            ticks = math.floor(second2tick(deltatime, self.mid.ticks_per_beat, self.tempo))
            self.track.append(Message("note_off", note=pitch, velocity=velocity, time=ticks))
            print(f'Note Off: {pitch} Velocity: {velocity} deltatime (s)={deltatime} deltatime (ticks)={ticks}')