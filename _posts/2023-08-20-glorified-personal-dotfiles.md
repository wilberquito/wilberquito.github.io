---
title: A Glorified Personal Dotfiles
author: wilberquito
date: 2023-08-20 11:33:00 +0800
categories: [Technology, Linux]
tags: [dotfiles, linux, environment]
pin: true
math: true
mermaid: true
---


This post aims to unveil the remedy for a recurring issue I've encountered each
time I've had to set up a fresh Linux OS from scratch. I find great ease in
conducting my entire workflow within the terminal. However, achieving this
level of comfort necessitates the installation of specific programs and
configurations. This process typically consumes a significant amount of time,
and due to my limited memory capacity (dummy hehe), it becomes challenging to
recall all the program names and references for the required configurations.

This solution is available on GitHub within [this
repository](https://github.com/wilberquito/dotfiles). Feel free to fork the
repository and make necessary modifications to tailor the files according to
your requirements.

## Overview

The solution consists of three main steps:

1. Program Installation
2. Configuration Linking
3. Operating System Bootstrapping

## Program Installation

The initial step, of course, involves the installation of the necessary
programs. For the majority of installations, I rely on
[dnf](https://docs.fedoraproject.org/en-US/quick-docs/dnf/); however, there are
instances where a program might not be present in the package registry of this
package manager, or you might prefer to acquire it from GitHub or using an
alternative package manager. To accommodate these situations, I execute the
installation of each program using individual shell or bash scripts. It's up to
you to determine the installation method for each program. The installation
script for each program is stored within the `install/`{: .filepath} directory.

As an illustration, the installation process for my preferred terminal,
[kitty](https://sw.kovidgoyal.net/kitty/), would involve crafting a unique
script, such as `install/kitty.sh`{: .filepath}, containing the subsequent content:

```bash
if test ! $(which kitty)
then
	echo "	Installing kitty for you."
	dnf -y install kitty
fi

exit 0
```

Once you've crafted all the scripts for program installations, navigate to the
`script/`{: .filepath} directory and execute the following command as a sudo
user:

```bash
$ sudo ./install
```

Go ahead and fix yourself a cup of coffee while you patiently await the
completion of the program installations. By the time your coffee is ready, your
software will be too! Just remember, even code needs a moment to caffeinate
itself.

> It is essential that the scripts you've created for program installations are designed to operate without any user interaction.
{: .prompt-warning }

## Configuration Linking

To properly elucidate this section, a clear understanding of what a symbolic
link is becomes crucial. In the realm of operating systems, a symbolic link
refers to a file-object that serves as a pointer to another object. Now, why
does this matter? Well, the significance lies in the fact that symbolic links
empower us to construct centralized configuration solutions, which can be
directed from the anticipated pathway. In essence, symbolic links act as
bridges that seamlessly connect different locations, allowing for organized and
streamlined management of configurations.

If you haven't already noticed, the configurations for most programs are tucked
away in hidden files, often referred to as dotfiles. These files are scattered
across various locations within your system. Commonly, you'll find them either
directly under your home directory, such as `/home/<user>/`{: .filepath}, or
nestled within the concealed `.config/`{: .filepath} directory within your home path,
specifically `/home/<user>/.config/`{: .filepath}. These inconspicuous locations house the
inner workings of programs, orchestrating their behaviors and settings.

Whether you're dealing with a single file or an entire folder, the critical
factor is the placement of these configurations. If the configurations belong
under your home path, that is, `/home/<user>/`{: .filepath}, you should
incorporate them into the `symbolic/home/`{: .filepath} path. Conversely, for
configurations nestled within the `/home/<user>/.config/`{: .filepath}
directory, they should find their home within the `symbolic/home/`{: .filepath}
path as well. In essence, it's about ensuring that these symbolic links
appropriately mirror the original configuration locations, maintaining a
harmonious structure for your system's settings.

> It's important to note that the files and directories intended for creating
> symbolic links must conclude with the `.symlink` extension.
{: .prompt-warning }

Once you have included all the necessary configuration files and directories,
proceed to the `script/`{: .filepath} directory and initiate the subsequent
command:

```bash
$ ./symlink
```

> The `symlink` program operates interactively. Upon encountering an existing
configuration file or folder, it engages in a dialogue, offering you options to
either create a backup, remove the existing item, or skip the creation of the
symbolic link altogether. This interactive approach ensures that you have
control over how the symbolic links are established, preventing accidental
overwrites or disruptions to your existing configurations.
{: .prompt-info }


## Operating System Bootstrapping

Given that the installation of programs is designed to be non-interactive with
the user, there might be instances where you'll need to run these programs
post-installation for self-configuration, installation of additional programs,
or logging into online platforms.

These post-installation tasks can be managed by modifying the
`script/bootstrap`{: .filepath} script. Once the necessary edits are complete,
proceed to the `script/`{: .filepath} directory and execute the following
command (you might need to elevate to superuser privileges):

```bash
# sudo ./bootstrap
$ ./bootstrap
```

This process will ensure that any actions required after the initial
installation can be seamlessly integrated into your system setup.
