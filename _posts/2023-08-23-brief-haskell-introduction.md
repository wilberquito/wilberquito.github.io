---
title: Brief Haskell Introduction
author: wilberquito
date: 2023-08-23 11:33:00 +0800
categories: [Programming, Haskell]
tags: [programming, fp, haskell, math]
pin: true
math: true
mermaid: true
---

*"Can programming be liberated from the von Neumann style?"*

Von Neumann programming languages, aka "imperative programming languages" use
variables to imitate the computer's storage cells; control statements elaborate
its jump and test instructions; and assignment statements imitate its fetching,
storing, and arithmetic.

Is there any good alternative to this?, yes there is! FP (functional
programming) is programming paradigm based on the principles of "Lambda
Calculus". Lambda Calculus is a computational formal system developed by Alonzo
Church that is based on functions abstraction, applications, variable binding
and substitution. This computational formal system  can be used to simulate any
Turing Machine.

![Light lambda img](/assets/img/2023-08-23-a-brief-haskell-introduction/lambda-light.png){: width="972" height="589" .light}
![Dark lambda img](/assets/img/2023-08-23-a-brief-haskell-introduction/lambda-dark.png){: width="972" height="589" .dark}
_Greek alphabet, lowercase lambda_

## Haskell

Haskell is a pure **functional programming** language known for **its
strong type system** and emphasis on **purity** and **immutability**. It's designed
to be **elegant**, **concise**, and **mathematically based**. Haskell key features
include **lazy evaluation**, **pattern matching**, and **type inference**, which
promote safer and expressive code.

## What you need to program in Haskell?

To program in Haskell you just 2 programs,

- A text editor
- A Haskell compiler

