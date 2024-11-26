import sys
import os
import pathlib
def split_string(string, n):
    return string[:n], string[n:]
def sign(num):
    c = 0
    if num > 127:
        var = 7
        while var >= 0:
            if num&2**var != 0:
                if var == 7:
                    c -= 2**var
                else:
                    c += 2**var
            var -= 1
    else:
        var = 7
        while var >= 0:
            if num&2**var != 0:
                c += 2**var
            var -= 1
    if num == 0:
        c = 0
    return c
file = open(sys.argv[1], "rb")
file = file.read()
if file[0:4] != b'NES\x1a':
    print("Not a valid INES file.")
    sys.exit()
prgBanks = int.from_bytes(file[4:5])
chrBanks = int.from_bytes(file[5:6])
if os.path.getsize(sys.argv[1]) != (prgBanks * 16384) + (chrBanks * 8192) + 16:
    print("Expected Size: " + str((prgBanks * 16384) + (chrBanks * 8192) + 16))
    print("Actual Size: " + str(os.path.getsize(sys.argv[1])))
if int.from_bytes(file[6:7]) >= 16:
    print("Mappers not supported.")
    sys.exit()
if file[7:16] != b'\x00\x00\x00\x00\x00\x00\x00\x00\x00':
    print("Mappers and NES 2.0 not supported, remove junk in bytes 7-15.")
    sys.exit()
instructions = ['BRK impl', 'ORA X,ind', 'ORA zpg', 'ASL zpg', 'PHP impl', 'ORA #', 'ASL A', 'ORA abs', 'ASL abs', 'BPL rel', 'ORA ind,Y', 'ORA zpg,X', 'ASL zpg,X', 'CLC impl', 'ORA abs,Y', 'ORA abs,X', 'ASL abs,X', 'JSR abs', 'AND X,ind', 'BIT zpg', 'AND zpg', 'ROL zpg', 'PLP impl', 'AND #', 'ROL A', 'BIT abs', 'AND abs', 'ROL abs', 'BMI rel', 'AND ind,Y', 'AND zpg,X', 'ROL zpg,X', 'SEC impl', 'AND abs,Y', 'AND abs,X', 'ROL abs,X', 'RTI impl', 'EOR X,ind', 'EOR zpg', 'LSR zpg', 'PHA impl', 'EOR #', 'LSR A', 'JMP abs', 'EOR abs', 'LSR abs', 'BVC rel', 'EOR ind,Y', 'EOR zpg,X', 'LSR zpg,X', 'CLI impl', 'EOR abs,Y', 'EOR abs,X', 'LSR abs,X', 'RTS impl', 'ADC X,ind', 'ADC zpg', 'ROR zpg', 'PLA impl', 'ADC #', 'ROR A', 'JMP ind', 'ADC abs', 'ROR abs', 'BVS rel', 'ADC ind,Y', 'ADC zpg,X', 'ROR zpg,X', 'SEI impl', 'ADC abs,Y', 'ADC abs,X', 'ROR abs,X', 'STA X,ind', 'STY zpg', 'STA zpg', 'STX zpg', 'DEY impl', 'TXA impl', 'STY abs', 'STA abs', 'STX abs', 'BCC rel', 'STA ind,Y', 'STY zpg,X', 'STA zpg,X', 'STX zpg,Y', 'TYA impl', 'STA abs,Y', 'TXS impl', 'STA abs,X', 'LDY #', 'LDA X,ind', 'LDX #', 'LDY zpg', 'LDA zpg', 'LDX zpg', 'TAY impl', 'LDA #', 'TAX impl', 'LDY abs', 'LDA abs', 'LDX abs', 'BCS rel', 'LDA ind,Y', 'LDY zpg,X', 'LDA zpg,X', 'LDX zpg,Y', 'CLV impl', 'LDA abs,Y', 'TSX impl', 'LDY abs,X', 'LDA abs,X', 'LDX abs,Y', 'CPY #', 'CMP X,ind', 'CPY zpg', 'CMP zpg', 'DEC zpg', 'INY impl', 'CMP #', 'DEX impl', 'CPY abs', 'CMP abs', 'DEC abs', 'BNE rel', 'CMP ind,Y', 'CMP zpg,X', 'DEC zpg,X', 'CLD impl', 'CMP abs,Y', 'CMP abs,X', 'DEC abs,X', 'CPX #', 'SBC X,ind', 'CPX zpg', 'SBC zpg', 'INC zpg', 'INX impl', 'SBC #', 'NOP impl', 'CPX abs', 'SBC abs', 'INC abs', 'BEQ rel', 'SBC ind,Y', 'SBC zpg,X', 'INC zpg,X', 'SED impl', 'SBC abs,Y', 'SBC abs,X', 'INC abs,X'] 
bytes = [0, 1, 5, 6, 8, 9, 10, 13, 14, 16, 17, 21, 22, 24, 25, 29, 30, 32, 33, 36, 37, 38, 40, 41, 42, 44, 45, 46, 48, 49, 53, 54, 56, 57, 61, 62, 64, 65, 69, 70, 72, 73, 74, 76, 77, 78, 80, 81, 85, 86, 88, 89, 93, 94, 96, 97, 101, 102, 104, 105, 106, 108, 109, 110, 112, 113, 117, 118, 120, 121, 125, 126, 129, 132, 133, 134, 136, 138, 140, 141, 142, 144, 145, 148, 149, 150, 152, 153, 154, 157, 160, 161, 162, 164, 165, 166, 168, 169, 170, 172, 173, 174, 176, 177, 180, 181, 182, 184, 185, 186, 188, 189, 190, 192, 193, 196, 197, 198, 200, 201, 202, 204, 205, 206, 208, 209, 213, 214, 216, 217, 221, 222, 224, 225, 228, 229, 230, 232, 233, 234, 236, 237, 238, 240, 241, 245, 246, 248, 249, 253, 254]
bytesArr = []
asm = []
file = []
if os.path.getsize(sys.argv[1]) == 24592:
    start = int("c000", 16)
