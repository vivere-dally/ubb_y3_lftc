AF
        // Specifies the availabe elements that are part of the alphabet
    alphabet: List<String> // Can be Set, Array
  
      // Specifies the entry point.
    initial_state: String 
  
      // Specifies the list of final points where you can exit the automaton
    final_states: List<String> // Can be Set, Array
                                          
       // Specifies the list of all the states in the automaton including the initial state, final states and the intermediary states.
    states: List<String> // Can be Set, Array
                                    
       // Specifies the list of all transitions in the automaton. See Transition
    transitions: List<Transition> // Can be Set, Array
                                                
    
Transition
      // specifies the starting state
    start: String
  
      // specifies the characters with which you can get from the starting state to the final state
    literals: String
  
      // specifies the final state
    finish: String