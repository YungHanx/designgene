from DAO import DAO
from MappingData import QUESTION_MAP
from ConversationService import ConversationService
from RecommendationServiceReply import RecommendationServiceReply
import uuid

class RecommendationServiceBot:
    def __init__(self, user_id, message):
        self._DAO = DAO()
        self.LUIS = ConversationService()
        self.BOT = RecommendationServiceReply()
        self.USER_ID = user_id
        self.MESSAGE = message
        is_new = self._DAO.getUser(user_id)
        if not is_new:
            user_first_data = {
                "user_id": user_id,
                "mission_number": 0,
                "mission_status": "start",
                "mission_tags": [],####################
                "status": "pending",
                "tags": []
            }
            self.USER_DATA = user_first_data
        else:
            self.USER_DATA = is_new
        #print(self.USER_DATA)
        self.LUIS.getConversationResponse(message)
        #print(self.USER_DATA)沒意義
        self.TOP_INTENT = self.LUIS.getTopIntent()
        #print(self.USER_DATA)沒意義
        self.ENTITIES = self.LUIS.getEntities()
        #print(self.USER_DATA)還是有保留misstion_tag
        mission_tags = self.USER_DATA["mission_tags"] + self.LUIS.ENTITIES
        #print(self.USER_DATA)還是有保留misstion_tag
        self.USER_DATA["mission_tags"] = list(set(mission_tags))
        #print(self.USER_DATA)還是有保留misstion_tag
        self.USER_DATA["tags"] = self.LUIS.genNewTag(self.USER_DATA["tags"], self.ENTITIES)
        #print(self.USER_DATA)還是有保留misstion_tag
        self._DAO.setUser(user_id, self.USER_DATA)
     # handler
    def handlePendingStatus(self):
        self._DAO.setUser(self.USER_ID, {
            "mission_status": "Pending"
        })
    def handleNextMission(self):
        self._DAO.setUser(self.USER_ID, {
            "mission_number": self.USER_DATA["mission_number"] + 1
        })
    def handleMissionComplete(self):
        self._DAO.setUser(self.USER_ID, {
            "mission_number": None,
            "Status": "Complete",
            "mission_status": "Complete"
        })
    #執行任務的順序確認資訊完成度才可以跳下一個
    def getReply(self):
        mission_number = self.USER_DATA["mission_number"]
        if mission_number == 0:
            return self.getBrandNameFlow()
        elif mission_number == 1:
            return self.getApplication()
        elif mission_number == 2:
            return self.getColor()
        elif mission_number == 3:
            return self.getMetaphor()
        elif mission_number == 4:
            return self.getDeadline()
        elif mission_number == 5:
            return self.getDesignTone()
        else:
            return None
    def checkGoal(self, goal):
        goal_copy = goal.copy()
        for _g in goal:
            if _g in self.USER_DATA["mission_tags"]:
                goal_copy.remove(_g)
        if len(goal_copy) == 0:
            return "IS_COMPLETE"
        else:
            text = self.BOT.askInformation(goal_copy)
            return text

    def getBrandNameFlow(self):
        GOAL = ["Brand_Name", "Brand_Product", "Brand_Goal", "Brand_Industry"]
        check_result = self.checkGoal(GOAL)
        if self.USER_DATA["mission_status"] == "start":
            self.handlePendingStatus()
            return self.BOT.genReply(QUESTION_MAP[1]['question'], self.USER_DATA)
        elif check_result != "IS_COMPLETE":
            return self.BOT.genReply(check_result, self.USER_DATA)
        else:
            self.handleNextMission()#跳到下題的關鍵
            return self.BOT.genReply(QUESTION_MAP[2]['question'], self.USER_DATA)
    def getApplication(self):
        GOAL = ["Application"]
        check_result = self.checkGoal(GOAL)
        if check_result != "IS_COMPLETE":
            return self.BOT.genReply(check_result, self.USER_DATA)
        else:
            self.handleNextMission()
            return self.BOT.genReply(QUESTION_MAP[3]['question'], self.USER_DATA)
    def getColor(self):
        GOAL = ["Main_Color"]
        check_result = self.checkGoal(GOAL)
        if check_result != "IS_COMPLETE":
            return self.BOT.genReply(check_result, self.USER_DATA)
        else:
            self.handleNextMission()
            return self.BOT.genReply(QUESTION_MAP[4]['question'], self.USER_DATA)
    def getMetaphor(self):
        GOAL = ["Metaphor"]
        check_result = self.checkGoal(GOAL)
        if check_result != "IS_COMPLETE":
            return self.BOT.genReply(check_result, self.USER_DATA)
        else:
            self.handleNextMission()
            return self.BOT.genReply(QUESTION_MAP[5]['question'], self.USER_DATA)
    def getDeadline(self):
        GOAL = ["Deadline_Date"]
        check_result = self.checkGoal(GOAL)
        if check_result != "IS_COMPLETE":
            return self.BOT.genReply(check_result, self.USER_DATA)
        else:
            self.handleNextMission()
            return self.BOT.genReply(QUESTION_MAP[6]['question'], self.USER_DATA)
    def getDesignTone(self):
        GOAL = ["Design_Style"]
        check_result = self.checkGoal(GOAL)
        if check_result != "IS_COMPLETE":
            return self.BOT.genReply(check_result, self.USER_DATA)
        else:
            self.handleMissionComplete()
            return self.BOT.genReply("Finish", self.USER_DATA)
        
    
print('')