elif os.path.getsize(sys.argv[1]) == 40976:
    start = int("8000", 16)
count = 0
while count < int("8000", 16):
    bytesArr.append(0)
    count += 1
count = 0
for byte in pathlib.Path(sys.argv[1]).read_bytes():
    if count >= 16 and count < os.path.getsize(sys.argv[1]) - 8192:
        bytesArr.append(byte)
    count += 1
count = 0
for byte in pathlib.Path(sys.argv[1]).read_bytes():
    if count >= 16 and count < os.path.getsize(sys.argv[1]) - 8192:
        bytesArr.append(byte)
    count += 1
def disassemble():
    fileBytes = start
    while fileBytes < len(bytesArr):
        if bytesArr[fileBytes] < 16: 
            instruction = ".byte $0" + hex(bytesArr[fileBytes]).replace("0x", "") 
        else: 
            instruction = ".byte $" + hex(bytesArr[fileBytes]).replace("0x", "") 
        highByte = ""
        lowByte = ""
        try:
            for byte in range(len(bytes)): 
                if bytes[byte] == bytesArr[fileBytes]: 
                    if " A" in instructions[byte]: 
                        instruction = instructions[byte].split(" A")[0] 
                    elif " abs" in instructions[byte] and "," not in instructions[byte]: 
                        instruction = instructions[byte].split(" abs")[0] 
                        highByte = bytesArr[fileBytes + 2] 
                        if highByte < 16: 
                            highByte = "0" + hex(highByte).replace("0x", "") 
                        else: 
                            highByte = hex(highByte).replace("0x", "") 
                        lowByte = bytesArr[fileBytes + 1]
                        if lowByte < 16: 
                            lowByte = "0" + hex(lowByte).replace("0x", "") 
                        else: 
                            lowByte = hex(lowByte).replace("0x", "") 
                        instruction = instruction + " $" + highByte + lowByte 
                        fileBytes += 2
                    elif " abs,X" in instructions[byte]: 
                        instruction = instructions[byte].split(" abs,X")[0] 
                        highByte = bytesArr[fileBytes + 2] 
                        if highByte < 16: 
                            highByte = "0" + hex(highByte).replace("0x", "") 
                        else: 
                            highByte = hex(highByte).replace("0x", "") 
                        lowByte = bytesArr[fileBytes + 1]
                        if lowByte < 16: 
                            lowByte = "0" + hex(lowByte).replace("0x", "") 
                        else: 
                            lowByte = hex(lowByte).replace("0x", "") 
                        instruction = instruction + " $" + highByte + lowByte + ",X" 
                        fileBytes += 2
                    elif " abs,Y" in instructions[byte]: 
                        instruction = instructions[byte].split(" abs,Y")[0] 
                        highByte = bytesArr[fileBytes + 2] 
                        if highByte < 16: 
                            highByte = "0" + hex(highByte).replace("0x", "") 
                        else: 
                            highByte = hex(highByte).replace("0x", "") 
                        lowByte = bytesArr[fileBytes + 1]
                        if lowByte < 16: 
                            lowByte = "0" + hex(lowByte).replace("0x", "") 
                        else: 
                            lowByte = hex(lowByte).replace("0x", "") 
                        instruction = instruction + " $" + highByte + lowByte + ",Y"
                        fileBytes += 2 
                    elif " #" in instructions[byte]: 
                        instruction = instructions[byte].split(" #")[0] 
                        highByte = bytesArr[fileBytes + 1] 
                        if highByte < 16: 
                            highByte = "0" + hex(highByte).replace("0x", "") 
                        else: 
                            highByte = hex(highByte).replace("0x", "") 
                        instruction = instruction + " #$" + highByte 
                        fileBytes += 1 
                    elif " impl" in instructions[byte]: 
                        instruction = instructions[byte].split(" impl")[0] 
                    elif " ind" in instructions[byte] and "," not in instructions[byte]: 
                        instruction = instructions[byte].split(" ind")[0] 
                        highByte = bytesArr[fileBytes + 2] 
                        if highByte < 16: 
                            highByte = "0" + hex(highByte).replace("0x", "") 
                        else: 
                            highByte = hex(highByte).replace("0x", "") 
                        lowByte = bytesArr[fileBytes + 1]
                        if lowByte < 16: 
                            lowByte = "0" + hex(lowByte).replace("0x", "") 
                        else: 
                            lowByte = hex(lowByte).replace("0x", "") 
                        instruction = instruction + " ($" + highByte + lowByte + ")"
                        fileBytes += 2 
                    elif " X,ind" in instructions[byte]: 
                        instruction = instructions[byte].split(" X,ind")[0] 
                        highByte = bytesArr[fileBytes + 1] 
                        if highByte < 16: 
                            highByte = "0" + hex(highByte).replace("0x", "") 
                        else: 
                            highByte = hex(highByte).replace("0x", "") 
                        instruction = instruction + " ($" + highByte + ",X)" 
                        fileBytes += 1 
                    elif " ind,Y" in instructions[byte]: 
                        instruction = instructions[byte].split(" ind,Y")[0] 
                        highByte = bytesArr[fileBytes + 1] 
                        if highByte < 16: 
                            highByte = "0" + hex(highByte).replace("0x", "") 
                        else: 
                            highByte = hex(highByte).replace("0x", "") 
                        instruction = instruction + " ($" + highByte + "),Y" 
                        fileBytes += 1 
                    elif " rel" in instructions[byte]: 
                        instruction = instructions[byte].split(" rel")[0]  
                        highByte = bytesArr[fileBytes + 1] 
                        if highByte > 127:
                            highByte = hex(fileBytes + 1 - (255 - highByte)).replace("0x", "") 
                        else: 
                            highByte = hex(fileBytes + highByte + 2).replace("0x", "") 
                        if int(highByte, 16) < 16:
                            highByte = "000" + highByte
                        elif int(highByte, 16) < 256:
                            highByte = "00" + highByte
                        elif int(highByte, 16) < 4096:
                            highByte = "0" + highByte
                        instruction = instruction + " $" + highByte 
                        highByte = hex(bytesArr[fileBytes + 1]).replace("0x", "")
                        fileBytes += 1
                    elif " zpg" in instructions[byte] and "," not in instructions[byte]: 
                        instruction = instructions[byte].split(" zpg")[0] 
                        highByte = bytesArr[fileBytes + 1] 
                        if highByte < 16: 
                            highByte = "0" + hex(highByte).replace("0x", "") 
                        else: 
                            highByte = hex(highByte).replace("0x", "") 
                        instruction = instruction + " $" + highByte 
                        fileBytes += 1 
                    elif " zpg,X" in instructions[byte]: 
                        instruction = instructions[byte].split(" zpg,X")[0] 
                        highByte = bytesArr[fileBytes + 1] 
                        if highByte < 16: 
                            highByte = "0" + hex(highByte).replace("0x", "") 
                        else: 
                            highByte = hex(highByte).replace("0x", "") 
                        instruction = instruction + " $" + highByte + ",X" 
                        fileBytes += 1 
                    elif " zpg,Y" in instructions[byte]: 
                        instruction = instructions[byte].split(" zpg,Y")[0] 
                        highByte = bytesArr[fileBytes + 1] 
                        if highByte < 16: 
                            highByte = "0" + hex(highByte).replace("0x", "") 
                        else: 
                            highByte = hex(highByte).replace("0x", "") 
                        instruction = instruction + " $" + highByte + ",Y" 
                        fileBytes += 1 
                    break
        except:
            if bytesArr[fileBytes] < 16: 
                instruction = ".byte $0" + hex(bytesArr[fileBytes]).replace("0x", "") 
            else: 
                instruction = ".byte $" + hex(bytesArr[fileBytes]).replace("0x", "")
        asm.append(instruction)
        if highByte != "" and lowByte == "":
            file.append(len(asm) - 1) 
            file.append(len(asm) - 1)  
        elif highByte != "" and lowByte != "":
            file.append(len(asm) - 1)
            file.append(len(asm) - 1)
            file.append(len(asm) - 1)
        elif highByte == "" and lowByte == "":
            file.append(len(asm) - 1)
        fileBytes += 1
