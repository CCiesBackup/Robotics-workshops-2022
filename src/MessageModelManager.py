class OutgoingMessages:
    def ready(self):
        message = {
            "from": "client",
            "type": "ready"
                                }
        return message

    def test_planet(self, test_planet_name):
        message = {
                    "from": "client",
                    "type": "testPlanet",
                    "payload": {
                        "planetName": f"{test_planet_name}"
                                }
                                            }
        return message

    def path_msg(self, startX, startY, startD, endX, endY, endD, path_status):
        message = {
                    "from": "client",
                    "type": "path",
                    "payload": {
                                "startX": f"{startX}",
                                "startY": f"{startY}",
                                "startDirection": f"{startD}",
                                "endX": f"{endX}",
                                "endY": f"{endY}",
                                "endDirection": f"{endD}",
                                #free | blocked
                                "pathStatus": f"{path_status}"
                    }
                     }
        return message

    def path_select(self, startX, startY, startD):
        message = {
                    "from": "client",
                    "type": "pathSelect",
                      "payload": {
                        "startX": f"{startX}",
                        "startY": f"{startY}",
                        "startDirection": f"{startD}"
                      }
                            }
        return message

    def target_reached(self, text):
         message ={
            "from": "client",
            "type": "targetReached",
            "payload": {
                "message": f"{text}"
            }
        }
         return message

    def exploration_completed(self, text):
        message = {
            "from": "client",
            "type": "explorationCompleted",
            "payload": {
                "message": f"{text}"
            }
        }
        return message

#Seen above all as a reference
class IncomingMessages:

    test_planet_receive ={
                          "from": "debug",
                          "type": "notice",
                          "payload": {
                            "message": "active planet: <PLANET_NAME>"
                          }
                        }

    ready_receive = {
                      "from": "server",
                      "type": "planet",
                      "payload": {
                        "planetName": "<PLANET_NAME>",
                        "startX": "<X>",
                        "startY": "<Y>",
                        "startOrientation": "<O>"
                      }
                    }
    #Korrektur + weight
    path_receive = {
          "from": "server",
          "type": "path",
          "payload": {
            "startX": "<Xs>",
            "startY": "<Ys>",
            "startDirection": "<Ds>",
            "endX": "<Xc>",
            "endY": "<Yc>",
            "endDirection": "<Dc>",
            "pathStatus": "free|blocked",
            "pathWeight": "<weight>"
          }
        }
    #Course confirmation or amendment
    path_select_receive = {
                          "from": "server",
                          "type": "pathSelect",
                          "payload": {
                            "startDirection": "<Dc>"
                          }
                        }


    path_unveiled = {
        "from": "server",
        "type": "pathUnveiled",
        "payload": {
            "startX": "< Xs >",
            "startY": "< Ys >",
            "startDirection": "< Ds >",
            "endX": "< Xe >",
            "endY": " < Ye >",
            "endDirection": "< De >",
            "pathStatus": "free|blocked",
            "pathWeight": "< weight >"
        }
    }

    target = {
              "from": "server",
              "type": "target",
              "payload": {
                "targetX": "<Xt>",
                "targetY": "<Yt>"
              }
            }

    completed = {
                "from": "server",
                "type": "done",
                "payload": {
                    "message": "<TEXT>"
                }
            }



