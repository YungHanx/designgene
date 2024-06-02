
class RecommendationServiceReply:
    def __init__(self):
        pass
    def genReply(self, message, user_data):
        STATUS = user_data["status"]
        if message == "Finish":
            STATUS = "Complete"
        return {
            "user_id": user_data["user_id"],
            "question": message,
            "status": STATUS,
            "tags": user_data["tags"],
        }
    def askInformation(self, goal_list):
        message = ""
        if len(goal_list) == 1:
            message += "Thanks! Can you tell me more about your " + goal_list[0].replace("_", " ") + "?"
        else:
            message += "Thanks! Can you tell me more about your "
            for i, goal in enumerate(goal_list):
                text = goal.replace("_", " ")
                if i == len(goal_list) - 1:
                    message += "and " + text + "?"
                else:
                    if (len(goal_list) == 2):
                        message += text + " "
                    else:
                        message += text + ", "
        return message