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

![Light lambda img](/assets/img/2023-08-23-brief-haskell-introduction/lambda-light.png){: width="972" height="589" .light}
![Dark lambda img](/assets/img/2023-08-23-brief-haskell-introduction/lambda-dark.png){: width="972" height="589" .dark}
_Greek alphabet, lowercase lambda_

## Haskell

Haskell is a pure **functional programming** language known for **its
strong type system** and emphasis on **purity** and **immutability**. It's designed
to be **elegant**, **concise**, and **mathematically based**. Haskell key features
include **lazy evaluation**, **type inference** and much more, which
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

```
ghci> 2 + 5
7
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

```
main = do
  putStrLn "Hello Haskell!"
```
{: file="~/Downloads/Main.hs" }

To load the script module from any path we can do,

```
ghci> :cd ~/Downloads/
ghci> :l Main.hs
ghci> main
Hello Haskell!
ghci> :r
Ok, one module loaded.
ghci> :q
Leaving GHCi.
```

## Functions

One of the basic blocks in Haskell are functions, functions in Haskell are
**mathematical functions**. In math, we often say things like $$f(x) = y$$,
meaning there’s some function $$f$$ that takes a parameter $$x$$ and maps to a
value $$y$$.

In mathematics, the application of functions is denoted by parenthesis.

$$ a - f(a, b) * c $$

In Haskell function application is denoted by space, i.e.

```
ghci> a = 1 ; b = 2 ; c = 3 ; f = (+)
ghci> a - f a b * c
-8
```

> Function application denoted by space has maximum priority.
{: .prompt-info }

### Purity

Mathematical functions are pure, where its return value depends solely on its
input parameters, and they do not produce side effect as no mutation is
allowed. In Haskell as in math, if we define a function $$f$$ that takes as an
argument $$x$$, every evaluation of the application $$f(x)$$ return the same
$$y$$.

```
ghci> double x = x * 2
ghci> f        = double
ghci> f 2
ghci> 4
```

### Higher Order

In Haskell functions are considered first-class citizens, which means they can
be passed as arguments

```
ghci> double x      = x * 2
ghci> computeBy f a = f a
ghci> computeBy double 3
ghci> 6
```

, or being returned as values.

```
ghci> double x  = x * 2
ghci> double'   = double
ghci> double' 2
ghci> 4
```

### Order Reduction

The order reduction refers to the way an expression is reduced to another form.
There are basically two types of reductions, applicative reduction and normal
reduction. After we continue, lets define two simple functions in the Haskell
interpreter and application using the previous functions;

```
ghci> add1    = x + 1
ghci> square  = x^2
```

We can express the `add1` function using Lambda Calculus as follow.

$$ A = (\lambda x. x + 1) $$

, and the `square` function as follow.

$$ S = (\lambda x. x^2) $$

Now, suppose we want to evaluate this lambda expression $$ S \ (A \ 2)$$
expression. In Haskell this expression could be written as;


```
ghci> square (add1 2)
ghci> 9
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

