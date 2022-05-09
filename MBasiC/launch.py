import subprocess
import os
import pickle

from MBasiC.authuser import authenticate


def launch(version, workingDir, isFrozen, resourceDir):
    # Main launch handler
    authdata = authenticateuser(workingDir)

    if authdata.status == 0:
        authtoken, username, uuid = authdata.authtoken, authdata.username, authdata.uuid
    elif authdata.status == 1:
        print("! %s" % authdata.error)
        return "Failed"

    launch = constructcommand(
        version, authtoken, username, uuid, workingDir, isFrozen, resourceDir
    )

    print("* Launching...")

    launchcommand = subprocess.Popen(
        launch,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = launchcommand.communicate()
    if launchcommand.returncode != 0:
        print("! Launch failed with exit code %s" % launchcommand.returncode)
        print(
            "* The full log will be saved to your minecraft directory. Refer to the offical GitHub at https://github.com/Pyrotex7/MBasiC page for instruction on how to find this."
        )
        if input("* Would you like to see the full log now? (y/n): ") == "y":
            print(stderr)
            print(stdout)


def authenticateuser(workingDir):
    def manualcredentials():
        email = input("Email (or legacy username):\t")
        password = input("Password:\t")
        type = input("Account type:\t")
        return [email, password, type]

    if os.path.exists(os.path.join(workingDir, "auth.txt")):
        with open(os.path.join(workingDir, "auth.txt"), "r") as authfile:
            try:
                authargs = authfile.readlines()
                email = authargs[0].strip()
                password = authargs[1].strip()
            except:
                print(
                    "! Your auth.txt file was not formatted properly. Please enter your username and password manually to launch."
                )
                email, password = manualcredentials()
    else:
        email, password, type = manualcredentials()

    authrequest = authenticate(email=email, password=password, accounttype=type)

    return authrequest


def constructcommand(
    version, authtoken, username, uuid, workingDir, isFrozen, resourceDir
):

    with open(
        os.path.join(
            workingDir,
            "game",
            "{}_vanilla_install".format(version),
            "installdata_{}.dat".format(version),
        ),
        "rb",
    ) as installdata:
        installlaunchdata = pickle.load(installdata)

    launchinputlist = [
        installlaunchdata["mainclass"],
        "--username",
        username,
        "--version",
        version,
        "--gameDir",
        os.path.join(workingDir, "game", "minecraft"),
        "--assetsDir",
        os.path.join(
            workingDir, "game", "{}_vanilla_install".format(version), "assets"
        ),
        "--assetIndex",
        installlaunchdata["assetindex"],
        "--uuid",
        uuid,
        "--accessToken",
        authtoken,
        "--userType",
        "mojang",  # Will change to be dynamic in the future
        "--versiontype",
        installlaunchdata["versiontype"],
    ]

    with open(os.path.join(workingDir, "data", "javapath.dat"), "rb") as javapathfile:
        javapath = os.path.join(*pickle.load(javapathfile))

    command = [javapath]

    command.extend(
        [
            "-XstartOnFirstThread",
            "-Xms409m",
            "-Xmx2048m",
            "-Duser.language=en",
            "-cp",
        ]
    )

    libpathlist = []

    for lib in installlaunchdata["libraries"]:
        libpathlist.append(
            os.path.join(
                workingDir,
                "game",
                "{}_vanilla_install".format(version),
                "libraries",
                lib,
            )
        )

    for l in [
        os.path.join(resourceDir, "static", "lwjgl", i)
        for i in os.listdir(os.path.join(resourceDir, "static", "lwjgl"))
        if i.endswith(".jar")
    ]:
        libpathlist.append(l)
    libpathlist.append(
        os.path.join(resourceDir, "static", "log4j", "log4j-api-2.16.0.jar")
    )
    libpathlist.append(
        os.path.join(resourceDir, "static", "log4j", "log4j-core-2.16.0.jar")
    )

    command.append(":".join(libpathlist))

    return command + launchinputlist


if __name__ == "__main__":
    launch(input("Version : "))
