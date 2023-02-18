from copy import deepcopy


class DqlEngine:
    def __init__(self, rules, name=""):
        self.name = name
        self.rules = rules

    def _is_match(self, token, rules):
        if len(rules) > 0:

            rule = rules.pop(0)

            if rule[0] == 'type':
                # TODO implement in and like
                result = token[0] == rule[1]
                # if didn't match push the rule back on stack to match with next token
                if not result:
                    rules.insert(0, rule)
                return result

            elif rule[0] == 'value':
                # TODO implement in and like
                result = token[1] == rule[1]
                # if didn't match push the rule back on stack to match with next token
                if not result:
                    rules.insert(0, rule)
                return result

            elif rule[0] == 'skip':
                count = rule[1]
                # keep reducing count until 0, if at 0 mark the rule as consumed by not pushing it back
                count -= 1
                if count > 0:
                    rules.insert(0, ('skip', count - 1))
                return True

            elif rule[0] == 'after':
                count = rule[1]
                result = self._is_match(token, [rule[2]])

                # matched before min skips : fail immediately
                if result and count > 0:
                    return False

                if not result:
                    # reduce the match window and signal success for temporary continuation
                    count = count - 1 if count > 1 else 0
                    rules.insert(0, ('after', count, rule[2]))
                    return True
                else:
                    # matched after window : success
                    return True

            elif rule[0] == 'before':
                count = rule[1]
                result = self._is_match(token, [rule[2]])

                # matched after max skips : succeed immediately
                if result and count > 0:
                    return True

                if not result:
                    # reduce the match window and signal success for temporary continuation
                    count = count - 1 if count > 1 else 0
                    rules.insert(0, ('before', count, rule[2]))
                    return True
                else:
                    # matched after window : fail
                    return False

            elif rule[0] == 'between':
                min_count = rule[1]
                max_count = rule[2]
                result = self._is_match(token, [rule[3]])

                if result:
                    # matched before min skips : fail immediately
                    if min_count > 0:
                        return False
                    # matched after max skips : succeed immediately
                    elif max_count > 0:
                        return True

                if not result:
                    min_count = min_count - 1 if min_count > 1 else 0
                    max_count = max_count - 1 if max_count > 1 else 0

                    # update the window and signal temporary success since more attempts left in valid window
                    rules.insert(0, ('between', min_count, max_count, rule[2]))
                    return True

            elif rule[0] == 'or':
                result = False
                sub_rules = []
                for r in rule[1]:
                    res, sub_rule = self._is_match(token, r)
                    result = result or res
                    sub_rules = [*sub_rules, sub_rule]
                if not result:
                    rules.insert(0, rule)
                else:
                    rules.insert(0, ('or', sub_rules))
                return result

            else:
                raise SyntaxError(f"Unsupported rule {rule}")

        else:
            return False

    def match(self, match_tokens):
        rules = deepcopy(self.rules)
        matched = False
        while len(match_tokens) > 0 and len(rules) > 0:
            matched = self._is_match(match_tokens.pop(0), rules)
            if not matched:
                break
            elif len(rules) < 1:
                break
        return matched
