---
title: Harnessing the Power of C++ in Jupyter Notebooks with Xeus Cling
author: wilberquito
date: 2024-08-14 15:33:00 +0800
categories: [Technology, Jupyter]
tags: [xeus cling, jupyter kernel, jupyter, notebook, C++, docker]
pin: true
math: true
mermaid: true
image:
    path: /assets/img/2024-08-14-harnessing-the-power-of-cpp-in-jupyter-notebooks-with-xeus-cling/cpp-kernels-running.png
    alt: C++ kernels running on Jupyter server
---

Hey everyone! I want to share an amazing discovery I made recently about
Jupyter Notebook. Let me give you a bit of context so you can appreciate how I
stumbled upon this gem. As a data scientist, I frequently use Jupyter
Notebooks—a tool that’s incredibly popular for its simplicity and versatility.
It’s my go-to for delivering explanatory data, building quick models, and even
creating complete executable programs. I’ve always loved how seamlessly it
integrates text in HTML and Markdown, and how it allows for interactive code
execution. One of the most powerful aspects, in my opinion, is how easy it is
to use notebooks to explain complex procedures to non-technical audiences.

Until recently, I believed Jupyter Notebooks only worked with interpreted
languages like Python or R—the staple languages in the exciting world of Data
Science. But I just discovered that I was wrong! While exploring the book
[Teaching and Learning with
Jupyter](https://jupyter4edu.github.io/jupyter-edu-book/){:target="_blank"}, I learned that the
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
list](https://github.com/jupyter/jupyter/wiki/Jupyter-kernels){:target="_blank"}. if you’re
looking for one for your favorite language. I decided to use [Xeus
Cling](https://github.com/jupyter-xeus/xeus-cling){:target="_blank"}, which seems to be one of
the most popular kernels for working with C++.

To simplify the process of using the C++ in Jupyter and get
everything up and running quickly—without the hassle of installations and
figuring out which tools to install on your machine—I’ve made a
[template repository](https://github.com/wilberquito/xeus-cpp-kernel){:target="_blank"} available. It
includes a Dockerfile that allows you to create an image with everything
bundled together. You’ll need Docker for this, but once you’ve got it set up,
all the instructions are laid out in the README. After running the image, you
can connect to the C++ kernels through Jupyter directly from your browser, with
everything running smoothly in a virtual environment inside the container.


![Accessing server](/assets/img/2024-08-14-harnessing-the-power-of-cpp-in-jupyter-notebooks-with-xeus-cling/jupyter-access-server.png)
_Jupyter server running_

In your browser, if you've cloned the example repository, you should see
something similar to the image below when you access the Jupyter server.

![Template repository](/assets/img/2024-08-14-harnessing-the-power-of-cpp-in-jupyter-notebooks-with-xeus-cling/preview-cpp-project.png)
_Xeus C++ template repository snapshot_


![Available C++ kernels](/assets/img/2024-08-14-harnessing-the-power-of-cpp-in-jupyter-notebooks-with-xeus-cling/cpp-kernels-available.png){: width="972" height="589" .w-25 .right}

If you've set up the volume correctly, you can modify existing notebooks and
create new ones using the different C++ kernels available—without worrying
about losing your work when the container stops running.

That's all, folks! Now you can implement and execute C++ code quickly, with
immediate, visible results, all within Jupyter Notebooks.
