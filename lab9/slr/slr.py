from typing import List, Dict
from enum import Enum
from collections import deque

from lab9.grammar.grammar import Grammar, ProductionRule, Symbol, Nonterminal, Dollar, Terminal


class LR0Item:
    def __init__(self, production_rule: ProductionRule):
        if len(production_rule.rhs) == 0:
            raise RuntimeError('RHS cannot be empty.')

        self.__production_rule = production_rule
        self.__dot_index = 0

    @property
    def production_rule(self) -> ProductionRule:
        return self.__production_rule

    @property
    def dot_index(self) -> int:
        return self.__dot_index

    @property
    def current_symbol(self) -> Symbol:
        return self.__production_rule.rhs[self.__dot_index]

    def can_solve(self, symbol: Symbol) -> bool:
        if self.__production_rule.rhs[self.__dot_index] == symbol:
            return True

        return False

    def solve(self, symbol: Symbol) -> 'LR0Item':
        if not self.can_solve(symbol):
            raise RuntimeError(f'Cannot solve with {symbol}')

        item = LR0Item(self.__production_rule)
        item.__dot_index = self.__dot_index + 1
        return item

    def is_final_item(self) -> bool:
        return self.__dot_index == len(self.__production_rule.rhs)

    def __eq__(self, other) -> bool:
        return isinstance(other, LR0Item) and \
               self.__production_rule == other.__production_rule and \
               self.__dot_index == other.__dot_index

    def __ne__(self, other) -> bool:
        return not self == other

    def __repr__(self) -> str:
        return f'{repr(self.__production_rule)} with dot at {self.__dot_index}'

    def __str__(self) -> str:
        return repr(self)


class ClosureTransition:
    def __init__(self, symbol: Symbol, form_index: int, to_index: int):
        self.__symbol = symbol
        self.__form_index = form_index
        self.__to_index = to_index

    @property
    def symbol(self) -> Symbol:
        return self.__symbol

    @property
    def from_index(self) -> int:
        return self.__form_index

    @property
    def to_index(self) -> int:
        return self.__to_index


class ParsingTableActionState(Enum):
    ERROR = 0
    SHIFT = 1
    REDUCE = 2
    GOTO = 3
    ACCEPT = 4


class ParsingTableAction:
    def __init__(self, index: int, state: ParsingTableActionState):
        self.__index = index
        self.__state = state

    @property
    def index(self) -> int:
        return self.__index

    @property
    def state(self) -> ParsingTableActionState:
        return self.__state


class Closure:
    def __init__(self, grammar: Grammar, lr0items: List[LR0Item]):
        self.__grammar = grammar
        self.__lr0items = lr0items
        self.__apply_closure()

    def __apply_closure(self):
        new_lr0items = []
        for lr0item in self.__lr0items:
            new_lr0items.extend(self.__apply_closure_item(lr0item))

        self.__lr0items.extend(new_lr0items)

    def __apply_closure_item(self, lr0item: LR0Item) -> List[LR0Item]:
        new_lr0items = []
        if lr0item.is_final_item():
            return []

        symbol = lr0item.current_symbol
        # if Nonterminal.is_nonterminal(symbol.symbol):
        if isinstance(symbol, Nonterminal):
            for production_rule in self.__grammar.get_production_rules_by_lhs_nonterminal(symbol):
                new_lr0item = LR0Item(production_rule)
                new_lr0items.append(new_lr0item)
                new_lr0items.extend(self.__apply_closure_item(new_lr0item))

        return new_lr0items

    @property
    def lr0items(self) -> List[LR0Item]:
        return self.__lr0items

    def is_final_closure(self) -> bool:
        for lr0item in self.__lr0items:
            if not lr0item.is_final_item():
                return False

        return True

    def __eq__(self, other) -> bool:
        return self.__lr0items == other.__lr0items

    def __ne__(self, other) -> bool:
        return not self == other


class ReduceReduceConflict(RuntimeError):
    def __init__(self, symbol: Symbol, from_index: int, lr0items: List[LR0Item]):
        super().__init__(
            f'REDUCE REDUCE ERROR at {symbol} with index {from_index} - {[repr(lr0item) for lr0item in lr0items]}')


class ShiftReduceConflict(RuntimeError):
    def __init__(self, symbol: Symbol, from_index: int, lr0items: List[LR0Item]):
        super().__init__(
            f'SHIFT REDUCE ERROR at {symbol} with index {from_index} - {[repr(lr0item) for lr0item in lr0items]}')


class ParsingError(RuntimeError):
    def __init__(self, symbol: Symbol, from_index: int):
        super().__init__(
            f'PARSING ERROR at {symbol}. No production rule found with index {from_index}')