```
ghci> inf       = 1 + inf
ghci> zero x    = 0
ghci> zero inf
0
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
`square` has bounded the name `x`.

```
ghci> square x = x * x
```

You may imagine that the evaluation of the expression `square (2 + 2)` is the following;

$$
\begin{eqnarray}
& square \ (2 + 2) \\
by \ square \ definition \implies & (2 + 2) * (2 + 2) \\
operator \ (*) \ forces \ left \ expression \implies & 4 * (2 + 2) \\
operator \ (*) \ forces \ right \ expression \implies & 4 * 4 \\
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
operator \ (*) \ forces \ left \ expression \implies & 4 * 4 \\
by \ (*) \ operator \implies & 16 \\
\end{eqnarray}
$$

## Lazy Evaluation

In Haskell, expression are only evaluated when they are really needed. When we
say a expression is needed, we refer to the fact that a expression need to be
computed to produce value.

Consider the lambda abstraction $$F$$, which is defined to take two arguments
and return the first one:

$$
F = \lambda x, y. \ x
$$

In order to fully evaluate the abstraction $$F$$, it must be applied with two
arguments. However, it's important to note that the definition of $$F$$ only
employs the first argument while ignoring the second argument. The lambda
abstraction's structure includes both $$x$$ and $$y$$ as parameters, but when the
function is applied, it only utilizes $$x$$ in its definition.

Consider now the definition of the data structure list, a list that can be defined
recursively, i.e.

$$
List = Empty \ | \ L : List
$$

As you can imagine, by this definition we can create an infinite list, i.e.

$$
L : (L : (L : ( L : ( \cdot \ \cdot \ \cdot ))))
$$

Moreover, the process of evaluating an infinite list inevitably demands an
infinite duration. In the Haskell, generating an infinite
list of numbers is remarkably simple:

```
ghci> numbers = [1..]
```

In this scenario, the generation of this infinite list functions as an
expression. Since no immediate evaluation of this expression is required, the
interpreter remains unaffected and doesn't stall. However, **when we request the
presentation of the list, we effectively compel the evaluation of the
expression**. Consequently, as anticipated, the process comes to a halt:

```
ghci> numbers
[1, 2, 3, 4, 5, 6, ...]
```

The same principle applies to the lambda abstraction $$F$$, where the second
argument remains unused and thus not computed. Bellow we exemplify this
phenomenon in a Haskell context.


In this instance, when the infinite list of numbers is employed as the second
argument of function `f`, the interpreter proceeds without any issue:

```
ghci> numbers = [1..]
ghci> f a b = a
ghci> f (2 + 2) numbers
4
```

However, it's important to note that when the roles are reversed and the
infinite list is passed as the first argument to function `f`, the
interpreter will halt. This is a consequence of the
evaluation mechanism for infinite lists.

```
ghci> numbers = [1..]
ghci> f a b = a
ghci> f numbers (2 + 2)
[1, 2, 3, 4, 5, 6, ...]
```

## Variables

In Haskell, what are referred to  "variables" defy the conventional
understanding of variables in imperative programming. Abiding by the principle
of transformation over mutability, Haskell employs immutable variables. A
better way to refer to variables in Haskell is "values" or "names".

Hence, attempting to modify any value's state as demonstrated in the following
script module will lead to an error involving multiple bindings.

```
main = do
  let x = 1
      x = 2
  return ()
```
{: file="~/Downloads/DummyError.hs" }

```
ghci> :cd ~/Downloads/
ghci> :l DummyError.hs
[1 of 1] Compiling Main             ( DummyError.hs, interpreted )

DummyError.hs:2:7: error:
    Conflicting definitions for ‘x’
    Bound at: DummyError.hs:2:7
              DummyError.hs:3:7
  |
2 |   let x = 1
  |       ^^^^^.
```

## Types

Haskell compiler ensures that every expression in the program has a
well-defined type, and **type's expressions are checked at compile-time**.
Inconsistent use of types leads to type errors.

What are types by the way?, intuitively, we can think of **types as sets of
values and a set of allowed operations on those values**.

In Haskell, types are capitalized. Here you have some built-in types.

|       Type        |          Literals          |                                  Use                                   |                  Operations                   |
| :---------------: | :------------------------: | :--------------------------------------------------------------------: | :-------------------------------------------: |
|        Int        |          1, 2, -3          |                      Number type (signed, 64bit)                       |       +, -, \*, div, mod, fromIntegral        |
|      Integer      | 1, -2, 900000000000000000  |                         Unbounded number type                          | +, -, \*, div, mod, fromInteger, fromIntegral |
|       Float       |         0.1, 1.2e5         |                         Floating point numbers                         |               +, -, \*, /, sqrt               |
|      Double       |         0.1, 1.2e5         | Floating point numbers. Aproximations are more precise than Float type |               +, -, \*, /, sqrt               |
|       Bool        |        True, False         |                              Truth values                              |           &&, \|\|, not, otherwise            |
|       Char        | 'a', 'Z', '\n', '\t', '\\' |  Represents a character (a letter, a digit, a punctuation mark, etc)   | ord, chr, isAlpha, isDigit, isUpper, isLower  |
| String aka [Char] |         "abcd", ""         |                         Strings of characters                          |                  reverse, ++                  |


As every expression in Haskell has its own type, the compiler can reason quite a lot about
our programs before run them unlike other programming languages.
One of the most powerful features of Haskell is that it **supports type inference**.

Most of the times, Haskell by its own can infer the type of expressions, so we
do not need to explicitly write out the types of our functions and expressions
to get things done, e.g.

```
ghci> :t 'a'
'a' :: Char
ghci> :t True
True :: Bool
ghci> :t "HELLO!"
HELLO!" :: [Char]
ghci> :t (True, 'a')
(True, 'a') :: (Bool, Char)
ghci> :t 4 == 5
4 == 5 :: Bool
ghci> :t (+)
(+) :: Num a => a -> a -> a
```

**Many of the type's operations are defined for a big group of types in a
typeclass**. A typeclass is a sort of interface that defines some
behavior. If a type is an instance of a typeclass, then that type supports and
implements the behavior that the typeclass describes.

Lets see for example, the equal operation and how multiple types define this
operation. It make sense to compare String with String and Int with and Int,
but no a String with an Int, right?

```
ghci> "hello" == "hello"
True
ghci> "Hello" == "hellO"
False
ghci> 1 == 1
True
ghci> 1 == 0
False
```

But if you try to compare different types, Haskell compiler will blame you:

```
ghci> 1 == "one"

