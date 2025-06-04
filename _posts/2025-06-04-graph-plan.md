---
title: A propositional planner
author: wilberquito
date: 2025-06-04 15:21:00 +0800
categories: [Planning, SAT]
tags: [planning, encoding, kissat]
pin: true
math: true
mermaid: true
image:
    path: assets/img/2024-08-25-data_augmentation_e_commerce_opinion/t5-text-to-text-transformer.png
    alt: Diagram of text-to-text framework
---

Graph Plan is a propositional planner, in other words, there are no variables. This is a key difference
to other planners that they do  need to worry about unification
an other problems araising from the existences of variables.

One of the backwards of Graph Plan is that working with propositional representation,
we need to instantiate per every variable in the relationship, meaning that
we are force to do a cartesian product of the variables to instantiate a relationship between variables.

Once we build a Graph Plan of depth $k$, we can obtain a planning of the planning problem. We do as follow:

* Make a plan graph of depth $k$
* Search for a solution
* If not solution found $k = k + 1$

A plan of depth $k$ has $k$ times steps and may have parallel actions per time step. Making a plan graph of depth $k$
means finding a planning solutions of $k$ times steps but it will be partially ordered because some actions might possible
take place in a single time step.


## Planning complexity

For those of you who are interested in complexity stuff, scheduling is, in most
formulations, NP complete. There are basically exponentially many schedules,
and in the worst case you have to try them all. But planning is worse. Planning
is P-space complete because sometimes you might have a very small description
of your problem so there are just a few very general-purpose operators, but the
plan itself might be quite long, so there's variability in the length of a plan as
well as in all the different operations that you might have to put in, so planning,
where you have to have to think about what all the different operations are, is
more complicated because you don't know the length of the plan

* Planning: find steps and schedule (PSPACE-complete)
* Scheduling: tasks are fixed (NP-complete)










