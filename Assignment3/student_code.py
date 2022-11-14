import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact or Rule) - Fact or Rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_rule):
        """Retract a fact or a rule from the KB

        Args:
            fact_rule (Fact or Rule) - Fact or Rule to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_rule])
        ####################################################
        # Student code goes here
        if factq(fact_rule):
            for each_fact in self.facts:
                if fact_rule == each_fact:
                    fact_rule = each_fact
                    break
        else:
            for each_rule in self.rules:
                for each_rule in self.rules:
                    if fact_rule == each_rule:
                        fact_rule = each_rule
                        break
        
        if fact_rule.asserted:
            if fact_rule.supported_by:
                for each_pair in fact_rule.supported_by:
                    if each_pair[0] not in self.rules or each_pair[1] not in self.facts:
                        fact_rule.supported_by.remove(each_pair)
                if fact_rule.supported_by:
                    fact_rule.asserted = False
            else:
                if factq(fact_rule):
                    self.facts.remove(fact_rule)
                else:
                    self.rules.remove(fact_rule)
                for supports_fact in fact_rule.supports_facts:
                    if len(supports_fact.supported_by) == 1:
                        self.kb_retract(supports_fact)
                    elif len(supports_fact.supported_by) > 1:
                        for each_pair in supports_fact.supported_by:
                            if fact_rule in each_pair:
                                supports_fact.supported_by.remove(each_pair)

                for supports_rule in fact_rule.supports_rules:
                    if len(supports_rule.supported_by) == 1:
                        self.kb_retract(supports_rule)
                    elif len(supports_rule.supported_by) > 1:
                        for each_pair in supports_fact.supported_by:
                            if fact_rule in each_pair:
                                supports_rule.supported_by.remove(each_pair)

        else:
            for each_pair in fact_rule.supported_by:
                if each_pair[0] not in self.rules or each_pair[1] not in self.facts:
                    fact_rule.supported_by.remove(each_pair)
            if not fact_rule.supported_by:
                if factq(fact_rule):
                    self.facts.remove(fact_rule)
                else:
                    self.rules.remove(fact_rule)
                for supports_fact in fact_rule.supports_facts:
                    self.kb_retract(supports_fact)
                for supports_rule in fact_rule.supports_rules:
                    self.kb_retract(supports_rule)


class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here
        curr_bindings = match(fact.statement, rule.lhs[0])
        if not curr_bindings:
            return

        created_supported_by = [[rule, fact]]
        created_rhs = instantiate(rule.rhs, curr_bindings)
        if len(rule.lhs) == 1:
            created_fact = Fact(created_rhs, created_supported_by)
            kb.kb_add(created_fact)
            fact.supports_facts.append(created_fact)
            rule.supports_facts.append(created_fact)
        else:
            created_lhs = []
            for statement in rule.lhs[1:]:
                created_lhs.append(instantiate(statement, curr_bindings))
            created_rule = Rule([created_lhs, created_rhs], created_supported_by)
            kb.kb_add(created_rule)
            fact.supports_rules.append(created_rule)
            rule.supports_rules.append(created_rule)
