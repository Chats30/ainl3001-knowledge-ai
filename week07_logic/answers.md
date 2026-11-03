# Week 7 — Knowledge Representation and Logical Reasoning: Answers

## Task 0 — Manual reasoning
Can we infer take_umbrella? Yes. The rule IF rainy THEN take_umbrella fires because rainy is a known fact.

Can we infer stay_dry? Yes. The rule IF take_umbrella THEN stay_dry needs take_umbrella, which was inferred in step 1. A conclusion from one rule triggers another rule (chaining).

Can we infer wear_coat? No. The rule needs rainy AND cold. We know rainy, but cold is not known, so the rule does not fire.

Order of discovery: take_umbrella first, then stay_dry.


## Task 1 — Represent facts
A Python set suits facts for these reasons:

- It stores each fact only once, so there are no duplicates.
- Membership checks (fact in facts) are fast.
- Order doesn't matter, and a knowledge base has no natural order.

Adding the same fact twice changes nothing. When cold is added, the rule IF rainy AND cold THEN wear_coat can fire, so wear_coat appears in the inferred facts.


## Task 2 — Represent rules
Each rule is a tuple of a list of conditions and a conclusion. The conditions mean AND, so all must be established before the conclusion follows. (["rainy", "cold"], "wear_coat") is the only rule with two conditions.


## Task 3 — Forward chaining
forward_chaining copies the starting facts into a new set so the original is not modified. It then loops over every rule. A rule fires only if all its conditions are already known, and its conclusion is added if it is new. The loop repeats until a full pass adds nothing. Repeating matters because a newly inferred fact can unlock another rule: take_umbrella is inferred first, which then lets stay_dry fire. The function returns the completed set of original and inferred facts.

With the starting facts rainy and weekday, the result is rainy, weekday, take_umbrella, stay_dry. wear_coat is not added because cold is unknown.


## Task 4 — Query the knowledge base
query checks whether the statement is in the completed fact set and returns True or False.

| Statement | Result | Why |
| --- | --- | --- |
| take_umbrella | True | inferred from rainy |
| stay_dry | True | inferred from take_umbrella |
| wear_coat | False | cold is not known |

False means "cannot be established from the available facts and rules". It does not mean the statement is false in the real world. With cold added to the facts, wear_coat becomes True. The original facts set still contains only the starting facts after forward_chaining runs.


## Task 5 — Backward chaining
Goal: stay_dry.

1. Which rule concludes it? IF take_umbrella THEN stay_dry.
2. What does it require? take_umbrella.
3. Which rule could establish that? IF rainy THEN take_umbrella.
4. Does the chain reach an initial fact? Yes, rainy is in the starting facts.

```
stay_dry  <-  take_umbrella  <-  rainy  (initial fact)
```

Forward chaining starts from known facts and asks what follows. Backward chaining starts from the goal and asks what must be true to prove it.


## Task 6 — Logic discussion
DOes IF rainy THEN take_umbrella have to be true in the real world? No. Someone might not own an umbrella, or it might be too windy to use one 

WHat assumptions do we make? We assume the rule is reliable and has no exceptions. We also assume the facts are accurate and the knowledge base is complete.

Logical inference vs statistical reasoning: logical inference gives certain conclusions from accepted rules. A statement is either established or not, with no degrees of belief. Statistical reasoning assigns probabilities when evidence is uncertain. ENtailment only says the conclusion follows from the knowledge base. it doesnt guarantee the knowledge base matches reality

## Reflection questions

1. What is logical entailment?
A conclusion is entailed by a knowledge base if it must be true whenever the knowledge base is true. it follows from the facts and rules under the logic's inference rules. It says nothing about whether the knowledge base is accurate.



2. How does forward chaining work?
It starts from the known facts. It checks each rule and, if all its conditions are known, adds the conclusion as a new fact. It repeats this until a full pass adds nothing new. The result is every fact that follows from the starting facts and rules.


3. How does backward chaining differ from forward chaining?
Backward chaining starts from a goal and works backwards. it finds a rule that concludes the goal, then tries to prove that rule's conditions. It continues until it reaches initial facts or fails. Forward chaining is data driven and explores everything that follows. Backward chaining is goal driven and only explores what is relevant to the goal.


4. What are the limitations of propositional logic?
Statements are indivisible symbols with no internal structure, so it can't express relationships like parent(alice, bob).
It has no variables or generalisation, so a rule like "a parent of a parent is a grandparent" needs a separate rule for every person.
Statements are only true or false, so it can't handle uncertainty, probabilities or exceptions.
It can't say "for all" or "there exists".
Rules can only be as good as what was written down, so incomplete knowledge gives silent "not established" results.

