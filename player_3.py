import sound
import sys
from notes import notes_to_freq
inst = sound.instrument.ElectricBass()
inst.tempo = 90

class CounterPointStatus:
    INTERVAL = "Intervals are incorrect"
    LEAPS = "Too Many leaps"
    FIFTHS = "Parallel 5ths detected"
    OCTAVES = "Parallel octaves detected"
    FALSESTART = "improper start"
    FALSEEND = "improper end"
    ERRORLESS = "No errors detected"

def line_difference(line1, line2, i):
        note1 = notes_to_freq[line1[i]][1]
        note2 = notes_to_freq[line2[i]][1]
        return note_difference(note1, note2)

def note_difference(note1, note2):
    diff = abs(note1 - note2)
    return diff

def check_intervals(lines):
    line1 = lines[0]
    line2 = lines[1]
    for i in range(len(line1)):
        ##convert current note into pitch class w/ dictionary
        diff = line_difference(line1, line2, i)
        invalid_harmonies = (1, 2, 3, 5, 6, 10, 11)
        if diff in invalid_harmonies:
            return CounterPointStatus.INTERVAL
    return "No interval errors detected"

#
def check_parallels(lines):
    line1 = lines[0]
    line2 = lines[1]
    fifth_counter = 0
    octave_counter = 0
    for i in range(len(line1)):
        diff = line_difference(line1, line2, i)
        if diff == 0 or diff == 12:
            octave_counter += 1
        elif diff == 7:
            fifth_counter += 1
        else:
            fifth_counter = 0
            octave_counter = 0
        if fifth_counter == 2:
            return CounterPointStatus.FIFTHS
        elif octave_counter == 2:
            return CounterPointStatus.OCTAVES
    return "no parallels detected"

##returns a list of the first and last note of a line parameter
def get_start_end(line):
    start = notes_to_freq[line[0]][1]
    end = notes_to_freq[line[-1]][1]
    start_end = [start, end]
    return start_end

##starting/ending notes must be either in unison or octaves
def check_start_end(lines):
    line1_start_end = get_start_end(lines[0])
    line2_start_end = get_start_end(lines[1])
    start_dif = note_difference(line1_start_end[0], line2_start_end[0])
    end_dif = note_difference(line1_start_end[1], line2_start_end[1])
    if start_dif % 12 != 0:
        return CounterPointStatus.FALSESTART
    if end_dif % 12 != 0:
        return CounterPointStatus.FALSEEND
    return "Start and finish both appropriate"

##Determine a constant value that the total difference in leaps
##cannot excede
def determine_leap_constant(line2):
    length = len(line2)
    leap_constant = length/3
    return leap_constant

##Checks the counterpoint line (NOT CANTUS FIRMUS) if too many leaps occur
def check_leaps(line2):
    leap_tracker = 0
    iter_notes = iter(line2)
    previous_note = notes_to_freq[next(iter_notes)][1]
    for note in iter_notes:
        curr_pitch_class = notes_to_freq[note][1]
        diff = note_difference(curr_pitch_class, previous_note)
        ##if it is a leap (greater than a 3rd) incriment the leaptracker
        if diff > 4:
            leap_tracker += 1
        previous_note = curr_pitch_class
    leap_constant = determine_leap_constant(line2)
    if (leap_tracker > leap_constant):
        return CounterPointStatus.LEAPS
    return "Not too many leaps"


def check_legality(lines):
    print(check_intervals(lines))
    print(check_start_end(lines))
    print(check_parallels(lines))
    print(check_leaps(lines[1]))

#reads the argument files into a string split by spaces
##returns a list with both objects
def load_music():
    filename = sys.argv[1]
    file = open(filename)
    music_data = file.read().split("\n")[0]
    ##splitting string into list of "notes"
    music_notes1 = music_data.split(" ")
    filename = sys.argv[2]
    file = open(filename)
    music_data = file.read().split("\n")[0]
    music_notes2 = music_data.split(" ")
    music_parts = [music_notes1, music_notes2]
    return music_parts

##convert string into compatible frequencies for playing
def parse_notes(music_data):
    tune = parse_note(music_data[0])
    for note in music_data[1:]:
        tune = tune & parse_note(note)
    return tune

def parse_note(raw_note):
    freq = notes_to_freq[raw_note][0]
    playable_note = inst.note(freq)
    return playable_note

##play two lines at once
def play_double(notes1, notes2):
    doubled_notes = (notes1 + notes2)/2
    play_music(doubled_notes)

##play single line of music
def play_music(notes):
    notes.play()

def main():
    music_data = load_music()
    check_legality(music_data)
    notes1 = parse_notes(music_data[0])
    notes2 = parse_notes(music_data[1])
    play_double(notes1, notes2)

if __name__ == "__main__":
    main()
