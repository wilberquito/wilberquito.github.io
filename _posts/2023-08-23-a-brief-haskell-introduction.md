*"Can programming be liberated from the von Neumann style?"*

Von Neumann programming languages, aka "imperative programming languages" use
variables to imitate the computer's storage cells; control statements elaborate
its jump and test instructions; and assignment statements imitate its fetching,
storing, and arithmetic.

Is there any good alternative to this?, yes there is! FP (funcitonal
programming) is programming paradigm based on the principles of "Lambda
Calculus". Lambda Calculus is a computational formal system developed by Alonzo
Church that is based on functions abstraction, applications, variable binding
and substitution. This computational formal system  can be used to simulate any
Turing Machine.

![Desktop View](/assets/img/2023-08-23-a-brief-haskell-introduction/lambda.png){: width="972" height="589" }
_Greek alphabet, lowercase lambda_

## Haskell

Haskell is a pure **functional programming** language known for **its
strong type system** and emphasis on **purity** and **immutability**. It's designed
to be **elegant**, **concise**, and **mathematically based**. Haskell's key features
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

If you are using Linux, running the next command will be enought to install
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
