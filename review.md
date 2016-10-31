# Lecture 1

* What is Computer Architecture?
    * Interconnecting hardware components and designing the hardware software interface to create a computing system that meets functional,  performance, energy consumption, cost, and other specific goals.

* What is ISA?

* What is MicroArchitecture?

* What is Moore's Law?

* What is Dennard Scaling?

* Microarchitecture: before 2000s
    * Faster Memory Access
        * On chip caches
        * Why is memory slow?
    * Exploiting ILP i.e. execute many instructions as possible within a single stream of execution
        * Pipelining
        * Branch Prediction
        * Superscalar
        * Out of order
        * Deep pipeline
* After 2000s
    * Focus on Multicore
    * CMPs

* Why Single-Core to Multicore?

    * complexity -> transistors -> power
    * clock rate -> switches -> power
    * limited by cooling
    * No more large benefits from ILP
        * Degrees of ILP is limited
        * Diminishing returns for ILP (more complex)
* cont.
    * Parallesim to improve performacne
        * Latency v. throughput
    * Parallesim to gain power benefits
        * Divide task into 2 independent parts. Now use 2 cores, reduce clock rate by half.
    * Benefits of multicore
        * Power -> clock rate (linear)
        * clockrate -> voltage (linear)

* Paradigm Shift
    * Moore's law survives, Dennard scaling has ended.
    * More demanding applications
    * User expectations higher
* Future
    * Heterogenous archictecture
        * GPUS, FPGAs, accelators
    * Energy efficient
    * Data intensive
    * Brain inspired computing
    * New material science

* Why Study?
    * Create better systems
    * new computing capabilites
    * understand computers

* What will you Learn?
    * Trade offs
    * Implement functional modern processor

* Buzzwords
    * ISA
    * uarch, control, datapath
    * ILP
    * Pipeline, deep pipeline, superscalar, OOO
    * Parallel processing
    * CMP
    * Cache, virtual memory, main memory
    * I/O

* What is A Computer
    * Computation
    * Communication
    * Storage

* Von Neumann Model
    * Stored Program Computer
        * Instructions stored in a linaer memory array
        * Memory is unified between instructions and data
            * Interpretations of stored value depends on control signals
    * Sequential instruction processing
        * One Instr processed at a time
        * PC ids current instr
        * Advanced sequentially except for branches
    * All major architectures are:
        * x86, ARM, MIPS, SPARC
    * microarchitecture is v different across models
        * pipelined
        * multiple
        * out of order
        * seperate instructions / caches

* ISA v. MicroArchitecture
    * ISA
        *  Agreed upon interface between software and hardware
            * SW/ Compiler assumes
        * What programmer needs to konw to write and debug system/user programs
    * Microarchitecture
        * Implementation of ISA under specific design constrains and goals.
        * Not visible to software
    * Implemtnation can vary as long as it satisfies the specification ISA
    * Microarch changs faster than ISA

# Lecture 2
* ISA
    * Opcodes, Addressing Modes, Data Types
    * Instructions Types and Formats
    * Registers, Condition Codes
    * Memory Organization
        * Address space, Adressibility, Alignment
        * Virtual Memory Management
    * Call Interrupt/ Exception Handling
    * Access Control, Priority / Priviledge
    * I/O: memory-mapped vs. instr
    * Task/ thread managment
    * Power and Thermal Managment
    * Multi-threaing support
* ISA Element
    * Or machine code, consists of
        * opcode: what it does
        * operand: parameters
* Data Types
    * Representation of information for which there are instructions that operate on the representation
    * ARMv8
        * Integer( byte, half word, word, double word)
        * FP
        * Fixed point
        * Vector Formats
    * Others
* Instruction Process Style
    * Specifies # of operands
    * 0,1,2,3 Address machines
        * 0: stack machine
        * 1: acc machine
        * 2: 2-operand machine
        * 3: 3-operand machine
    * ARMv8 is a 3 adress machine

* Instruction Classes

    * Operate Classes
        * Process Data: arith & logical
        * Fetch operands, compute result, store result
        * control flow
    * Data movement instructions
        * move data registers & i/o
        * implicit sequential control flow
    * Control flow instructions
        *  Change sequence of instructions execute
* Instruction Adressing Modes
    * Specificies how to obtain operand of instruction
        * Register
        * Immediate
        * Memory
    * Fewer or more modes of adressing?
* Instruction addressing modes for memory
    * ABS LW rt, 10000
    * Indirect  LW Rt, r(base)
    * Displaed LW Rt , offset r(base)
    * Indexed LW Rt, (r(base), r(index))
    * Memory Index
    * Memory Indirect
* Instruction Length
    * Fixed Len
        * easier to decode
        * easier to decode concurrently
        * wasted bits 
        * harder to extend ISA
    * Variable Len
        * compact
        * extensible
        * more logic to decode
        * harder to decode concurrently
    * Tradeoffs
        * size vs complexity
        * extensibility vs expressiveess vs complexity
        * performance/ energy efficieny

