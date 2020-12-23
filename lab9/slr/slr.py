from collections import deque
from enum import Enum

from typing import List, Dict, Deque, Union

from lab9.grammar.grammar import Grammar
from lab9.grammar.production_rule import ProductionRule
from lab9.grammar.symbols.dollar import Dollar
from lab9.grammar.symbols.epsilon import Epsilon
from lab9.grammar.symbols.nonterminal import Nonterminal
from lab9.grammar.symbols.symbol import Symbol
from lab9.grammar.symbols.terminal import Terminal
from lab9.slr.closure import Closure, ClosureTransition
from lab9.slr.first_and_follow import FnF
from lab9.slr.lr0item import LR0Item


class ReduceReduceConflict(RuntimeError):
    def __init__(self, closure: Closure, index: int):
        super().__init__(f'REDUCE REDUCE ERROR for closure with index {index}.\n{closure}')


class ShiftReduceConflict(RuntimeError):
    def __init__(self, closure: Closure, symbol: Symbol, index: int):
        super().__init__(f'SHIFT REDUCE ERROR for {closure} at {symbol} with index {index}.')


class ParsingError(RuntimeError):
    def __init__(self, temporary_result: List[str], message: str):
        newline = '\n'
        super().__init__(f"{newline.join([result for result in temporary_result])}\n{message}")


class ParsingTableActionState(Enum):
    """
    Class that represents the possible actions in a SLR Parsing Table.
    """

    ERROR = 0
    SHIFT = 1
    REDUCE = 2
    GOTO = 3
    ACCEPT = 4

    def __repr__(self):
        return self.name

    def __str__(self):
        return repr(self)


class ParsingTableAction:
    """
    Class that represents an action in a SLR Parsing Table.
    Based on the ParsingTableActionState the following actions will be possible:
    ERROR => an Error will be thrown when parsing.
    SHIFT => encountered a terminal when parsing. Shift to index
    REDUCE => we have a possible reduce. Apply a production rule and reduce to lhs.
    GOTO => encountered a non-terminal when parsing. Go to index
    ACCEPT => the parsed sequence was accepted.
    """

    def __init__(self, index: int, state: ParsingTableActionState):
        self.__index = index
        self.__state = state

    @property
    def index(self) -> int:
        return self.__index

    @property
    def state(self) -> ParsingTableActionState:
        return self.__state

    def __repr__(self):
        return f"{self.__state} to {self.__index}"

    def __str__(self):
        return repr(self)


