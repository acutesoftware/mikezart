import musictheory
import random
import operator
import pianoprinter

# rselect RandomSelect returns random element of list
def rselect(lista):
    return random.choice(lista)


# wselect WeightedSelect returns element of dictionary based on dict weights {element:weight}
def wselect(dicti):
    total=0
    for i in list(dicti):
        total = total + dicti[i]
    indice = total*random.random()
    for i in list(dicti):
        if dicti[i]>=indice:
            return i
        indice = indice - dicti[i]
    raise ValueError ("something went wrong")



def mainMenu():
    print("\nWelcome to the MikezarIO music creation interface (art by Forrest Cook & Alexander Craxton)")
    print("      ________________________________    \n     /    o   oooo ooo oooo   o o o  /\    \n    /    oo  ooo  oo  oooo   o o o  / /    \n   /    _________________________  / /     \n  / // / // /// // /// // /// / / / /      \n /___ //////////////////////////_/ /       \n \____\________________________\_\/  \n")
    while True:
        print("Pp - Create a Palette")
        print("Ee - Edit a Palette")
        print("Ss - Create a Structure")
        print("Cc - Create a Song from a Palette and a Structure")    #UNDEFINED OPTIONS
        print("Qq - Quit")
        
        inp = input(">")
        if inp in "Pp":
            paletteMenu()
        
        elif inp in "Qq":
            return

    
def bpmMenu():
    while True:
        print("Please input the number of beats per minute for this Palette (write G or g for random):")
        bpmt = input(">")
        if bpmt in "Gg":
            bpm = wselect({80:5, 100:10, 120:20, 140:10, 160:5, 180:5})
        else:
            bpm = eval(bpmt)
        while True:
            print(str(bpm) + " beats per minute. Accept? (Yy, Nn, Pp(preview)):")
            inp = input(">")
            if inp in "Yy":
                return bpm
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewbpm(bpm)

def csizeMenu():
    while True:
        print("Please input the number of beats in a chunk for this Palette (write G or g for random):")
        ct = input(">")
        if ct in "Gg":
            cs = wselect({2:5, 3:10, 4:20, 5:10, 6:5})
        else:
            cs = eval(ct)
        while True:
            print(str(cs) + " (x4 quarter) beats in a chunk. Accept? (Yy, Nn, Pp(preview)):")
            inp = input(">")
            if inp in "Yy":
                return cs
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewcs(cs)
                
def psizeMenu():
    while True:
        print("Please input the number of chunks in a progression for this Palette (write G or g for random):")
        pt = input(">")
        if pt in "Gg":
            ps = rselect((2,3,4,5,6))
        else:
            ps = eval(pt)
        while True:
            print(str(ps) + " chunks in a progression. Accept? (Yy, Nn, Pp(preview)):")
            inp = input(">")
            if inp in "Yy":
                return ps
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewps(ps)
    
def progcMenu():
    while True:
        print("Please input the number of progressions in a voice for this Palette (write G or g for random):")
        pt = input(">")
        if pt in "Gg":
            pc = rselect((2,3,4,5,6))
        else:
            pc = eval(pt)
        while True:
            print(str(pc) + " progressions in a voice. Accept? (Yy, Nn, Pp(preview)):")
            inp = input(">")
            if inp in "Yy":
                return pc
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewpc(pc)
    
def scaleMenu():
    while True:
        print("Please input the list of 7 notes in the Scale (ex: 'C Ds E ...'), a smaller list to autocomplete, or write G or g for random:")
        scalet = input(">")
        if scalet in "Gg":
            scale = musictheory.scale7()
        else:
            notenames = str.split(scalet, " ")
            notes = ()
            for i in range(len(notenames)):
                if len(notenames[i]) != 0:
                    notes = notes + (musictheory.mnote.fromName(notenames[i] + "0"),)
            scale = musictheory.scale7(notes)
        while True:
            print ("Your scale: "+str(scale)[2:-2])
            pianoprinter.octoPrint(scale._notes)
            print("Chords |Short  |Normal |Large  ")
            print("Minor  |" + str(len(scale.getChords("minor", "short"))) + "      |" + str(len(scale.getChords("minor", "normal"))) + "      |" + str(len(scale.getChords("minor", "large"))) + "      ")
            print("Weird  |" + str(len(scale.getChords("weird", "short"))) + "      |" + str(len(scale.getChords("weird", "normal"))) + "      |" + str(len(scale.getChords("weird", "large"))) + "      ")
            print("Major  |" + str(len(scale.getChords("major", "short"))) + "      |" + str(len(scale.getChords("major", "normal"))) + "      |" + str(len(scale.getChords("major", "large"))) + "      ")
            print()
            print ("Accept? (Yy, Nn, Pp(preview)):")
            inp = input(">")
            if inp in "Yy":
                return scale
            elif inp in "Nn":
                break
            elif inp in "Pp":
                previewscale(scale)
            
