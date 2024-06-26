# Fr lang
# Interperted lang, looks like asm
# NO IMPORTS!!!!
from sys import argv

# Lists
code   = []    # Code as objects
label  = {}    # Labels
regs   = {}    # Registers
stack  = []    # Stack
load   = ''    # Loaded data

dbg = False

if len(argv) == 1: file = 'test.fr'
else: file = argv[1]

# Read file + preprocess (comments, empty lines)
with open(file) as f: lines = [i.strip('\n') for i in f.readlines()]# if i.strip() != '' and not i.strip().startswith('#')]


# Convert to objects
i = 0
labelName = 'root'
for i,line in enumerate(lines):
    if line.strip() == '' or line.strip().startswith('#'):
        code.append({'type':'comment','value':line.removeprefix('#').strip()})
        continue
    ind = line.count('    ') + line.count('\t')
    line = line.strip()
    if line.endswith(':') and ind == 0:
        label_ = i
        labelName = line.removesuffix(':')
        print(f'{i}: --- {labelName} ---')
        obj = {
            "type": "label",
            "name": labelName,
            "pos":  i
        }
        code.append(obj)
        label[labelName] = i
        continue
    
    obj = {
        "type": "code",
        "code": line,
        "indents": ind,
        "label": label_,
        "labelName": labelName
    }
    code.append(obj)
    print(f'{i}: {ind} {line}')

def execInst(instruction:str):
    execute(line,{'type':'code','code':instruction,'indents':0,'label':0,'labelName':'root'})

def execute(i:int,inst:dict):
    global load, regs, line, dbg
    while True:
        if i == -100 and inst == {}:
            inst = code[1]
            i = 0

        # Skip labels and comments
        if inst['type'] in {'label','comment'}:
            i += 1
            inst = code[i]
            continue
        
        line = i
        
        
            
        # Debug
        if debug or dbg:
            dbg = False
            print('Code: ',i+1,inst['code'])
            print('Regs: ',regs)
            print('Load: ',load)
            print()

        
        # Split instruction
        try:
            a = inst['code'].split(' ',1)
            opcode:str = a[0]
            args:str = a[1].strip('"')
        except:
            opcode = inst['code']
            args = None
        
        # Store instruction
        if opcode.startswith('st'):
            # Get register from end of opcode
            reg = opcode.removeprefix('st')

            # Store
            regs[reg] = load

        # Static load instruction
        elif opcode == 'ld':
            load = args
        
        # Load instruction
        elif opcode.startswith('ld'):
            # Get register from end of opcode
            reg = opcode.removeprefix('ld')

            # Load
            load = regs[reg]
        
        # Print instruction
        elif opcode == 'pnt':
            print(str(load).replace('\\n','\n'),end='')

        # Loop instruction
        elif opcode == 'loop':
            i = inst['label']
            
        # Jump instruction
        elif opcode == 'jmp':
            i = label[args]
        
        # Branch instruction
        elif opcode == 'bnc':
            execute(label[args]+1,code[label[args]+1])
        
        elif opcode == 'cmp':
            args = args.split(' ')
            if args[0] == '=':
                load = load == regs[args[1]]
            if args[0] == '!=':
                load = load != regs[args[1]]
            if args[0] == '>':
                load = load > regs[args[1]]
            if args[0] == '<':
                load = load < regs[args[1]]
            if args[0] == '<=':
                load = load <= regs[args[1]]
            if args[0] == '>=':
                load = load >= regs[args[1]]
            
        # Branch if true
        elif opcode == 'beq':
            if load: execInst(f'bnc {args}')
                
        # Branch if false
        elif opcode == 'bne':
            if not load: execInst(f'bnc {args}')        
        
        # Return from subroutine
        elif opcode == 'rts':
            return
        
        # Get input instruction
        elif opcode == 'inp':
            load = input(str(load).replace('\\n','\n'))
        
        # Exit instruction
        elif opcode == 'ext':
            print(str(load).replace('\\n','\n'),end='')
            exit()
        
        # Increment instruction
        elif opcode == 'inc':
            regs[args] = int(regs[args])+1
        
        # Decrement instruction
        elif opcode == 'dec':
            regs[args] = int(regs[args])-1
        
        # Add instruction
        elif opcode == 'add':
            args = args.split(' ')
            load = int(regs[args[0]]) + int(regs[args[1]])
        
        # Substract instruction
        elif opcode == 'sub':
            args = args.split(' ')
            load = int(regs[args[0]]) - int(regs[args[1]])
        
        # Multiply instruction
        elif opcode == 'mlt':
            args = args.split(' ')
            load = int(regs[args[0]]) * int(regs[args[1]])
        
        # Divide instruction
        elif opcode == 'div':
            args = args.split(' ')
            load = int(regs[args[0]]) / int(regs[args[1]])
        
        # Divide instruction
        elif opcode == 'exp':
            args = args.split(' ')
            load = int(regs[args[0]]) ** int(regs[args[1]])
        
        # Round instruction
        elif opcode == 'rnd':
            load = round(load,args)
        
        # Char instruction (gets first char)
        elif opcode == 'chr':
            regs[args] = load[0]
        
        # Removes first char
        elif opcode == 'rch':
            load = load[1:]
        
        # Split instruction
        elif opcode == 'spl':
            a = load.split(args.strip('"').replace('\\n','\n'))
            if len(a) == 1: a = a[0] # No 1 long lists
            load = a
            
        # Index instruction
        elif opcode == 'idx':
            load = load[int(args)]
            print(load)
        
        # Push instruction
        elif opcode == 'psh':
            stack.append(load)
        
        # Pop instruction
        elif opcode == 'pop':
            load = stack.pop()
        
        # StackPeek instruction
        elif opcode == 'spk':
            load = stack[load]
        
        # Exec instruction
        elif opcode == 'exc':
            execInst(regs[args])
            
        # Python instruction
        elif opcode == 'py':
            exec(regs[args])
        
        # Debug instruction
        elif opcode == 'dbg':
            dbg = True
        
        i += 1
        try: inst = code[i]
        except IndexError:
            return

debug = False

try: execute(-100,{})
except Exception as e:
    print(f'\nError at {line}: {e}')
    if debug: raise e
