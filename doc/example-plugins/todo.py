outputs = []
crontabs = []

tasks = {}

def process_message(data):
    global tasks
    channel = data["channel"]
    text = data["text"]
    #only accept tasks on DM channels
    if channel.startswith("D") or channel.startswith("C"):
        if channel not in tasks.keys():
            tasks[channel] = []
        #do command stuff
        if text.startswith("todo"):
            tasks[channel].append(text[5:])
            outputs.append([channel, "added"])
        if text == "tasks":
            output = ""
            counter = 1
            for task in tasks[channel]:
                output += "%i) %s\n" % (counter, task)
                counter += 1
            outputs.append([channel, output])
        if text == "fin":
            tasks[channel] = []
        if text.startswith("done"):
            num = int(text.split()[1]) - 1
            tasks[channel].pop(num)
        if text == "show":
            print tasks