* Uniform / Non-uniform Decode of Inst
    * Uniform decode: same bits in each correspond to same emaing
        * opcode in same location
        * ditto operand specficiers, immediate values
        * many "risc" isa, mips, spac
        * easier, simpler hardware
        * better for para: generate target adress before knowing is a brach
        * resricts instruction format
    * Non-uniform
        * opcode can be 1st-7th byte in x86
        * more compact & powerful
        * more complex decode

* ISA Element: Registers
    * Fast
    * How many?
    * Size of each?
    * General vs. Special?
    * Why is good?
        * Data locality
        * eliminates need to go to memory

* ISA Element: Memory organization

    * Address space: How many uniquely identifiable locations in memory
    * How much data does each location store?
    * Aligned /unaligned access?

* Load/Store vs Memory Architectures

    * Can operate on memory locations vs can operate on registers

* ISA Element: Memory organization
    * Memory mapped I/O
        * region memory mapped to i/o devices
        * i/o opertions are loads and stores to those locations
    * special i/o instructions
        * in and out instructions in x86 deal with ports of the chip
    * tradeoffs
        * which is more general purpose
* Other Elements
    * Priviledge modes
    * Exception / interrupt handling
    * Virtual Memory
    * Access Protection

* CISC vs RISC

    * complex instruction set -> complex instructions
    * reduced instruct set computer -> simple instructions
    * simple compiler, complex hardware vs complex compiler, smple hardwar

* Programmer Invisible State
    * Microarchitectural State
    * Cannot access driectly
    * e.g. cache/ registers

* ARM v8 ISA
    * RISC, load/store, 32/64bits
    * 3-address machine
    * 32-bit
    * simple d-types
    * adressing mode: reg, imm, simple mem
# Lecture 3
* I skipped things that seemed obvious to me
* Review: Memory Usage Convention
    * text : program code
    * static data:
        * global variables
        * static variables
    * dynamic data :  heap
    * stack

* Review: Caller and Callee Saved Registers
    * Callee- Saved
        * Caller says to Callee," values of registers should not change "
        * Callee says I will save values of registers on stack first
    * Caller Saved Registers
        * Caller says, if there is anything I care about in these registers I already saved it myself
        * Callee says dont count on this stuff staying the sme when I'm done
* Process
    * Caller saves caller saved registers
    * Caller loads args in x0..x7
    * caller jumps to callee using BL
    * callee allocates space on stack
    * calle saves caller args
    * callee loads results to x0..x7
    * callee restores saved values
    * br x30
    * caller continues with return values in x0..x7
* Got Lazy and didnt write stuff down
# Lecture 4: Single Cycle uArch and Pipelining
* Single-Cycle uarch performance
    * Every instruction takes 1 cycle
    * Each instruction determined by slowest instruction
        * Even if other may be faster
    * not easy to optimize/improve performance
    * all resources are not fully utillized

# Lecture 5: Data Dependency
* Properties of an Ideal Pipeline
    * Increase throughput with minimal increase in cost
    * repetition of identical instructions
    * reptition of independent operations
    * uniformly partiionable suboperations

* Instruction pipeline: Not Ideal
    * different instructiosn not all need same stages; differnt instructions go through the same pipe stages
    * need to force each stage to be controlled by the same clock
    * need to detect and resolve inter-instruction dependencies to ensure the pipeine provides correct results.
* Ways of handling flow dependencies

    * Detect and wait
    * Detect & forward
    * Detect & eliminate
    * Predict and verify
    * Do something else
* How to update
    * Prevent update of PC and IF/Fd registers
    * write enabled signal for the register
    *
* Dependency Analysis
    * RAW dependence on an immediately preceding LDUR instruction this is caleld load use dependency
    * Requires a stall

# Lecture 6: Pipeling Control Dependency Handling

* Performance Analysis

    * Correct guess -> no penalty
    * incorrect guess -> 2 bubbles
    * Assume
         * no data dependency related stalls
         * 20 % control flow instructions
         * 70 % control flow instructions taken
* Improve Guess

    * Get rid of control flow instructions
    * Get rid of unnecessary control flow instructions
    * Convert control dependencies to data dependencies

* Predicatd Execution Discussions
    * Advantages
        * Works Well for Simple Control flows
        * Always not taken works better
        * Compiler has more freedom to optimize code
    * Dis
        * Useless work: some instructions fetched/ executed but discarded
        * requires ISA and hardware support
        * how to support complex control flows
        * Can we elminate all branches using predicated execution
        * Cannot adapt to dynamic behavoir
* Enhanced Branch Prediction

    * Predict the next fetch address
    * Requires 3 things
        * Whether fetched instruction is a branch
            * Accomplished using BTB which remembers target
        * Conditional branch direction
        * Branch target address
* Branch Direction Schemes
    * Compile Time (static)
        * Always taken
        * Always  not taken
        * BTFN
        * Profile Based
        * Program analysis
        * Heurestics
        * Annotated
        *
    * Run Time
        * Last time prediction
        * Two bit counter
        * Two level prediction
        * Hybrid