class SLR:
    def __init__(self, grammar: Grammar, fnf: FnF):
        self.__grammar = grammar
        self.__fnf = fnf

        # Canonical collection
        self.__augmented_production = ProductionRule(
            Nonterminal(f"{self.__grammar.start_symbol.symbol}'"),
            [self.__grammar.start_symbol])
        self.__closures: List[Closure] = []
        self.__transitions: List[ClosureTransition] = []
        self.__build_canonical_collection()
        # [print(f"{index} --- {closure}") for index, closure in enumerate(self.__closures)]  # print for debug
        # [print(repr(transition)) for transition in self.__transitions]  # print for debug

        # Parsing table
        self.__parsing_table: List[Dict[Symbol, ParsingTableAction]] = []
        self.__build_parsing_table()
        # [print(x) for x in enumerate(self.__parsing_table)]  # print for debug

    def __build_canonical_collection(self):
        """
        Build canonical collection. TODO COMMENT
        """
        start_closure = Closure(self.__grammar, [LR0Item(self.__augmented_production)])
        self.__closures = [start_closure]
        dq = deque([start_closure])
        while len(dq) > 0:
            closure = dq.popleft()
            symbols = {}
            # Get non-final items' symbols from the closure
            for item in closure.lr0items:
                if not item.is_final_item:
                    if item.current_symbol == Epsilon():
                        continue
                    if item.current_symbol in symbols:
                        symbols[item.current_symbol].append(item)
                    else:
                        symbols[item.current_symbol] = [item]

            # Solve items
            closure_index = self.__closures.index(closure)
            for symbol, items in symbols.items():
                lr0items = []
                for item in items:
                    lr0items.append(item.solve(symbol))

                new_closure = Closure(self.__grammar, lr0items)
                if new_closure not in self.__closures:
                    self.__closures.append(new_closure)
                    dq.append(new_closure)

                new_closure_index = self.__closures.index(new_closure)
                self.__transitions.append(ClosureTransition(symbol, closure_index, new_closure_index))

    def __build_parsing_table(self):
        """
        Build the parsing table. TODO COMMENT
        """

        def __find_transition__(symbol: Symbol, from_index: int) -> int:
            """
            Find the transition by a symbol and a start index.
            """
            for transition in self.__transitions:
                if transition.symbol == symbol and transition.from_index == from_index:
                    return transition.to_index

            return -1  # No transition found

        all_symbols: List[Symbol] = self.__grammar.terminals
        all_symbols.extend(self.__grammar.nonterminals)
        all_symbols.append(Dollar())

        # Fill table with errors
        for index in range(len(self.__closures)):
            symbol_action_dict = {}
            for symbol in all_symbols:
                symbol_action_dict[symbol] = ParsingTableAction(index, ParsingTableActionState.ERROR)

            self.__parsing_table.append(symbol_action_dict)

        for index, closure in enumerate(self.__closures):
            # Check for RR Conflict
            if closure.is_final_closure and len(closure.lr0items) > 1:
                follows_intersection = set.intersection(
                    *[self.__fnf.get_follow_of_nonterminal(item.production_rule.lhs) for item
                      in closure.lr0items])
                if len(follows_intersection) != 0:
                    raise ReduceReduceConflict(closure, index)

            # Reduce for all final/epsilon items
            for item in closure.lr0items:
                if item.is_final_item or \
                        Epsilon() in item.production_rule.rhs:
                    for follow_symbol in self.__fnf.get_follow_of_nonterminal(item.production_rule.lhs):
                        self.__parsing_table[index][follow_symbol] = ParsingTableAction(
                            # Take the index of the production rule with which we should reduce
                            self.__grammar.production_rules.index(item.production_rule),
                            ParsingTableActionState.REDUCE
                        )

            # Decide by transitions
            for symbol in all_symbols:
                to_index = __find_transition__(symbol, index)

                # Accept
                if to_index == -1 and \
                        closure.is_final_closure and \
                        len(closure.lr0items) == 1 and \
                        closure.lr0items[0].production_rule == self.__augmented_production and \
                        symbol == Dollar():
                    self.__parsing_table[index][symbol] = ParsingTableAction(to_index,
                                                                             ParsingTableActionState.ACCEPT)
                # Shift/Goto
                elif to_index != -1:
                    if isinstance(symbol, Nonterminal):
                        self.__parsing_table[index][symbol] = ParsingTableAction(to_index, ParsingTableActionState.GOTO)
                    elif isinstance(symbol, Terminal):
                        for item in closure.lr0items:
                            if item.is_final_item and \
                                    symbol in self.__fnf.get_follow_of_nonterminal(item.production_rule.lhs):
                                raise ShiftReduceConflict(closure, symbol, index)

                        self.__parsing_table[index][symbol] = ParsingTableAction(to_index,
                                                                                 ParsingTableActionState.SHIFT)

    def parse(self, buffer: List[Symbol]) -> List[str]:
        buffer.append(Dollar())  # Add $ at the end.
        result: List[str] = []
        stack: Deque[Union[int, Symbol]] = deque([0])  # Start from the first closure.
        i = 0
        action_index = 1
        while i < len(buffer):
            result.append(f"=== STEP {action_index} ===\n-> STACK STATE: {stack}")
            from_index = stack[-1]
            buffer_symbol = buffer[i]
            action = self.__parsing_table[from_index][buffer_symbol]
            if action.state == ParsingTableActionState.ERROR:
                raise ParsingError(result, f"ERROR: no action found at index {from_index} with {buffer_symbol}.")

            elif action.state == ParsingTableActionState.SHIFT:
                result.append(f"SHIFT: from {from_index} to {action.index} with {buffer_symbol}.")
                stack.append(buffer_symbol)
                stack.append(action.index)

            elif action.state == ParsingTableActionState.REDUCE:
                production_rule = self.__grammar.production_rules[action.index]
                result.append(f"REDUCE: use production rule {production_rule}.")
                if not Epsilon() in production_rule.rhs:
                    for _ in production_rule.rhs:  # Pop 2*len(rhs) items.
                        stack.pop()
                        stack.pop()

                action_index += 1
                from_index = stack[-1]
                stack.append(production_rule.lhs)
                result.append(f"=== STEP {action_index} ===\n-> STACK STATE: {stack}")
                action = self.__parsing_table[from_index][production_rule.lhs]
                result.append(f"GOTO: from {from_index} to {action.index} with {production_rule.lhs}.")
                stack.append(action.index)
                i -= 1  # Performed a reduce, decrement i

            elif action.state == ParsingTableActionState.ACCEPT:
                result.append(f"END: from {from_index} to ACCEPTED with {buffer_symbol}")

            i += 1
            action_index += 1

        return result