running = True
ins = 0
test = 0
testFile = open("test.log", "r")
pc2 = []
sp2 = []
ac2 = []
xr2 = []
yr2 = []
sr2 = []
cyc2 = []
s = []
while True:
    line = testFile.readline()
    if not line:
        break
    line = line.replace("\\n", "").replace("\n", "")
    pc = line.split()[0]
    ac = line.split("A:")[1].split()[0]
    xr = line.split("X:")[1].split()[0]
    yr = line.split("Y:")[1].split()[0]
    sr = line.split("P:")[1].split()[0]
    sp = line.split("SP:")[1].split()[0]
    cyc = line.split("CYC:")[1].split()[0]
    pc2.append(int(pc, 16))
    ac2.append(int(ac, 16))
    xr2.append(int(xr, 16))
    yr2.append(int(yr, 16))
    sr2.append(int(sr, 16))
    sp2.append(int(sp, 16))
    cyc2.append(int(cyc))
testFile.close()
pc = start
sp = 253
ac = 0
xr = 0
yr = 0
sr = 36
cyc = 7
disassemble()
while running:
    flag = False
    if pc != pc2[test]:
        print("Expected PC: " + hex(pc2[test]))
        print("Actual PC: " + hex(pc))
        break
    if sp != sp2[test]:
        print("Expected SP: " + hex(sp2[test]))
        print("Actual SP: " + hex(sp))
        break
    if ac != ac2[test]:
        print("Expected AC: " + hex(ac2[test]))
        print("Actual AC: " + hex(ac))
        break
    if xr != xr2[test]:
        print("Expected XR: " + hex(xr2[test]))
        print("Actual XR: " + hex(xr))
        break
    if yr != yr2[test]:
        print("Expected YR: " + hex(yr2[test]))
        print("Actual YR: " + hex(yr))
        break
    if sr != sr2[test]:
        print("Expected SR: " + hex(sr2[test]))
        print("Actual SR: " + hex(sr))
        break
    if cyc != cyc2[test]:
        print("Expected CYC: " + hex(cyc2[test]))
        print("Actual CYC: " + hex(cyc))
        break
    if "JMP $" in asm[file[ins]]:
        pc = int(asm[file[ins]].split("$")[1], 16)
        length = 0
        cyc += 3
        flag = True
    elif "LDX #$" in asm[file[ins]]:
        xr = int(asm[file[ins]].split("$")[1], 16)
        if xr == 0:
            if sr&2**1 == 0:
                sr += 2**1
        else:
            if sr&2**1 != 0:
                sr -= 2**1
        if xr&2**7 != 0:
            if sr&2**7 == 0:
                sr += 2**7
        else:
            if sr&2**7 != 0:
                sr -= 2**7
        length = 2
        cyc += 2
        flag = True
    elif "STX $" in asm[file[ins]] and "," not in asm[file[ins]] and len(asm[file[ins]].split("$")[1]) == 2:
        m = int(asm[file[ins]].split("$")[1], 16)
        bytesArr[m] = xr
        length = 2
        cyc += 3
        flag = True
    elif "JSR $" in asm[file[ins]]:
        s.append(pc + 3)
        pc = int(asm[file[ins]].split("$")[1], 16)
        length = 0
        sp -= 2
        cyc += 6
        flag = True
    elif "NOP" in asm[file[ins]]:
        length = 1
        cyc += 2
        flag = True
    elif "SEC" in asm[file[ins]]:
        if sr&2**0 == 0:
            sr += 2**0
        length = 1
        cyc += 2
        flag = True
    elif "BCS $" in asm[file[ins]]:
        var1 = split_string(hex(pc).replace("0x", ""), 2)[0]
        var2 = split_string(hex(int(asm[file[ins]].split("$")[1], 16)).replace("0x", ""), 2)[0]
        if sr&2**0 != 0:
            pc = int(asm[file[ins]].split("$")[1], 16)
            length = 0
            cyc += 1
            if var1 != var2:
                cyc += 2
        else:
            length = 2
        cyc += 2
        flag = True
    elif "CLC" in asm[file[ins]]:
        if sr&2**0 != 0:
            sr -= 2**0
        length = 1
        cyc += 2
        flag = True
    elif "BCC $" in asm[file[ins]]:
        var1 = split_string(hex(pc).replace("0x", ""), 2)[0]
        var2 = split_string(hex(int(asm[file[ins]].split("$")[1], 16)).replace("0x", ""), 2)[0]
        if sr&2**0 == 0:
            pc = int(asm[file[ins]].split("$")[1], 16)
            length = 0
            cyc += 1
            if var1 != var2:
                cyc += 2
        else:
            length = 2
        cyc += 2
        flag = True
    elif "LDA #$" in asm[file[ins]]:
        ac = int(asm[file[ins]].split("$")[1], 16)
        if ac == 0:
            if sr&2**1 == 0:
                sr += 2**1
        else:
            if sr&2**1 != 0:
                sr -= 2**1
        if ac&2**7 != 0:
            if sr&2**7 == 0:
                sr += 2**7
        else:
            if sr&2**7 != 0:
                sr -= 2**7
        length = 2
        cyc += 2
        flag = True
    elif "BEQ $" in asm[file[ins]]:
        var1 = split_string(hex(pc).replace("0x", ""), 2)[0]
        var2 = split_string(hex(int(asm[file[ins]].split("$")[1], 16)).replace("0x", ""), 2)[0]
        if sr&2**1 != 0:
            pc = int(asm[file[ins]].split("$")[1], 16)
            length = 0
            cyc += 1
            if var1 != var2:
                cyc += 2
        else:
            length = 2
        cyc += 2
        flag = True
    elif "BNE $" in asm[file[ins]]:
        var1 = split_string(hex(pc).replace("0x", ""), 2)[0]
        var2 = split_string(hex(int(asm[file[ins]].split("$")[1], 16)).replace("0x", ""), 2)[0]
        if sr&2**1 == 0:
            pc = int(asm[file[ins]].split("$")[1], 16)
            length = 0
            cyc += 1
            if var1 != var2:
                cyc += 2
        else:
            length = 2
        cyc += 2
        flag = True
    elif "STA $" in asm[file[ins]] and "," not in asm[file[ins]] and len(asm[file[ins]].split("$")[1]) == 2:
        m = int(asm[file[ins]].split("$")[1], 16)
        bytesArr[m] = ac
        length = 2
        cyc += 3
        flag = True
    elif "BIT $" in asm[file[ins]] and len(asm[file[ins]].split("$")[1]) == 2:
        bool = True
        m = int(asm[file[ins]].split("$")[1], 16)
        var = 7
        while var >= 0:
            if bytesArr[m]&2**var == ac&2**var and ac&2**var != 0:
                bool = False
                break
            var -= 1
        if bool == True:
            if sr&2**1 == 0:
                sr += 2**1
        else:
            if sr&2**1 != 0:
                sr -= 2**1
        if sr&2**6 == 0:
            if bytesArr[m]&2**6 != 0:
                sr += 2**6
        else:
            if bytesArr[m]&2**6 == 0:
                sr -= 2**6
        if sr&2**7 == 0:
            if bytesArr[m]&2**7 != 0:
                sr += 2**7
        else:
            if bytesArr[m]&2**7 == 0:
                sr -= 2**7
        length = 2
        cyc += 3
        flag = True
    elif "BVS $" in asm[file[ins]]:
        var1 = split_string(hex(pc).replace("0x", ""), 2)[0]
        var2 = split_string(hex(int(asm[file[ins]].split("$")[1], 16)).replace("0x", ""), 2)[0]
        if sr&2**6 != 0:
            pc = int(asm[file[ins]].split("$")[1], 16)
            length = 0
            cyc += 1
            if var1 != var2:
                cyc += 2
        else:
            length = 2
        cyc += 2
        flag = True
    elif "BVC $" in asm[file[ins]]:
        var1 = split_string(hex(pc).replace("0x", ""), 2)[0]
        var2 = split_string(hex(int(asm[file[ins]].split("$")[1], 16)).replace("0x", ""), 2)[0]
        if sr&2**6 == 0:
            pc = int(asm[file[ins]].split("$")[1], 16)
            length = 0
            cyc += 1
            if var1 != var2:
                cyc += 2
        else:
            length = 2
        cyc += 2
        flag = True
    elif "BPL $" in asm[file[ins]]:
        var1 = split_string(hex(pc).replace("0x", ""), 2)[0]
        var2 = split_string(hex(int(asm[file[ins]].split("$")[1], 16)).replace("0x", ""), 2)[0]
        if sr&2**7 == 0:
            pc = int(asm[file[ins]].split("$")[1], 16)
            length = 0
            cyc += 1
            if var1 != var2:
                cyc += 2
        else:
            length = 2
        cyc += 2
        flag = True
    elif "RTS" in asm[file[ins]]:
        pc = s[len(s) - 1]
        s.pop(len(s) - 1)
        length = 0
        sp += 2
        cyc += 6
        flag = True
    elif "SEI" in asm[file[ins]]:
        if sr&2**2 == 0:
            sr += 2**2
        length = 1
        cyc += 2
        flag = True
    elif "SED" in asm[file[ins]]:
        if sr&2**3 == 0:
            sr += 2**3
        length = 1
        cyc += 2
        flag = True
    elif "PHP" in asm[file[ins]]:
        oldPC = sr
        if oldPC&2**4 == 0:
            oldPC += 2**4
        sp -= 1
        length = 1
        cyc += 3
        flag = True
    elif "PLA" in asm[file[ins]]:
        ac = oldPC
        if ac == 0:
            if sr&2**1 == 0:
                sr += 2**1
        else:
            if sr&2**1 != 0:
                sr -= 2**1
        if ac&2**7 != 0:
            if sr&2**7 == 0:
                sr += 2**7
        else:
            if sr&2**7 != 0:
                sr -= 2**7
        length = 1
        sp += 1
        cyc += 4
        flag = True
    elif "AND #$" in asm[file[ins]]:
        oldAC = 0
        oper = int(asm[file[ins]].split("$")[1], 16)
        var = 7
        while var >= 0:
            if oper&2**var == ac&2**var:
                oldAC += 2**var
            var -= 1
        ac = oldAC
        if ac == 0:
            if sr&2**1 == 0:
                sr += 2**1
        if ac&2**7 != 0:
            if sr&2**7 == 0:
                sr += 2**7
        length = 2
        cyc += 2
        flag = True
    elif "CMP #$" in asm[file[ins]]:
        oper = int(asm[file[ins]].split("$")[1], 16)
        if ac >= oper:
            if sr&2**0 == 0:
                sr += 2**0
        else:
            if sr&2**0 != 0:
                sr -= 2**0
        if ac == oper:
            if sr&2**1 == 0:
                sr += 2**1
        else:
            if sr&2**1 != 0:
                sr -= 2**1
        oper = ac - oper
        if oper&2**7 != 0:
            if sr&2**7 == 0:
                sr += 2**7
        else:
            if sr&2**7 != 0:
                sr -= 2**7
        length = 2
        cyc += 2
        flag = True
    elif "CLD" in asm[file[ins]]:
        if sr&2**3 != 0:
            sr -= 2**3
        length = 1
        cyc += 2
        flag = True
    elif "PHA" in asm[file[ins]]:
        oldPC = ac
        sp -= 1
        length = 1
        cyc += 3
        flag = True
    elif "PLP" in asm[file[ins]]:
        sr = oldPC
        if sr&2**4 != 0:
            sr -= 2**4
        if sr&2**5 == 0:
            sr += 2**5
        sp += 1
        length = 1
        cyc += 4
        flag = True
    elif "BMI" in asm[file[ins]]:
        var1 = split_string(hex(pc).replace("0x", ""), 2)[0]
        var2 = split_string(hex(int(asm[file[ins]].split("$")[1], 16)).replace("0x", ""), 2)[0]
        if sr&2**7 != 0:
            pc = int(asm[file[ins]].split("$")[1], 16)
            length = 0
            cyc += 1
            if var1 != var2:
                cyc += 2
        else:
            length = 2
        cyc += 2
        flag = True
    elif "ORA #$" in asm[file[ins]]:
        oldAC = 0
        var = 7
        m = int(asm[file[ins]].split("$")[1], 16)
        bool = False
        while var >= 0:
            if m&2**var != ac&2**var:
                if var == 7:
                    if sr&2**7 == 0:
                        sr += 2**7
                oldAC += 2**var
                bool = True
            var -= 1
        ac = oldAC
        if bool == False:
            if sr&2**1 == 0:
                sr += 2**1
        length = 2
        cyc += 2
        flag = True
    elif "CLV" in asm[file[ins]]:
        if sr&2**6 != 0:
            sr -= 2**6
        length = 1
        cyc += 2
        flag = True
    elif "EOR #$" in asm[file[ins]]:
        oldAC = 0
        var = 7
        m = int(asm[file[ins]].split("$")[1], 16)
        bool = False
        while var >= 0:
            if m&2**var != ac&2**var:
                if var == 7:
                    if sr&2**7 == 0:
                        sr += 2**7
                oldAC += 2**var
                bool = True
            var -= 1
        ac = oldAC
        if bool == False:
            if sr&2**1 == 0:
                sr += 2**1
        length = 2
        cyc += 2
        flag = True
    elif "ADC #$" in asm[file[ins]]:
        oper = int(asm[file[ins]].split("$")[1], 16)
        c = sr&2**0
        newAC = ac + oper + c
        if newAC > 255:
            if sr&2**0 == 0:
                sr += 2**0
        else:
            if sr&2**0 != 0:
                sr -= 2**0
        acS = sign(ac)
        oper2 = sign(oper)
        oldAC = sign(newAC)
        if acS < 0:
            acS = 1
        else:
            acS = 0
        if oper2 < 0:
            oper2 = 1
        else:
            oper2 = 0
        if oldAC < 0:
            oldAC = 1
        else:
            oldAC = 0
        if oldAC != acS and acS == oper2:
            if sr&2**6 == 0:
                sr += 2**6
        else:
            if sr&2**6 != 0:
                sr -= 2**6
        if newAC == 0 or newAC == 256:
            if sr&2**1 == 0:
                sr += 2**1
        else:
            if sr&2**1 != 0:
                sr -= 2**1
        if newAC&2**7 != 0:
            if sr&2**7 == 0:
                sr += 2**7
        ac = newAC
        if ac > 255:
            ac -= 256
        length = 2
        cyc += 2
        flag = True
    elif "LDY #$" in asm[file[ins]]:
        yr = int(asm[file[ins]].split("$")[1], 16)
        if yr == 0:
            if sr&2**1 == 0:
                sr += 2**1
        else:
            if sr&2**1 != 0:
                sr -= 2**1
        if yr&2**7 != 0:
            if sr&2**7 == 0:
                sr += 2**7
        else:
            if sr&2**7 != 0:
                sr -= 2**7
        length = 2
        cyc += 2
        flag = True
    elif "CPY #$" in asm[file[ins]]:
        oper = int(asm[file[ins]].split("$")[1], 16)
        if yr >= oper:
            if sr&2**0 == 0:
                sr += 2**0
        else:
            if sr&2**0 != 0:
                sr -= 2**0
        if yr == oper:
            if sr&2**1 == 0:
                sr += 2**1
        else:
            if sr&2**1 != 0:
                sr -= 2**1
        oper = yr - oper
        if oper&2**7 != 0:
            if sr&2**7 == 0:
                sr += 2**7
        else:
            if sr&2**7 != 0:
                sr -= 2**7
        length = 2
        cyc += 2
        flag = True
    elif "CPX #$" in asm[file[ins]]:
        oper = int(asm[file[ins]].split("$")[1], 16)
        if xr >= oper:
            if sr&2**0 == 0:
                sr += 2**0
        else:
            if sr&2**0 != 0:
                sr -= 2**0
        if xr == oper:
            if sr&2**1 == 0:
                sr += 2**1
        else:
            if sr&2**1 != 0:
                sr -= 2**1
        oper = xr - oper
        if oper&2**7 != 0:
            if sr&2**7 == 0:
                sr += 2**7
        else:
            if sr&2**7 != 0:
                sr -= 2**7
        length = 2
        cyc += 2
        flag = True
    elif "SBC #$" in asm[file[ins]]:
        oper = int(asm[file[ins]].split("$")[1], 16)
        c = sr&2**0
        newAC = ac - oper - (1 - c)
        if newAC < 0:
            if sr&2**0 != 0:
                sr -= 2**0
            newAC += 256
        else:
            if sr&2**0 == 0:
                sr += 2**0
        acS = sign(ac)
        oper2 = sign(oper - (1 - c))
        oldAC = sign(newAC)
        if acS - oper2 != oldAC:
            if sr&2**6 == 0:
                sr += 2**6
        else:
            if sr&2**6 != 0:
                sr -= 2**6
        if newAC == 0 or newAC == -256:
            if sr&2**1 == 0:
                sr += 2**1
        else:
            if sr&2**1 != 0:
                sr -= 2**1
        if newAC&2**7 != 0:
            if sr&2**7 == 0:
                sr += 2**7
        else:
            if sr&2**7 != 0:
                sr -= 2**7
        ac = newAC
        length = 2
        cyc += 2
        flag = True
    elif "INY" in asm[file[ins]]:
        yr += 1
        if yr == 256:
            yr = 0
        if yr == 0:
            if sr&2**1 == 0:
                sr += 2**1
        else:
            if sr&2**1 != 0:
                sr -= 2**1
        if yr&2**7 != 0:
            if sr&2**7 == 0:
                sr += 2**7
        else:
            if sr&2**7 != 0:
                sr -= 2**7
        length = 1
        cyc += 2
        flag = True
    elif "INX" in asm[file[ins]]:
        xr += 1
        if xr == 256:
            xr = 0
        if xr == 0:
            if sr&2**1 == 0:
                sr += 2**1
        else:
            if sr&2**1 != 0:
                sr -= 2**1
        if xr&2**7 != 0:
            if sr&2**7 == 0:
                sr += 2**7
        else:
            if sr&2**7 != 0:
                sr -= 2**7
        length = 1
        cyc += 2
        flag = True
    elif "DEY" in asm[file[ins]]:
        yr -= 1
        if yr == -1:
            yr = 255
        if yr == 0:
            if sr&2**1 == 0:
                sr += 2**1
        else:
            if sr&2**1 != 0:
                sr -= 2**1
        if yr&2**7 != 0:
            if sr&2**7 == 0:
                sr += 2**7
        length = 1
        cyc += 2
        flag = True
    elif "DEX" in asm[file[ins]]:
        xr -= 1
        if xr == -1:
            xr = 255
        if xr == 0:
            if sr&2**1 == 0:
                sr += 2**1
        else:
            if sr&2**1 != 0:
                sr -= 2**1
        if xr&2**7 != 0:
            if sr&2**7 == 0:
                sr += 2**7
        length = 1
        cyc += 2
        flag = True
    if flag == False:
        running = False
        break
    test += 1
    ins = pc - start + length
    pc += length
print("Unknown Instruction: (" + hex(pc) + ") - " + asm[file[ins]])