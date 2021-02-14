import time
import rtmidi

bridge = rtmidi.MidiOut()
bridge.open_virtual_port("My virtual output")
bridge_back = rtmidi.MidiIn()
bridge_back.open_virtual_port("My virtual output")

# Connect to Akai249
midiin = rtmidi.MidiIn()
midiin.open_port(0)
midiout = rtmidi.MidiOut()
midiout.open_port(0)
note_on = [0x91, 60, 112] # channel 1, middle C, velocity 112
note_off = [0x81, 60, 0]
# while True:
#     midiout.send_message(note_on)
#     time.sleep(.05)
#     midiout.send_message(note_off)
#     time.sleep(.05)

class Note(object):
    def __new__(cls, msg):
        # failed constructions
        if msg is None:
            return None
        if len(msg[0]) < 3:
            print("Bad Msg ", str(msg))
            return None
        return object.__new__(cls)
    def __init__(self, msg):
        print("On Msg ", str(msg))
        self.channel = hex(msg[0][0])[3]
        self.code = hex(msg[0][0])[2]
        self.note = msg[0][1]
        self.val  = msg[0][2]
    def __str__(self):
        return str(self.code) + str(self.channel) + str(self.note)
    def to_Midi(self):
        opcode = int("0x"+self.code+self.channel, 0)
        return [opcode, self.note, self.val]

def parse_message(msg):
    if msg == None:
        return None
    ret = ""
    for x in msg[0]:
        if ret == "":
            ret += str(hex(x)) + ", "
        else:
            ret += str(x) + " "
    return ret

bool = True

noteOffDict = {}
depressedPadsDict = {}

while True:
    timer = time.time()
    #print("Begin poll.")
    msg = midiin.get_message()
    ableton_response = bridge_back.get_message()
    if msg is not None:
        print(parse_message(msg))
        print (noteOffDict)
        bridge.send_message(msg[0])
        # if a pad is released, see if we need to send pending LED messages
        note = Note(msg)
        if note is not None:
            hash = str(note.channel) + str(note.note)
            # if it's a depressed pad, register it
            if note.code == "9" and note.channel != "0":
                depressedPadsDict[hash] = True
            # if a pad is released, see if you need to release it
            if note.code == "8" and note.channel != "0":
                if hash in depressedPadsDict:
                    del depressedPadsDict[hash]
            # if it's a pending light signal, send it
            if hash in noteOffDict:
                send = noteOffDict[hash].to_Midi()
                print("To SEND?" + str(send))
                midiout.send_message(send)
                del noteOffDict[hash]
        # if bool:
        #     midiout.send_message(note_on)
        #     bool = not bool
        # else:
        #     midiout.send_message(note_off)
        #     bool = not bool
    if ableton_response is not None:
        note = Note(ableton_response)
        if note is None:
            continue
        hash = str(note.channel) + str(note.note)
        # if pad is not pressed down, send the response to controller
        if hash not in depressedPadsDict:
            midiout.send_message(note.to_Midi())
        else:
            # put the led signal in the pending list
            noteOffDict[hash] = note
    time.sleep(0.001)