def paletteMenu():
    while True:
        print("Starting Palette creation:")
        bpm = bpmMenu()
        csize = csizeMenu()
        progsize = psizeMenu()
        progcount = progcMenu()
        scale = scaleMenu()
        pal = musictheory.palette(scale, progsize, progcount, csize)
        while True:
            print("Palette created, Accept? Yy Nn(redo) Qq(quit):")
            inp = input(">")
            if inp in "Yy":
                name = nameMenu()
                paletteEdit(pal, name)
                return
            elif inp in "Nn":
                print("Retrying:")
                break
            elif inp in "Qq":
                return
        
def nameMenu():
    while True:
        print("Name this palette (will be used as filename):")
        name = input(">")
        while True:
            print(name + ", is this name ok? Yy Nn:")
            inp = input(">")
            if inp in "Yy":
                return name
            elif inp in "Nn":
                break
            
def paletteEdit(pal, name): # Main palette edition thing, can enter theme or prog edition
    print("Entering palette edition interface for palette: "+name)
    if pal._n1 == None:
        cprogN1 = None
    else:
        cprogN1 = pal._n1._cprog
    if pal._n2 == None:
        cprogN2 = None
    else:
        cprogN2 = pal._n2._cprog
    if pal._ch == None:
        cprogCH = None
    else:
        cprogCH = pal._ch._cprog
    if pal._bg != None:
        cprogCH = pal._bg._cprog
    while True:
        if cprogN1 == None:
            print ("Warning: undefined chord progression: Verses 1!")
        if cprogN2 == None:
            print ("Warning: undefined chord progression: Verses 2!")
        if cprogCH == None:
            print ("Warning: undefined chord progression: Chorus/Bridge!")
        if pal._n1 == None:
            print ("Warning: undefined Theme: Verses 1!")
        if pal._n2 == None:
            print ("Warning: undefined Theme: Verses 2!")
        if pal._ch == None:
            print ("Warning: undefined Theme: Chorus!")
        if pal._bg == None:
            print ("Warning: undefined Theme: Bridge!")
        if pal._ge == None:
            print ("Warning: undefined Theme: General!")
        print("DEBUG", cprogCH)
        print("Cc - Define chord Progressions")
        print("Tt - Create a Theme")
        print("Ee - Edit a Theme")
        print("Dd - Display Palette Properties")
        print("Ss - Save Palette")
        print("Qq - Quit")
        inp = input(">")                                #UNDEFINED OPTIONS
        if inp in "Cc":
            res = cprogMenu(pal, cprogN1, cprogN2, cprogCH)
            if res == False:
                res = False
            elif res[0] == "n1":
                cprogN1 = res[1]
            elif res[0] == "n2":
                cprogN2 = res[1]
            elif res[0] == "ch":
                crpogCH = res[1] #BUG !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
def cprogMenu(pal, cprogN1, cprogN2, cprogCH): # Edit progressions for palette, returns ("ch", prog) or False if failed
    while True:
        print("Note: changed progressions are only taken into effect if their themes are recreated")
        if cprogN1 == None:
            print ("n1 - Define Verses 1 chord Progression (undefined!)")
        else:
            print ("n1 - Define Verses 1 chord Progression")
        if cprogN2 == None:
            print ("n2 - Define Verses 2 chord Progresion (undefined!)")
        else:
            print ("n2 - Define Verses 2 chord Progresion")
        if cprogCH == None:
            print ("ch - Define Chorus/Bridge chord Progresion (undefined!)")
        else:
            print ("ch - Define Chorus/Bridge chord Progresion")
        print ("Qq - Quit")
        inp = input(">")
        if inp in "n1":
            prog = makeProgMenu(pal)
            if prog == None:
                prog = False
            else:
                return ("n1", prog)
        elif inp in "n2":
            prog = makeProgMenu(pal)
            if prog == None:
                prog = False
            else:
                return ("n2", prog)   
        elif inp in "ch":
            prog = makeProgMenu(pal)
            if prog == None:
                prog = False
            else:
                print("DEBUG: returning ch",prog)
                return ("ch", prog)   
        elif inp in "Qq":
            return False
        
        
