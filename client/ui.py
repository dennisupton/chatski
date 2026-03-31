import config
import image
#┌ ┐ └ ┘ ─ │ ├ ┤ ┬ ┴ ┼ ╭ ╮ ╯ ╰

showHelp = False

def printUI(img, users):
    print(addBorder(img))
    print(config.username)
    print()
    if len(users)>0:
        for address,user in net.users.items():
            print(addBorder(user["frame"]))
            print()
    if showHelp:
        print(" - Press q to quit")
        print(" - Press d to toggle dynamic shading"+toOnOff(image.dynamicShading))
        print(" - Press c to redo config")
    print("Press h to show help menu")

def addBorder(img):
    img = img.split("\n")
    res = []
    res.append("╭"+"─"*len(img[0])+"╮")
    for i in img:
        res.append("│"+i+"│")
    res.append("╰"+"─"*len(img[0])+"╯")
    res = "\n".join(res)
    return res


def toOnOff(condition):
    if condition:
        return "(On)"
    return "(Off)"