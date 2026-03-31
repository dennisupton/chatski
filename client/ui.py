import config

#┌ ┐ └ ┘ ─ │ ├ ┤ ┬ ┴ ┼ ╭ ╮ ╯ ╰

def printUI(img, users):
    print(addBorder(img))
    print(config.username)
    print()
    if len(users)>0:
        for address,user in net.users.items():
            print(addBorder(user["frame"]))
            print()
    print("Press q to quit")

def addBorder(img):
    img = img.split("\n")
    res = []
    res.append("╭"+"─"*len(img[0])+"╮")
    for i in img:
        res.append("│"+i+"│")
    res.append("╰"+"─"*len(img[0])+"╯")
    res = "\n".join(res)
    return res