import pyphen

dic=pyphen.Pyphen(lang="pl_PL")

def right_length(message):
    return count_syllables(message)==(5+7+5)

def count_syllables(message):
    words=message.replace("\t","").split(" ")
    count=0
    for word in words:
        count+=len(dic.inserted(word).split("-"))
    return count

def is_haiku(message):
    if(not right_length(message)):
        return False
    syl=(5,7,5)
    words=message.replace("\t","").split(" ")
    lines=[[],[],[]]
    line=0
    syl_count=0
    for word in words:
        syl_count+=count_syllables(word)
        print(word,dic.inserted(word),count_syllables(word),syl_count,line)
        if(syl_count<syl[line]):
            lines[line].append(word)
        elif(syl_count==syl[line]):         
            lines[line].append(word)
            syl_count=0
            line+=1
        elif(syl_count>syl[line]):
            return False
    return lines
    pass



def haikufy(message):
    haiku= is_haiku(message)
    out=""
    if(haiku):
        for line in haiku:
            out+=" ".join(line)
            out+="\n"
        return out
    return False
'''
print(haikufy("w zupełnej ciszy trzepot motylich skrzydeł rozkrusza skałę"))
print(haikufy("kamienny Budda - uczę się wybaczać komarowi"))
print(haikufy("koniec alei z ramion staruszka opadają liście"))
print(haikufy("przydrożny rów pod cienką warstwą lodu pierwsze kaczeńce"))
print(haikufy("cały dzień pracy na ogrodowej grządce krecie kopczyki"))
print(haikufy("ucieczka z miasta po obu stronach grobli żabie stereo"))
print(haikufy("pęk koniczyny w małej dłoni dziewczynki końskie chrapy"))
print(haikufy("sępy tych dolin to nie milczące ptaki lecz zwykli ludzie"))
print(haikufy("moje łydki są ranione przez te kosze na nasze torby"))
print(haikufy("po upalnym dniu jakież wytchnienie niesie noc pełna rosy"))
'''