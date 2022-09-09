
import math
import rtmidi
import pygame
import tkinter as tk
import tkinter.ttk as ttk

from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo, second2tick
from generate_melody import MagentaMusicTransformer

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
            print(f"Opening port {i}!") 
            midiin.open_port(i)
            midiin.set_callback(record_message)
        else:
            print('NO MIDI INPUT PORTS!')
    except KeyboardInterrupt:
        mid.save("test.mid")
        raise SystemExit

def record_message(event, data) -> None:
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

def record_button():
    if record_btn["text"] == "Record":
        print(1)
        record_btn.config(text="Stop Recording")

        global mid
        global track
        global tempo
        global midiin
        global recorded

        recorded= True

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

    else:
        record_btn.config(text="Record")
        mid.save("test.mid")
        midiin.close_port()

def playback():
    
    if not recorded:
        # TODO: add pop-up box here
        print("Nothing to playback.")
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

def generate_music():

    music_transformer.generate("test.mid")

    return

def playback_generated():

        # play midi file
        freq = 44100    # audio CD quality
        bitsize = -16   # unsigned 16 bit
        channels = 2    # 1 is mono, 2 is stereo
        buffer = 1024    # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)

        # optional volume 0 to 1.0
        pygame.mixer.music.set_volume(0.8)

        # play song
        play_music("generated.mid")


if __name__ == "__main__":

    recorded = False
    music_transformer = MagentaMusicTransformer("../model/melody_conditioned_model_16.ckpt")

    window = tk.Tk()
    window.title("Test Window")
    window.geometry('500x600')

    title = ttk.Label(window, text="Simple Music Collaborator", font=("Arial Bold", 36))
    title.pack(side='top')

    record_btn = tk.Button(window, text="Record", command=record_button, bg='#be2538', width=16, height=3, font=("Arial", 24))
    record_btn.place(relx=0.5, rely=0.2, anchor='center')

    playback_btn = tk.Button(window, text="Playback Recording", command=playback, width=16, height=3, font=("Arial", 24))
    playback_btn.place(relx=0.5, rely=0.4, anchor='center')

    create_btn = tk.Button(window, text="Generate Music", command=generate_music, width=16, height=3, font=("Arial", 24))
    create_btn.place(relx=0.5, rely=0.6, anchor='center')

    create_btn = tk.Button(window, text="Play Generated Music", command=playback_generated, width=16, height=3, font=("Arial", 24))
    create_btn.place(relx=0.5, rely=0.8, anchor='center')

    window.mainloop()
