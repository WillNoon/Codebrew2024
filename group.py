import coreFunctions


class Group:            
    def __init__(self):
        self.id = coreFunctions.generateId()
        self.tags = {"computing","debating"}
        self.members = {"123456","223456","333456","444456"}
        self.max = 6
        self.desc = "this is a test club it is a club for computing and debating it is a club"

