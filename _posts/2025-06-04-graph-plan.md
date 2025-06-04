---
title: Graph Plan, a propositional planner
author: wilberquito
date: 2025-06-04 15:21:00 +0800
categories: [Planning, SAT]
tags: [planning, encoding]
pin: true
math: true
mermaid: true
image:
    path: assets/img/2024-08-25-data_augmentation_e_commerce_opinion/t5-text-to-text-transformer.png
    alt: Diagram of text-to-text framework
---

## What is a Graph Plan?

**GraphPlan** is a **propositional planner**, meaning it operates without variables. This is a key distinction from other planning approaches, which must address issues like **unification** and other complexities that arise from the presence of variables.

However, a drawback of working with a **propositional representation** is that **all operator schemas must be fully instantiated**. This requires generating the **Cartesian product** of all possible variable assignments, which can significantly increase the size of the planning problem.

Once a GraphPlan of depth $k$ is constructed for a given problem, we attempt to extract a plan from it using the following process:

* Construct a plan graph of depth $k$
* Attempt to extract a valid plan (a solution)
* If no solution is found, increment $k$ and repeat

A plan of depth $k$ consists of $k$ **time steps**, where each step may include **parallel actions**. Thus, constructing a plan graph of depth $k$ corresponds to searching for a plan with $k$ time steps. The resulting plan is typically **partially ordered**, since some actions may be executed in parallel if they are not mutually exclusive.


## Planning complexity

For those of you who are interested in complexity stuff, scheduling is, in most
formulations, NP-complete. There are basically exponentially many schedules,
and in the worst case you have to try them all. But planning is worse. Planning
is P-space complete because sometimes you might have a very small description
of your problem so there are just a few very general-purpose operators, but the
plan itself might be quite long, so there's variability in the length of a plan as
well as in all the different operations that you might have to put in, so planning,
where you have to think about what all the different operations are, is
more complicated because you don't know the length of the plan.

## Components of a Graph Plan

As far as I know, the terminology used to describe the components of a graph plan can vary depending on the source you consult. However, based on the PDDL language, a plan consists of **operators** and **facts**. Both can be instantiated depending on the number of arguments they require.

The execution of an operator is referred to as an **action**, meaning that all its parameters have been instantiated. Similarly, when a fact is instantiated during execution, it is called a **fluent**.

A graph plan is composed of a sequence of alternating layers: **fact layers** and **action layers**. The **nodes** in the graph correspond to **propositions** and **actions**, and they are connected based on the definitions of the actions. The instantiation of an action $a_i^t$ is subject to a set of **preconditions**, and its execution yields a set of **effects**, where $a_i \in A^t$.

The `preconditions` and `effects` functions define how nodes in the graph are connected across layers: the preconditions of an action reside in layer $t-1$, while its effects appear in layer $t+1$:

$$
\begin{eqnarray}
\text{preconditions}(a_i^t) &=& \{p_j^{t-1} \mid p_j^{t-1} \in P^{t-1},\ p_j^{t-1} \in \text{preconditions}(a_i^t)\} \\
\text{effects}(a_i^t) &=& \{p_j^{t+1} \mid p_j^{t+1} \in P^{t+1},\ p_j^{t+1} \in \text{effects}(a_i^t)\}
\end{eqnarray}
$$


## Building a Graph Plan

To build a **Graph Plan**, the following steps should be followed:

1. **Initialize the graph with the initial state** of the problem, which consists of the set of propositions (facts) that are true at time step $t = 0$.

2. **Add applicable actions** to the graph. These are actions whose **preconditions** are satisfied in the current fact layer.

3. **Add the effects of these actions** to the next fact layer in the graph. An action can either **add** or **delete** a proposition. To keep the graph as compact as possible, we avoid duplicating propositions; instead, we add edges labeled as either `AddEffect` or `DeleteEffect` to distinguish how each action affects the proposition.

4. **Add maintenance actions** that connect propositions from the current fact layer to the next. These actions represent the persistence of a proposition's truth value over time—that is, the proposition remains true at step $t$ because it was true at step $t - 2$ and we did nothing to make it false.


### Mutually exclusive actions

If we leave the plan graph as it is, it simply represents the full search space of the problem up to a certain depth. However, the true advantage of using a plan graph lies in its ability to prune the search space by identifying and eliminating mutually exclusive actions—that is, actions that cannot be executed in parallel.

There are several reasons why actions might be mutually exclusive. The most common ones are:

1. **Interference**: This occurs when the effects of one action negate the preconditions of another action. For example, if one action adds a proposition that another action deletes, they cannot be executed together.

2. **Competing needs**: If there is a precondition of action $a$ and a precondition of action $b$ that are mutually exclusive.

## Solution extraction


A **solution to a Graph Plan** is a **subgraph** of the complete plan graph that includes all the necessary facts in both the **initial** and **goal** layers, and ensures that **no two operators in the same layer are mutually exclusive**. Since the structure of a plan graph closely resembles that of a **propositional formula**, it is possible to **automatically convert** a planning graph into **Conjunctive Normal Form (CNF)**, enabling the use of SAT solvers for plan extraction.

1. The initial state holds at layer 1 (fully specified), also the goals hold at the highest layer.

2. Operators imply their preconditions.
    $$
    \begin{eqnarray}
    LOAD(A,R,L,2) \implies (AT(A,L,1) \land AT(R,L,1))
    \end{eqnarray}
    $$


3. Each fact at level $i$ implies the disjunction of all operators at level $i-1$ that can produce it.
    $$
    \begin{eqnarray}
    IN(A,R,3) \implies (LOAD(A,R,L,2) \lor LOAD(A,R,P,2) \lor MAINTAIN(IN(A,R),2))
    \end{eqnarray}
    $$

4. Conflicting actions are mutually exclusive.
    $$
    \begin{eqnarray}
    \neg LOAD(A,R,L,2) \lor \neg LOAD(A,R,P,2)
    \end{eqnarray}
    $$




