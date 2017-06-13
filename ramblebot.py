#######################################################
#
# ###Ramblebot###
# Bot that creates random sentences using a context free grammar
#
# Heavily structured off of this article:
# http://eli.thegreenplace.net/2010/01/28/generating-random-sentences-from-a-context-free-grammar
#
#
#######################################################

from collections import defaultdict
import random

class CFG(object):
    def __init__(self):
        self.prod = defaultdict(list)
		
    def add_prod(self, lhs, rhs):
        """ Add production to the grammar. 'rhs' can
            be several productions separated by '|'.
            Each production is a sequence of symbols
            separated by whitespace.
            Usage:
                grammar.add_prod('NT', 'VP PP')
                grammar.add_prod('Digit', '1|2|3|4')
        """
        prods = rhs.split('|')
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))

    def gen_random(self, symbol):
        """ Generate a random sentence from the
            grammar, starting with the given
            symbol.
        """
        sentence = ''

        # select one production of this symbol randomly
        rand_prod = random.choice(self.prod[symbol])

        for sym in rand_prod:
            # for non-terminals, recurse
            if sym in self.prod:
                sentence += self.gen_random(sym)
            else:
                sentence += sym + ' '

        return sentence
		
    def gen_random_convergent(self, symbol, cfactor=0.25, pcount=defaultdict(int)):
        """ Generate a random sentence from the
            grammar, starting with the given symbol.
            Uses a convergent algorithm - productions
            that have already appeared in the
            derivation on each branch have a smaller
            chance to be selected.
            cfactor - controls how tight the
            convergence is. 0 < cfactor < 1.0
            pcount is used internally by the
            recursive calls to pass on the
            productions that have been used in the
            branch.
        """
        sentence = ''

        # The possible productions of this symbol are weighted
        # by their appearance in the branch that has led to this
        # symbol in the derivation
        #
        weights = []
        for prod in self.prod[symbol]:
            if prod in pcount:
                weights.append(cfactor ** (pcount[prod]))
            else:
                weights.append(1.0)

        rand_prod = self.prod[symbol][weighted_choice(weights)]

        # pcount is a single object (created in the first call to
        # this method) that's being passed around into recursive
        # calls to count how many times productions have been
        # used.
        # Before recursive calls the count is updated, and after
        # the sentence for this call is ready, it is rolled-back
        # to avoid modifying the parent's pcount.
        #
        pcount[rand_prod] += 1

        for sym in rand_prod:
            # for non-terminals, recurse
            if sym in self.prod:
                sentence += self.gen_random_convergent( sym, cfactor=cfactor, pcount=pcount)
            else:
                sentence += sym + ' '

        # backtracking: clear the modification to pcount
        pcount[rand_prod] -= 1
        return sentence
		
def weighted_choice(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i
		
cfg = CFG()
cfg.add_prod('S', 'S | S L S' )
cfg.add_prod('S', 'PN VP | Q AV PN VP ?')
cfg.add_prod('NP', 'Det N | Det A N')
cfg.add_prod('PN', 'I | he | she | Jess | you')
cfg.add_prod('VP', 'V NP | V')
cfg.add_prod('Det', 'a | the | my | his | her | our | your')
cfg.add_prod('N', 'desk | car | cat | dog | cow | building | shoe')
cfg.add_prod('V', 'kick | follow | eat | hit | knock over | sneeze on | chew on | run over | love | hate | know')
cfg.add_prod('L', 'because | but | for | since | and | or | yet | so ')
cfg.add_prod('Q', 'who | what | when | where | why | how')
cfg.add_prod('AV', 'did | are | will')
cfg.add_prod('A' , 'furry | small | big | soft | nice | mean')


for i in range(10):
	print(cfg1.gen_random_convergent('S'))