pick yourself your favorite text editor (by the way, mine is Neovim). There are
different alternatives to install a Haskell compiler, in this case we are using
[GHCup](https://www.haskell.org/ghcup/) which is a program that allows use to
install tools to work with different Haskell environments.

If you are using Linux, running the next command will be enough to install
interactively a Haskell compiler (ghc) and other tools.

```bash
$ curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
```

> Refer yourself to GHCup
> [install documentation](https://www.haskell.org/ghcup/install/) for any other
> OS system or installation problem.
{: .prompt-warning }

After the installation, from the terminal you can call the Haskell interpreter as follow:

```bash
$ ghci
ghci>
```

You can use `ghci` as a calculator,

```haskell
ghci> 2 + 5
"7"
```

but you take advantages from Haskell power when you write the logic on scripts.
To do so, here are some commands that you may find usuful to work with scripts
and the Haskell interpreter.

| Command                      | Description      |
|:-----------------------------|:-----------------|
| `:quit` or `:q`              | Quit the current interpreter session.    |
| `:load` or `:l`              | Load a script module.                    |
| `:reload` or `:r`            | Recompile the current loaded modules.    |
| `:+m`                        | Load multiple script modules.            |
| `:cd`                        | Change the current interpreter directory.|

Lets create a script module call `Main.hs` and define the funcion `main`. The
script module is under the download directory `~/Downloads`{: .filepath} for
example.

```haskell
main = do
  putStrLn "Hello Haskell!"
```
{: file="~/Downloads/Main.hs" }

To load the script module from any path we can do,

```haskell
ghci> :cd ~/Downloads/
ghci> :l Main.hs
ghci> main
"Hello Haskell!"
ghci> :r
"Ok, one module loaded."
ghci> :q
"Leaving GHCi."
```

## Functions

One of the basic blocks in Haskell are functions, functions in Haskell are
**mathematical functions**. In math, we often say things like $$f(x) = y$$,
meaning there’s some function $$f$$ that takes a parameter $$x$$ and maps to a
value $$y$$.

In mathematics, the application of functions is denoted by parenthesis.

$$ a - f(a, b) * c $$

In Haskell function application is denoted by space, for instance;

```haskell
ghci> a = 1 ; b = 2 ; c = 3 ; f = (+)
ghci> a - f a b * c
"-8"
```

> Function application denoted by space has maximum priority.
{: .prompt-info }

### Purity

Mathematical functions are pure, where its return value depends solely on its
input parameters, and they do not produce side effect as no mutation is
allowed. In Haskell as in math, if we define a function $$f$$ that takes as an
argument $$x$$, every evaluation of the application $$f(x)$$ return the same
$$y$$.

```haskell
ghci> double x = x * 2
ghci> f        = double
ghci> f 2
ghci> "4"
```

### Higher Order

In Haskell functions are considered first-class citizens, which means they can
be passed as arguments

```haskell
ghci> double x      = x * 2
ghci> computeBy f a = f a
ghci> computeBy double 3
ghci> "6"
```

, or being returned as values.

```haskell
ghci> double x  = x * 2
ghci> double'   = double
ghci> double' 2
ghci> "4"
```

### Order Reduction

The order reduction refers to the way an expression is reduced to another form.
There are basically two types of reductions, applicative reduction and normal
reduction. After we continue, lets define two simple functions in the Haskell
interpreter and application using the previous functions;

```haskell
ghci> add1    = x + 1
ghci> square  = x^2
```

We can express the `add1` function using Lambda Calculus as follow;

$$ A = (\lambda x. x + 1) $$

, and the `square` function as follow;

$$ S = (\lambda x. x^2) $$

Now, suppose we want to evaluate this lambda expression $$ S \ (A \ 2)$$
expression. In Haskell this expression could be written as;


```haskell
ghci> square (add1 2)
ghci> "9"
```

We are interested on how the expression `square (add1 2)` is reduced to `9`.
If Haskell would use **applicative reduction** (innermost redex), the order would proceed by
evaluating the sub-expressions and then applying the function, i.e.

$$
\begin{eqnarray}
& S \ (A \ 2) \\
& \lambda x. x^2 \left( \underline{ (\lambda x. x + 1) \ 2} \right) \\
by \ add1 \ definition \implies & \lambda x. x^2 \left( 2 + 1 \right) \\
by \ (+) \ operator \implies & \underline{ \lambda x. x^2 \ 3 }\\
by \ square \ definition \implies & 3^2 \\
by \ (\wedge) \ operator \implies & 9 \\
\end{eqnarray}
$$

Yet Haskell uses **normal order reduction** (outermost redex) which proceeds by
applying the function first and then evaluating the sub-expression, i.e.

$$
\begin{eqnarray}
& S \ (A \ 2) \\
& \underline{ \lambda x. x^2 \left( (\lambda x. x + 1) \ 2 \right) } \\
by \ square \ definition \implies & \left( \underline{ (\lambda x. x + 1) \ 2 } \right)^2  \\
by \ add1 \ definition \implies & \ (2 + 1)^2  \\
by \ (+) \ operator \implies & 3^2 \\
by \ (\wedge) \ operator \implies & 9 \\
\end{eqnarray}
$$

Normal order reduction comes with various advantages (although it is not
without its drawbacks, such as increased memory usage). Among its significant
benefits is that it ensures reaching a normal form if one exists in the
expression being reduced, as guaranteed by the Standardization Theorem. For
instance, consider the functions `inf` and `zero`. The former function
aligns with this principle as it generates the infinity number through
recursive processes. On the contrary, the latter function consistently
evaluates to zero, irrespective of its input value.

```haskell
ghci> inf       = 1 + inf
ghci> zero x    = 0
ghci> zero inf
ghci> "0"
```

If Haskell were to perform reduction in applicative order on the expression
`zero inf`, it would result in a hang. The reason for this is as previously
explained: applicative reduction order evaluates the arguments before the
functions. In this specific scenario, the evaluation of the argument leads to a
hang, i.e.

$$
\begin{eqnarray}
& zero \ inf \\
by \ inf \ definition \implies & zero \ (1 + inf)  \\
by \ inf \ definition \implies & zero \ (1 + (1 + inf))  \\
by \ inf \ definition \implies & zero \ (1 + (1 + (1 + inf)))  \\
& \cdot \ \cdot \ \cdot
\end{eqnarray}
$$

In normal order reduction this is trivial, i.e.

$$
\begin{eqnarray}
& zero \ inf \\
by \ zero \ definition \implies & 0  \\
\end{eqnarray}
$$

Another big benefits is that as argument expressions are passed without
evaluating them (pass by name), **any time a name is evaluated it gets
shared**. Every occurrence of the name points at the same potentially
unevaluated expression. To show how the sharing work, lets define a function
`square` that has one argument called `x`, we can also say that the function
`square` has bind the name `x`. Notice that `x` is used twice in the function
definition.

```haskell
ghci> square x = x * x
```

You may imagine that the evaluation of the expression `square (2 + 2)` is the following;


$$
\begin{eqnarray}
& square \ (2 + 2) \\
by \ square \ definition \implies & (2 + 2) * (2 + 2) \\
operator \ (*) \ forces \ left \ argument \implies & 4 * (2 + 2) \\
operator \ (*) \ forces \ right \ argument \implies & 4 * 4 \\
by \ (*) \ operator \implies & 16 \\
\end{eqnarray}
$$

However, what really happens is that the expression $$ 2 + 2 $$ referenced by
the name `x` is only computed once. The result of the evaluation is then shared
between all occurrences, i.e.

$$
\begin{eqnarray}
& square \ (2 + 2) \\
by \ square \ definition \implies & (2 + 2) * (2 + 2) \\
operator \ (*) \ forces \ left \ argument \implies & 4 * 4 \\
by \ (*) \ operator \implies & 16 \\
\end{eqnarray}
$$
