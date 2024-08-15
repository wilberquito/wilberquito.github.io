---
title: Harnessing the Power of C++ in Jupyter Notebooks with Xeus Cling
author: wilberquito
date: 2024-08-14 15:33:00 +0800
categories: [Technology, Jupyter Notebook]
tags: [xeus cling, jupyter kernel, jupyter, notebook, C++, docker]
pin: true
math: true
mermaid: true
image:
    path: /assets/img/2024-08-14-harnessing-the-power-of-cpp-in-jupyter-notebooks-with-xeus-cling/cpp-kernels-running.png
    alt: C++ kernels running on Jupyter Notebooks
---

Hey everyone! I’m thrilled to share an amazing discovery I made recently. Let
me give you a bit of context so you can appreciate how I stumbled upon this
gem. As a data scientist, I frequently use Jupyter Notebooks—a tool that’s
incredibly popular for its simplicity and versatility. It’s my go-to for
delivering explanatory data, building quick models, and even creating complete
executable programs. I’ve always loved how seamlessly it integrates text in
HTML and Markdown, and how it allows for interactive code execution. One of the
most powerful aspects, in my opinion, is how easy it is to use notebooks to
explain complex procedures to non-technical audiences.

Until recently, I believed Jupyter Notebooks only worked with interpreted
languages like Python or R—the staple languages in the exciting world of Data
Science. But I just discovered that I was wrong! While exploring the book
[Teaching and Learning with
Jupyter](https://jupyter4edu.github.io/jupyter-edu-book/), I learned that the
open-source community has developed a variety of kernels that support different
programming languages, including C++, Haskell, Scala, and many more. This opens up
a whole new world of possibilities, and I’m eager to dive in and explore them.
If you haven’t already, I highly recommend checking out this resource—it might
just change the way you think about Jupyter Notebooks!

To start, I decided to experiment with a compiled programming language because
I was genuinely curious about how it would function within Jupyter. I chose
C++—a language that brings back memories from my Computer Science degree days.
Back then, we didn't have the luxury of an interpreter to quickly test our
code; instead, we had to go through the tedious process of compiling it just to
see if our programs worked. I vividly remember how frustrating that was! So,
naturally, I was intrigued to see how C++ would integrate into the Jupyter
environment.

There are many kernels out there that work with C++ and Jupyter—check out [this
list](https://github.com/jupyter/jupyter/wiki/Jupyter-kernels) if you’re
looking for one for your favorite language. I decided to use [Xeus
Cling](https://github.com/jupyter-xeus/xeus-cling), which seems to be one of
the most popular kernels for working with C++.
