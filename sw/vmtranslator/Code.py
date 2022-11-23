#!/usr/bin/env python3
import io
import os
import queue
import uuid


class Code:
    def __init__(self, outFile):
        self.outFile = outFile
        self.counter = 0
        self.vmFileName = None
        self.labelCounter = 0

    # DONE
    def close(self):
        self.outFile.close()

    # DONE
    def updateVmFileName(self, name):
        self.vmFileName = os.path.basename(name).split(".")[0]

    # DONE
    def commandsToFile(self, commands):
        for line in commands:
            self.outFile.write(f"{line}\n")

    # DONE
    def getUniqLabel(self):
        return self.vmFileName + str(self.labelCounter)

    # DONE
    def updateUniqLabel(self):
        self.labelCounter = self.labelCounter + 1

    # DONE
    def writeHead(self, command):
        self.counter = self.counter + 1
        return ";; " + command + " - " + str(self.counter)

    # DONE
    def writeInit(self, bootstrap, isDir):
        commands = []

        if bootstrap or isDir:
            commands.append(self.writeHead("init"))

        if bootstrap:
            commands.append("leaw $256,%A")
            commands.append("movw %A,%D")
            commands.append("leaw $SP,%A")
            commands.append("movw %D,(%A)")

        if isDir:
            commands.append("leaw $Main.main, %A")
            commands.append("jmp")
            commands.append("nop")

        if bootstrap or isDir:
            self.commandsToFile(commands)

    # TODO
    def writeLabel(self, label):
        commands = []
        commands.append(self.writeHead("label") + " " + label)

        # TODO ...
        self.commandsToFile(commands)

    # TODO
    def writeGoto(self, label):
        commands = []
        commands.append(self.writeHead("goto") + " " + label)

        # TODO ...
        self.commandsToFile(commands)

    # TODO
    def writeIf(self, label):
        commands.append(self.writeHead("if") + " " + label)
        commands = []

        # TODO ...
        self.commandsToFile(commands)

    # TODO
    def writeArithmetic(self, command):
        self.updateUniqLabel()
        if len(command) < 2:
            print("instrucão invalida {}".format(command))
        commands = []
        commands.append(self.writeHead(command))

        if command == "add":
            commands.append("leaw $SP, %A")
            commands.append("movw (%A), %A")  # A ta com 258 
            commands.append("decw %A")   # A = 257
            commands.append("movw (%A), %D")  # D ta com y
            commands.append("decw %A")   # A = 256
            commands.append("addw (%A), %D, %D") # (A) ta com x, x+y em D
            commands.append("movw %D, (%A)") 
            commands.append("incw %A")
            commands.append("movw %A, %D")
            commands.append("leaw $SP, %A")
            commands.append("movw %D, (%A)")


        elif command == "sub":
            commands.append("leaw $SP, %A")
            commands.append("movw (%A), %A")  # A ta com 258 
            commands.append("decw %A")   # A = 257
            commands.append("movw (%A), %D")  # D ta com y
            commands.append("decw %A")   # A = 256
            commands.append("subw (%A), %D, %D") # (A) ta com x, x+y em D
            commands.append("movw %D, (%A)") 
            commands.append("incw %A")
            commands.append("movw %A, %D")
            commands.append("leaw $SP, %A")
            commands.append("movw %D, (%A)")
        
        elif command == "or":
            commands.append("leaw $SP, %A")
            commands.append("movw (%A), %A")  # A ta com 258 
            commands.append("decw %A")   # A = 257
            commands.append("movw (%A), %D")  # D ta com y
            commands.append("decw %A")   # A = 256
            commands.append("orw (%A), %D, %D") # (A) ta com x, xory em D
            commands.append("movw %D, (%A)") 
            commands.append("incw %A")
            commands.append("movw %A, %D")
            commands.append("leaw $SP, %A")
            commands.append("movw %D, (%A)")
            
        elif command == "and":
            commands.append("leaw $SP, %A")
            commands.append("movw (%A), %A")  # A ta com 258 
            commands.append("decw %A")   # A = 257
            commands.append("movw (%A), %D")  # D ta com y
            commands.append("decw %A")   # A = 256
            commands.append("andw (%A), %D, %D") # (A) ta com x, xory em D
            commands.append("movw %D, (%A)") 
            commands.append("incw %A")
            commands.append("movw %A, %D")
            commands.append("leaw $SP, %A")
            commands.append("movw %D, (%A)")
            
            

        elif command == "not":
            commands.append("leaw $SP, %A")
            commands.append("movw (%A), %A")  # A ta com 257
            commands.append("decw %A")   # A = 256
            commands.append("movw (%A), %D")  # D ta com x
            commands.append("notw, %D, %D") # D ta x not 
            commands.append("movw %D, (%A)")  # D em 256
            commands.append("incw %A")   
            commands.append("movw %A, %D")  # 
            commands.append("leaw $SP ,%A")   
            commands.append("movw %D, (%A)")  # 
        
        
        
        elif command == "neg":
            commands.append("leaw $SP, %A")
            commands.append("movw (%A), %A")  # A ta com 257
            commands.append("decw %A")   # A = 256
            commands.append("movw (%A), %D")  # D ta com x
            commands.append("negw, %D, %D") # D ta x not 
            commands.append("movw %D, (%A)")  # D em 256
            commands.append("incw %A")   
            commands.append("movw %A, %D")  # 
            commands.append("leaw $SP ,%A")   
            commands.append("movw %D, (%A)")  # 
        
        elif command == "eq":
            # dica, usar self.getUniqLabel() para obter um label único

            zerou = self.getUniqLabel()
            self.updateUniqLabel()
            fim = self.getUniqLabel()

            commands.append("leaw $SP, %A")   
            commands.append("movw (%A), %A")  # A = 258 
            
            commands.append("decw %A")   # A= 257
            commands.append("movw (%A), %D")   # D TA C Y
            commands.append("decw %A")  # A= 256
            commands.append("subw (%A), %D, %D")   # D TA C X-Y

            commands.append(f"leaw ${zerou}, %A")     
            commands.append("je")  
            commands.append("nop")  
            
            commands.append("leaw $0, %A")  
            commands.append("movw %A, %D") 
            
            commands.append("leaw $SP, %A") 
            commands.append('movw (%A), %A')
            commands.append("decw %A") 
            commands.append("decw %A") 
            commands.append("movw %D, (%A)")      

            commands.append(f"leaw ${fim}, %A")     
            commands.append("jmp")  
            commands.append("nop")       
            
            
            commands.append(f"{zerou}:")  
            
            commands.append("leaw $65535, %A")  
            commands.append("movw %A, %D") 
            commands.append("leaw $SP, %A") 
            commands.append('movw (%A), %A')
            commands.append("decw %A") 
            commands.append("decw %A") 
            commands.append("movw %D, (%A)") 

            commands.append(f"{fim}:")  
            commands.append("leaw $SP, %A")  
            commands.append("movw (%A), %D") 
            commands.append("decw %D") 
            commands.append("movw %D, (%A)") 
        


            



            pass # TODO
        elif command == "gt":

            pozi = self.getUniqLabel()
            self.updateUniqLabel()
            fim= self.getUniqLabel()

            commands.append("leaw $SP, %A")   
            commands.append("movw (%A), %A")  # A = 258 
            
            commands.append("decw %A")   # A= 257
            commands.append("movw (%A), %D")   # D TA C Y
            commands.append("decw %A")  # A= 256
            commands.append("subw (%A), %D, %D")   # D TA C X-Y

            commands.append(f"leaw ${pozi}, %A")     
            commands.append("jg")  
            commands.append("nop")  
            
            commands.append("leaw $0, %A")  
            commands.append("movw %A, %D") 
            
            commands.append("leaw $SP, %A") 
            commands.append('movw (%A), %A')
            commands.append("decw %A") 
            commands.append("decw %A") 
            commands.append("movw %D, (%A)")      

            commands.append(f"leaw ${fim}, %A")     
            commands.append("jmp")  
            commands.append("nop")       
            
            
            commands.append(f"{pozi}:")  
            
            commands.append("leaw $65535, %A")  
            commands.append("movw %A, %D") 
            commands.append("leaw $SP, %A") 
            commands.append('movw (%A), %A')
            commands.append("decw %A") 
            commands.append("decw %A") 
            commands.append("movw %D, (%A)") 

            commands.append(f"{fim}:")  
            commands.append("leaw $SP, %A")  
            commands.append("movw (%A), %D") 
            commands.append("decw %D") 
            commands.append("movw %D, (%A)") 
        




        elif command == "lt":
            # dica, usar self.getUniqLabel() para obter um label único
            neg = self.getUniqLabel()
            self.updateUniqLabel()
            fim= self.getUniqLabel()

            commands.append("leaw $SP, %A")   
            commands.append("movw (%A), %A")  # A = 258 
            
            commands.append("decw %A")   # A= 257
            commands.append("movw (%A), %D")   # D TA C Y
            commands.append("decw %A")  # A= 256
            commands.append("subw (%A), %D, %D")   # D TA C X-Y

            commands.append(f"leaw ${neg}, %A")     
            commands.append("jl")  
            commands.append("nop")  
            
            commands.append("leaw $0, %A")  
            commands.append("movw %A, %D") 
            
            commands.append("leaw $SP, %A") 
            commands.append('movw (%A), %A')
            commands.append("decw %A") 
            commands.append("decw %A") 
            commands.append("movw %D, (%A)")      

            commands.append(f"leaw ${fim}, %A")     
            commands.append("jmp")  
            commands.append("nop")       
            
            
            commands.append(f"{neg}:")  
            
            commands.append("leaw $65535, %A")  
            commands.append("movw %A, %D") 
            commands.append("leaw $SP, %A") 
            commands.append('movw (%A), %A')
            commands.append("decw %A") 
            commands.append("decw %A") 
            commands.append("movw %D, (%A)") 

            commands.append(f"{fim}:")  
            commands.append("leaw $SP, %A")  
            commands.append("movw (%A), %D") 
            commands.append("decw %D") 
            commands.append("movw %D, (%A)") 
        

        self.commandsToFile(commands)

    def writePop(self, command, segment, index):
        self.updateUniqLabel()
        commands = []
        commands.append(self.writeHead(command) + " " + segment + " " + str(index))

        if segment == "" or segment == "constant":
            return False
        elif segment == "local":
            # dica: usar o argumento index (push local 1)
            
            commands.append("leaw $13, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $32, %A") 
            commands.append('movw %D, (%A)') 
            
            commands.append("leaw $8, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $34, %A") 
            commands.append('movw %D, (%A)')

            commands.append("leaw $257, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $0, %A") 
            commands.append('movw %D, (%A)')

        elif segment == "argument":
            commands.append("leaw $13, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $32, %A") 
            commands.append('movw %D, (%A)') 
            
            commands.append("leaw $8, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $34, %A") 
            commands.append('movw %D, (%A)')

            commands.append("leaw $257, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $0, %A") 
            commands.append('movw %D, (%A)')

    
        elif segment == "this":
            commands.append("leaw $13, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $1024, %A") 
            commands.append('movw %D, (%A)') 
            
            commands.append("leaw $8, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $1026, %A") 
            commands.append('movw %D, (%A)')

            commands.append("leaw $257, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $0, %A") 
            commands.append('movw %D, (%A)')

        elif segment == "that":
            commands.append("leaw $13, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $1024, %A") 
            commands.append('movw %D, (%A)') 
            
            commands.append("leaw $8, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $1026, %A") 
            commands.append('movw %D, (%A)')

            commands.append("leaw $257, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $0, %A") 
            commands.append('movw %D, (%A)')
            
        elif segment == "temp":
            # dica: usar o argumento index (push temp 0)
            commands.append("leaw $13, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $10, %A") 
            commands.append('movw %D, (%A)') 
            
            commands.append("leaw $8, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $12, %A") 
            commands.append('movw %D, (%A)')

            commands.append("leaw $257, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $0, %A") 
            commands.append('movw %D, (%A)')
            pass # TODO
        elif segment == "static":
            pass # TODO
        elif segment == "pointer":
            commands.append("leaw $13, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $THIS, %A") 
            commands.append('movw %D, (%A)') 
            
            commands.append("leaw $8, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $THAT, %A") 
            commands.append('movw %D, (%A)')

            commands.append("leaw $257, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $0, %A") 
            commands.append('movw %D, (%A)')
            

        self.commandsToFile(commands)

    def writePush(self, command, segment, index):
        commands = []
        commands.append(self.writeHead(command + " " + segment + " " + str(index)))

        if segment == "constant":
            # dica: usar index para saber o valor da consante
            # push constant index
            commands.append("leaw $12, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $256, %A") 
            commands.append('movw %D, (%A)') 
            
            commands.append("leaw $143, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $257, %A") 
            commands.append('movw %D, (%A)')

            commands.append("leaw $258, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $SP, %A") 
            commands.append('movw %D, (%A)')
        elif segment == "local":
            commands.append("leaw $4, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $256, %A") 
            commands.append('movw %D, (%A)') 
            
            commands.append("leaw $13, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $257, %A") 
            commands.append('movw %D, (%A)')

            commands.append("leaw $258, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $SP, %A") 
            commands.append('movw %D, (%A)')
        elif segment == "argument":
            commands.append("leaw $4, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $256, %A") 
            commands.append('movw %D, (%A)') 
            
            commands.append("leaw $13, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $257, %A") 
            commands.append('movw %D, (%A)')

            commands.append("leaw $258, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $SP, %A") 
            commands.append('movw %D, (%A)')
            
        elif segment == "this":
            commands.append("leaw $4, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $256, %A") 
            commands.append('movw %D, (%A)') 
            
            commands.append("leaw $13, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $257, %A") 
            commands.append('movw %D, (%A)')

            commands.append("leaw $258, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $SP, %A") 
            commands.append('movw %D, (%A)')
        elif segment == "that":
            commands.append("leaw $4, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $256, %A") 
            commands.append('movw %D, (%A)') 
            
            commands.append("leaw $13, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $257, %A") 
            commands.append('movw %D, (%A)')

            commands.append("leaw $258, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $SP, %A") 
            commands.append('movw %D, (%A)')

   
        elif segment == "static":
            commands.append("leaw $4, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $256, %A") 
            commands.append('movw %D, (%A)') 
            
            commands.append("leaw $13, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $257, %A") 
            commands.append('movw %D, (%A)')

            commands.append("leaw $258, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $SP, %A") 
            commands.append('movw %D, (%A)')
        elif segment == "temp":
            commands.append("leaw $4, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $256, %A") 
            commands.append('movw %D, (%A)') 
            
            commands.append("leaw $13, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $257, %A") 
            commands.append('movw %D, (%A)')

            commands.append("leaw $258, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $SP, %A") 
            commands.append('movw %D, (%A)')
        
        elif segment == "pointer":
            commands.append("leaw $4, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $256, %A") 
            commands.append('movw %D, (%A)') 
            
            commands.append("leaw $8, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $257, %A") 
            commands.append('movw %D, (%A)')

            commands.append("leaw $258, %A") 
            commands.append('movw %A, %D')
            commands.append("leaw $SP, %A") 
            commands.append('movw %D, (%A)')

        self.commandsToFile(commands)

    # TODO
    def writeCall(self, funcName, numArgs):
        commands = []
        commands.append(self.writeHead("call") + " " + funcName + " " + str(numArgs))

        # TODO
        # ...

        self.commandsToFile(commands)

    # TODO
    def writeReturn(self):
        commands = []
        commands.append(self.writeHead("return"))

        # TODO
        # ...

        self.commandsToFile(commands)

    # TODO
    def writeFunction(self, funcName, numLocals):
        commands = []
        commands.append(self.writeHead("func") + " " + funcName + " " + str(numLocals))

        # TODO
        # ...

        self.commandsToFile(commands)
