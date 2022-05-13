import os
import pickle
import string

import Sapphire.installversion as inst
import Sapphire.launch as lnch
import Sapphire.prelaunchchecks as check


def main(workingDir, isFrozen, resourceDir):
    check.launchcheck(workingDir)
    launcherversion, commands = info()
    interactiveloop(commands, launcherversion, workingDir, isFrozen, resourceDir)


def info():
    launcherversion = None  # I ditched this because I'm not releasing it yet so I'm not tracking until then
    commands = [["quit", "exit"], "launch", "install", ["help", "?"]]
    return launcherversion, commands


def ifwhatversions(workingDir):
    if os.path.exists(os.path.join(workingDir, "data", "installedversions.dat")):
        with open(
            os.path.join(workingDir, "data", "installedversions.dat"), "rb"
        ) as iV:
            instversions = pickle.load(iV)
            return instversions
    else:
        return "None"


def helpinfo(fcommands):
    print("? Commands : {}".format(", ".join(fcommands) + ","))
    print(
        "? Refer to the GitHub README.md or a wiki (when we have one) at https://github.com/Pyrotex7/Sapphire-Launcher for further info."
    )


def recursivelist(list2):
    def subrecursivelist(rlist):
        for val in rlist:
            if type(val) is list:
                for val2 in recursivelist(val):
                    yield val2

            else:
                yield val

    return [val for val in subrecursivelist(list2)]


def interactiveloop(commands, launcherversion, workingDir, isFrozen, resourceDir):

    fcommands = recursivelist(commands)

    print('\n# Sapphire Launcher - Type "?" or "help" for help.\n')

    while True:
        prompt = input("[] ")

        # For an empty command
        if "" == prompt.strip():
            print("! Empty command")
            continue

        # Invalid command
        elif prompt.rsplit()[0] not in fcommands:
            print("! Not a command")

        # Closing command
        elif prompt.strip() in commands[0]:
            print("* Closing...")
            break

        # Help command
        elif prompt.strip() in commands[3]:
            helpinfo(fcommands)

        # Install command
        elif commands[1] == prompt.rsplit()[0]:
            if 1 < len(prompt.rsplit()):
                version = prompt.rsplit()[1]
                checkversions = ifwhatversions(workingDir)
                if checkversions == "None":
                    if (
                        input(
                            "* No versions appear to be installed, would you like to install this one? (y/n): "
                        )
                        == "y"
                    ):
                        inst.install(version, workingDir, resourceDir)
                        if (
                            input(f"* Would you still like to launch {version}? (y/n): ")
                            == "y"
                        ):
                            lnch.launch(version, workingDir, isFrozen, resourceDir)
                        else:
                            print("* Returning...")
                    else:
                        print("* Returning...")
                elif version not in checkversions:
                    if (
                        input(
                            "* Version %s is not installed, would you like to install it? (y/n): "
                            % version
                        )
                        == "y"
                    ):
                        inst.install(version, workingDir, resourceDir)
                elif version in checkversions:
                    lnch.launch(version, workingDir, isFrozen, resourceDir)

            else:
                print("! No version provided")

            continue

        elif commands[2] == prompt.rsplit()[0]:
            if 1 < len(prompt.rsplit()):
                version = prompt.rsplit()[1]
                checkversions = ifwhatversions(workingDir)
                if checkversions == "None" or version not in checkversions:
                    inst.install(version, workingDir, resourceDir)
                else:
                    if (
                        input(
                            "* Version {} is already installed, would you like to launch this version? (y/n): ".format(
                                version
                            )
                        )
                        == "y"
                    ):
                        lnch.launch(version, workingDir, isFrozen, resourceDir)