class SLR:
    def __init__(self, grammar: Grammar):
        self.__grammar = grammar
        self.__augmented_production = ProductionRule(Nonterminal(f"{grammar.start_symbol.symbol}'"),
                                                     [grammar.start_symbol])

        start_closure = Closure(self.__grammar, [LR0Item(self.__augmented_production)])
        self.__unbuilt_closures = deque([start_closure])
        self.__closures = [start_closure]
        self.__transitions = []
        self.__build_canonical_collection()

        self.__parsing_table: List[Dict[Symbol, ParsingTableAction]] = []
        self.__build_parsing_table()

    def __build_canonical_collection(self):
        while len(self.__unbuilt_closures) != 0:
            closure = self.__unbuilt_closures.popleft()
            symbols = {}
            for lr0item in closure.lr0items:
                if not lr0item.is_final_item():
                    symbols[lr0item.current_symbol] = []

            for symbol, lr0items in symbols.items():
                for lr0item in closure.lr0items:
                    if not lr0item.is_final_item() and lr0item.can_solve(symbol):
                        lr0items.append(lr0item.solve(symbol))

            for symbol, lr0items in symbols.items():
                new_closure = Closure(self.__grammar, lr0items)
                if new_closure not in self.__closures:
                    self.__closures.append(new_closure)
                    self.__unbuilt_closures.append(new_closure)

                closure_index = self.__closures.index(closure)
                new_closure_index = self.__closures.index(new_closure)
                self.__transitions.append(ClosureTransition(symbol, closure_index, new_closure_index))

    def __find_transition(self, symbol: Symbol, from_index: int) -> int:
        for transition in self.__transitions:
            if transition.symbol == symbol and transition.from_index == from_index:
                return transition.to_index

        return -1

    def __build_parsing_table(self):
        all_symbols = set(self.__grammar.nonterminals).union(set(self.__grammar.terminals))
        all_symbols.add(Dollar())

        for index, closure in enumerate(self.__closures):
            current_dict = {}
            for symbol in all_symbols:
                to_index = self.__find_transition(symbol, index)
                if to_index == -1:
                    if closure.is_final_closure():
                        found = False
                        for follow in self.__grammar.get_follow_of_nonterminal(closure.lr0items[0].production_rule.lhs):
                            if follow.symbol == symbol.symbol:
                                found = True

                        if len(closure.lr0items) == 1 and found:
                            to_index = self.__grammar.production_rules.index(closure.lr0items[0].production_rule)
                            current_dict[symbol] = ParsingTableAction(to_index, ParsingTableActionState.REDUCE)
                        elif len(closure.lr0items) == 1:
                            if closure.lr0items[0].production_rule == self.__augmented_production:
                                current_dict[symbol] = ParsingTableAction(to_index, ParsingTableActionState.ACCEPT)
                            else:
                                current_dict[symbol] = ParsingTableAction(to_index, ParsingTableActionState.ERROR)
                        else:
                            follows = []
                            for lr0item in closure.lr0items:
                                follows.append(self.__grammar.get_follow_of_nonterminal(lr0item.production_rule.lhs))

                            follows = set.intersection(*follows)
                            if len(follows) == 0:
                                to_index = self.__grammar.production_rules.index(closure.lr0items[0].production_rule)
                                current_dict[symbol] = ParsingTableAction(to_index, ParsingTableActionState.REDUCE)
                                pass
                            else:
                                raise ReduceReduceConflict(symbol, index, closure.lr0items)
                    else:
                        current_dict[symbol] = ParsingTableAction(to_index, ParsingTableActionState.ERROR)

                else:
                    if Nonterminal.is_nonterminal(symbol.symbol):
                        current_dict[symbol] = ParsingTableAction(to_index, ParsingTableActionState.GOTO)
                    elif Terminal.is_terminal(symbol.symbol) or Dollar.is_dollar(symbol.symbol):
                        for lr0item in closure.lr0items:
                            if lr0item.is_final_item() and \
                                    symbol in self.__grammar.get_follow_of_nonterminal(lr0item.production_rule.lhs):
                                raise ShiftReduceConflict(symbol, index, closure.lr0items)

                        current_dict[symbol] = ParsingTableAction(to_index, ParsingTableActionState.SHIFT)

            self.__parsing_table.append(current_dict)

        self.__parsing_table = list(self.__parsing_table)

    def __get_by_symbol(self, index: int, item: Symbol) -> ParsingTableAction:
        table = self.__parsing_table
        for key, value in table[index].items():
            if key.symbol == item.symbol:
                return value

        return None

    def __perform(self, item: Symbol, stack) -> str:
        output = ''
        top_most_index = stack[-1]
        next_state = self.__get_by_symbol(top_most_index, item)
        if next_state.state == ParsingTableActionState.ERROR:
            raise ParsingError(item, top_most_index)

        elif next_state.state == ParsingTableActionState.GOTO:
            output = f'Performed GOTO: {item} to {next_state.index}\n'
            stack.append(item)
            stack.append(next_state.index)

        elif next_state.state == ParsingTableActionState.SHIFT:
            output = f'Performed SHIFT: {item} to {next_state.index}\n'
            stack.append(item)
            stack.append(next_state.index)

        elif next_state.state == ParsingTableActionState.REDUCE:
            production_rule = self.__grammar.production_rules[next_state.index]
            output = 'Performed REDUCE: '
            for i in range(len(production_rule.rhs)):
                stack.pop()
                stack_item = stack.pop()
                output += f'{stack_item}, '

            output += f'into {production_rule.lhs}\n'
            next_state = self.__get_by_symbol(stack[-1], production_rule.lhs)
            stack.append(production_rule.lhs)
            stack.append(next_state.index)
            output += self.__perform(item, stack)

        elif next_state.state == ParsingTableActionState.ACCEPT:
            output = 'ACCEPTED\n'

        return output

    def parse(self, buffer: List[Symbol]) -> str:
        output = ''
        buffer.append(Dollar())
        stack = deque([0])
        for buffer_item in buffer:
            output += self.__perform(buffer_item, stack)

        return output