def makeProgMenu(pal): # Request progression generation, returns None if failed
    progsize = pal._progsize
    prog = [] # list of chord3
    for i in range(progsize):
        prog = prog + ["<UNDEFINED>"]
    while True:
        string = ""
        for chord in prog:
            string = string + str(chord) + " "
        print("Your progression:")
        print(string)
        print("Dd - Define chords")
        print("Vv - Generate Progression with default verses weights")
        print("Cc - Generate Progression with default chorus weights")
        print("Gg - Generate Progression with custom weights")
        print("Ss - Show in piano")
        print("Pp - Preview")
        print("Ff - Use Progression as is")
        print("Qq - Quit")
        inp = input(">")
        if inp in "Dd":
            print("Requesting id in range [0-"+str(progsize-1)+"]")
            cid = idMenu()
            if cid in range(progsize):
                print("Defining chord "+str(cid))
                chord = chordMenu(pal._scale)
                if chord != None:
                    print("Chord defined!")
                    prog[cid] = chord
            else:
                print("Invalid id: " + str(cid))
        elif inp in "Vv":
            prog = list(pal._scale.makeProg(progsize, musictheory.n1ChWeights()[0], musictheory.n1ChWeights()[1]))
        elif inp in "Cc":
            prog = list(pal._scale.makeProg(progsize, musictheory.chChWeights()[0], musictheory.chChWeights()[1])) #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX FINISH ME
        elif inp in "Gg":
            raise ValueError("pooop")
        elif inp in "Ss":
            for c in prog:
                if c == "<UNDEFINED>":
                    pianoprinter.octoPrint([])
                else:
                    pianoprinter.octoPrint(c._types)
        elif inp in "Pp":
            previewProg(prog)
        elif inp in "Ff":
            return prog
        elif inp in "Qq":
            return None
        
        
                    
def idMenu(): # Request int id, return None if failed
    while True:
        print("Please input id: (Qq-quit)")
        inp = input(">")
        flag = True
        if inp in "Qq":
            return None
        for i in inp:
            if not i in "0123456789":
                flag = False
        if flag:
            return eval(inp)
        
def chordMenu(scale): # Request chord3 generation, return None if failed
    while True:
        print("Defining chord in scale: "+str(scale))
        print("Input list of 3 notes, separated by spaces")
        print("Input first note in chord")
        print("Rr - Generate")
        print("Aa - Generate with restraints")
        print("Ii - Scale info")
        print("Qq - Quit")
        inp = input(">")
        if inp in "Rr":
            chord = musictheory.chord3.fromScale(scale)
            pianoprinter.octoPrint(chord._types)
            while True:
                print(str(chord)+", accept? Yy Nn")
                inp2 = input(">")
                if inp2 in "Yy":
                    return chord
                elif inp2 in "Nn":
                    break
        elif inp in "Aa":
            print("Input restraint 1 (leave empty for NONE)")
            res1 = input(">")
            if res1 == "":
                res1 = None
            print("Input restraint 2 (leave empty for NONE)")
            res2 = input(">")
            if res2 == "":
                res2 = None
            chord = rselect(scale.getChords(res1, res2))
            pianoprinter.octoPrint(chord._types)
            while True:
                print(str(chord)+", accept? Yy Nn")
                inp2 = input(">")
                if inp2 in "Yy":
                    return chord
                elif inp2 in "Nn":
                    break
        elif inp in "Ii":
            print ("Your scale: "+str(scale)[2:-2])
            pianoprinter.octoPrint(scale._notes)
            print("Chords |Short  |Normal |Large  ")
            print("Minor  |" + str(len(scale.getChords("minor", "short"))) + "      |" + str(len(scale.getChords("minor", "normal"))) + "      |" + str(len(scale.getChords("minor", "large"))) + "      ")
            print("Weird  |" + str(len(scale.getChords("weird", "short"))) + "      |" + str(len(scale.getChords("weird", "normal"))) + "      |" + str(len(scale.getChords("weird", "large"))) + "      ")
            print("Major  |" + str(len(scale.getChords("major", "short"))) + "      |" + str(len(scale.getChords("major", "normal"))) + "      |" + str(len(scale.getChords("major", "large"))) + "      ")
        elif inp in "Qq":
            return None
        else:
            notenames = str.split(inp, " ")
            notes = ()
            for i in range(len(notenames)):
                if len(notenames[i]) != 0:
                    notes = notes + (musictheory.mnote.fromName(notenames[i] + "0"),)
            if len(notes) == 1:
                for i in scale.getChords():
                    if i._types[0]._type == notes[0]._type:
                        chord = i
                        break
                pianoprinter.octoPrint(chord._types)
                while True:
                    print(str(chord)+", accept? Yy Nn")
                    inp2 = input(">")
                    if inp2 in "Yy":
                        return chord
                    elif inp2 in "Nn":
                        break
                
            elif len(notes) == 3:
                chord = musictheory.chord3(notes)
                pianoprinter.octoPrint(chord._types)
                while True:
                    print(str(chord)+", accept? Yy Nn")
                    inp2 = input(">")
                    if inp2 in "Yy":
                        return chord
                    elif inp2 in "Nn":
                        break
    
        
            
mainMenu()