* Simple

    * Always not taken PC + 4
        * Simple to implement 
        * Low Accuracy
    * Always taken
        * no direction prediction
        * Better accuracy
            * backwards are usu taken
            * backward branch target address lower than branc PC

* Profile-Basd Static Branch Prediction
    * Idea: compiler determines likely direction for each branch
    *  Encodes direction as a hint bit
* Profile-Analysis Static Branch Prediction
    * Use heuristics based on program analysis
    * predict BLEZ at NT (error)
    * Example loop heursitic predict a branch guarding a loop execution as tkaen
    * Pointer and FP comparisons: Predict neq
# Lecture 7 : Branch Prediction


* Dynamic Branch Prediction
    * Can adapt to changes
    * doesn't require PL, compiler, ISA support
    * more complex
* Capturing Global Branch Correlation
    * Associate branch outcomes w/ global T/NT history
    * make a prediction basd on the outcome o the branch the last time same global branch history was encountered
    * keep track of global T/NT history of all branches in a resiter
    * Use GHR to index into a table that recorded the outcome thatw as seen for GHR value in the recent past -> PHT

* Two Levels of the Global Branch Prediction

    * First level : Global Branch history register
        * Direction of last N branches
    * Second level: 2-bit counters for each history entry
        * The direction teh branch took the las ttime the same history was seen
* Call and Return Prediction

    * Direct calls are easy to predict
        * Always taken, single target
        * Call marked in BTB, target predicted by BTB
    * Returns are indirect branches
        * A function called from many points in code 
        * return can have many target addresses
        * Usually return matches a call
        * Idea: Usesr to stack to predict return adresses
            * A fetched call : pushes the return onto the stack
            * a fetched return : pops the stack
            * Accurate 95% of time
* Other Branch Predictors
    * Loop branch detector/ predictor
    * Biased  branches & predict them with simpler predictor
* Other Considerations
    * Flyn's bottleneck
        *  machine will never obtain IPC greater than 1
    * Prediction is latency critical
        * Geneerate fetch address for next cycle
        * Bigger more complex predictors
    * More complex processors
        * Multi-issue
        * What is branch in the middle of fetched
* Delayed Branching
    * Delay the execution of a branch. N instructions that come afer the branch are awlays executed regardless of direction
    * How to find instructions to fill delay?
    * Unconditional branches: Easier to find instrucitons
    * Condition computation should not depend on instructions in delay slots

* Fancy Delayed Branching

    * Delayed branch with squashing
        * in SPARC
        * if the branch falls thru the delay slot is not executed

* Delayed Branching
    * Advantages
        * keeps the pipeline full assuming number of delay slots == number of instructions to keep the pipeline full before the branch resolves
        * all delay slots can be filled with useful instruction
    * dis-Advantages
        * not easy to fill slots
        * ties ISA semantics to hardware implemntation 

# Lecture 8: OUt of Order Execution
* Two Levels of GShare
    * N bits xor PC
    * 2-bit counters fo each history entry
* Dependency Handling in Pipeline
    * Software vs. Hardware
        * static scheduling
        * dynamic scheduling
    * What information does the compiler not know that makes tatic scheulding difficult
        * Anything determined at runtime
* Out-of-Order Execution
    * Idea
        * Move depedent instructions out of the way of independent ones
    * Approach
        * Monitor the source values of each instruction
        * When all source variables of an instruction are avaiablable, fire the instruction
        * retire each instruction in program order
    * Benefit
        * Latency Tolerance: allows independent instructions to execute and complete in the presence of a long latency operation

* Tomasulo's Algorithim
    * Register renaming
        * Track true dependency by link the consumer of a vlluae oto the producer
    * Buffer instructions in reservation stations until they are ready to execute
        *  Keep track of readiness of source values
        * Inustruction wakes up and dispatch to teh appropriate functional unit if all sources are ready
        * If mulitple instructions are awake, need to sleect one per FU

* Register Renaming
    * Output and anti-dependencies are not true dependencies
    * The register value is renamd to the reservation station entry that willl hold the register's value.
        * Register Id -> RS entry ID
        * Architectural register ID -> Physical REgister ID
        * After renaming, RS entry ID used to refer to teh regsister
    * Eliminates anti and output dependencies
        * large # of registers even though ISA can only support small nubmer
* Tomasulo's Algorithim
    * If reservation available, stall;
    else instruction + renmaed operands insert into the reservation station
    * While in reservation station, each instruction:
        * watches common data bus for tag of its sources
        * when tag seen grab value for source and keep in resveration station
        * when both ops available instruction ready to bre dispactched
    * Dispatch instruction to FU when instruction is ready
        * if mulitple instructions ready at the same time and require teh same FU need logic to select one
    * AFter instructions finishes in the FU
        * Arbitrate for CDB
        * Put tagged value onto CDB
        * Register file, RS and RAT connected to teh CDB
            * Register contains a tag indicatin the latest writer to teh register
            * If the rag in the register file, RS, and RAt matches the broad cast tag, write broadcast value into register ( and set valid bit)
        * Reclaim tag name

# Lecture 9: OUt of Order Execution II

# Lecture 10: Caches
