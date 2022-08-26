
import math
import rtmidi
import pygame
import multiprocessing
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo, second2tick

def record() -> None:
    '''
    Method opens midi port and sets recording call back.

    Args:
        None
    Returns:
        None
    '''
    try:
        # find midi port to open
        ports = range(midiin.get_port_count())
        if ports:
            for i in ports:
                print(midiin.get_port_name(i))
            print("Opening port 0!") 
            midiin.open_port(0)
            midiin.set_callback(record_message)
        else:
            print('NO MIDI INPUT PORTS!')
    except KeyboardInterrupt:
        mid.save("test.mid")
        raise SystemExit

def record_message(event, deltatime) -> None:
    '''
    Records midi messages from rtmidi.
    
    Args:
        event: contains note information and deltatime.
            note: message type (int), pitch (int), velocity (int)
            deltatime: time since last message in seconds
    Returns:
        None
    '''

    note, deltatime = event

    if note[0] == 144:
        _, pitch, velocity = note
        ticks = math.floor(second2tick(deltatime, mid.ticks_per_beat, tempo))
        track.append(Message("note_on", note=note[1], velocity=note[2], time=ticks))
        print(f'Note On: {pitch} Velocity: {velocity} deltatime (s)={deltatime} deltatime (ticks)={ticks}')
    elif note[0] == 128:
        _, pitch, velocity = note
        ticks = math.floor(second2tick(deltatime, mid.ticks_per_beat, tempo))
        track.append(Message("note_off", note=pitch, velocity=velocity, time=ticks))
        print(f'Note Off: {pitch} Velocity: {velocity} deltatime (s)={deltatime} deltatime (ticks)={ticks}')

def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print("Music file %s loaded!" % music_file)
    except pygame.error:
        print("File %s not found! (%s)" % (music_file, pygame.get_error()))
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(10)

if __name__ == "__main__":

    x = None
    recorded = False

    while x != "3":

        print("Welcome! Please select an option: \n")
        print("1. Record Song\n2.Playback Song\n3.Exit\n")

        x = input("Enter input: ")

        if x == "1":

            # set tempo and pulse per quarter
            tempo = 120
            ppq = 480

            # create midi file
            midiin = rtmidi.MidiIn()
            mid = MidiFile()
            track = MidiTrack()
            mid.tracks.append(
                track
            )

            # set tempo
            track.append(MetaMessage("set_tempo", tempo=bpm2tempo(tempo)))
            tempo = bpm2tempo(tempo)

            # start recording song
            record()

            # pressing enter stops recording
            input("Press enter to stop recording: ")

            # save file
            mid.save("test.mid")
            recorded = True
            
        elif x == "2":
            if not recorded:
                print("You have not recorded a track yet.")
            else:
                # play midi file
                freq = 44100    # audio CD quality
                bitsize = -16   # unsigned 16 bit
                channels = 2    # 1 is mono, 2 is stereo
                buffer = 1024    # number of samples
                pygame.mixer.init(freq, bitsize, channels, buffer)

                # optional volume 0 to 1.0
                pygame.mixer.music.set_volume(0.8)

                # play song
                play_music("test.mid")
        
        elif x == '3':
            break
        else:
            print(f'{x} is not a valid input number.')
