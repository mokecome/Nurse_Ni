# -*- coding: utf-8 -*-
"""
Created on Tue May 28 15:52:33 2024

@author: User
"""

def get_one_json(uri, text, url):
    one_data_json = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": url,
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "2:2",
                    "gravity": "top"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": text,
                                    "size": "lg",
                                    "color": "#ffffff",
                                    "weight": "regular",  
                                    "wrap": True,
                                    "maxLines": 2 
                                }
                            ]
                        }
                    ],
                    "position": "absolute",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px",
                    "backgroundColor": "#03303AF2",
                    "paddingAll": "20px",
                    "paddingTop": "23px",
                }
            ],
            "paddingAll": "0px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "了解更多",
                        "uri": uri
                    },
                    "height": "sm"
                }
            ],
        "paddingAll": "5px"
      }
    }

    return one_data_json




def add_json(data):
    flex_message = {
        "type": "carousel",
        "contents": data
    }
    return flex_message