<interactive>:5:1: error:
    • No instance for (Num String) arising from the literal ‘1’
    • In the first argument of ‘(==)’, namely ‘1’
      In the expression: 1 == "one"
      In an equation for ‘it’: it = 1 == "one"
```

Why is that?, well to reason about it, lets ask to Haskell compiler information
about the `(==)` operator.

```
ghci> :i (==)
type Eq :: * -> Constraint
class Eq a where
  (==) :: a -> a -> Bool
  ...
        -- Defined in ‘GHC.Classes’
infix 4 ==
```

The `(==)` operator functions as a binary operator, defined in the typeclass
`Eq`. The operator accepts two arguments of the type `a` and yields a `Bool`
result. **What is the implication of `a` in this context?** It serves as a
**type variable** or **type placeholder**, signifying that the provided
argument can assume any type, given the absence of specific type constraints in
this case.

Alright, we have now established the existence of this typeclass. However, it's
intriguing to understand how the `Int` and `String` types are able to exhibit
the characteristics outlined in the `Eq` typeclass. This phenomenon is achieved
through a procedure known as **instantiation**, which we'll delve into in a
future article.

For now, it is enough if you know that these types are instances of `Eq`.
And if you do not believe it, we can ask the compiler, e.g.

```
ghci> :i Int
type Int :: *
data Int = GHC.Types.I# GHC.Prim.Int#
        -- Defined in ‘GHC.Types’
instance Eq Int -- Defined in ‘GHC.Classes’
instance Ord Int -- Defined in ‘GHC.Classes’
instance Enum Int -- Defined in ‘GHC.Enum’
instance Num Int -- Defined in ‘GHC.Num’
instance Real Int -- Defined in ‘GHC.Real’
instance Show Int -- Defined in ‘GHC.Show’
instance Read Int -- Defined in ‘GHC.Read’
instance Bounded Int -- Defined in ‘GHC.Enum’
instance Integral Int -- Defined in ‘GHC.Real’
```

The signature `instance Eq Int` explicitly informs us that any value of type
`Int` can use the behaviors defined in the class `Eq`.

## Resume

This article provides an overview of an alternative programming paradigm,
focusing on the renowned programming language Haskell, in contrast to the
conventional von Neumann programming approach. In the von Neumann style,
variables and control flow simulate computer architecture. In contrast,
Functional Programming, deeply rooted in Lambda Calculus, offers a distinct
approach. Haskell serves as a prime example of this approach, emphasizing
principles such as purity, immutability, and a strong mathematical foundation.

In Haskell, functions closely resemble mathematical functions, ensuring
uniformity and predictability. The language supports advanced features like
higher-order capabilities, order reduction, and lazy evaluation, all of which
contribute to optimizing efficiency in program execution.

Rather than traditional mutable variables, Haskell employs immutable
"variables" as values or names. Its type system actively enforces type safety,
with support for type inference. The concept of typeclasses defines specific
behaviors, such as the `Eq` typeclass for equality comparison. Notably, types
that become instances of these typeclasses, inheriting their
associated behaviors.
