import os
import requests
import time
from slack_bolt import App
from yelpapi import YelpAPI

########################################
import logging

logging.basicConfig(level=logging.DEBUG)
app = App()


# @app.command("/hello-bolt-python-heroku")
# def hello(body, ack):
#     user_id = body["user_id"]
#     ack(f"Hi <@{user_id}>!")


# initializes app with bot token and signing secret
# app = App(token=os.environ.get('SLACK_BOT_TOKEN'),
#           signing_secret=os.environ.get('SLACK_SIGNING_SECRET'))

# include open weather key
# open_weather = os.environ.get('OPEN_WEATHER')

# # include yelp key
# yelp_key = os.environ.get('YELP')

# # include purple air key
# purple_key = os.environ.get('PURPLE')


# save some text lists for later

kayaking_list = [
    ':kayaking:' * 6,
    ':kayak1:' * 5,
    ':canoe_guy:' * 4,
    ':kayak:' * 3,
    ':canoe_guy_1:' * 2,
    ':jacked:'
    ]

not_kayaking_list = [
    ":kermit_nail-biting:" * 4,
    "😲☹  Ｉ 𝔸𝕄 ⓢ𝕠𝓇𝓇𝓎  🐣🐤",
    ":kermit_confused:" * 4,
    "•♞🍟  𝓘 𝐚Ⓜ 𝓈𝓸𝓇𝔯Ƴ  👌💎",
    ":kermit_sweat:" * 4,
    ".•°¤*(¯`★´¯)*¤° 𝕀 α𝕞 ร𝓞Ř𝓻Ƴ °¤*(¯´★`¯)*¤°•.",
    ":sad_kermit:" * 4,
    "´¯`•» 𝐢 ά𝓜 sᵒ𝐫𝓡Ｙ «•´¯`•",
    ":kermit_disappointment:" * 4,
    "💜🐝  เ 卂ᵐ 𝐬𝔬ŘᖇＹ  💙♠",
    ":kermit_tunnel:" * 4
    ]

hotdog_list = [
    ":hotdog_pack:" * 6,
    ":hotdog_dance_1:" * 5,
    ":eat_hotdog:" * 4,
    ":hotdog_dance:" * 3,
    ":hotdog_platter:" * 2
    ]


# listens to incoming messages that contain "kayak"
@app.message("kayak")
@app.message("Kayak")
@app.message("KAYAK")
@app.message("canoe")
@app.message("Canoe")
@app.message("row")
@app.message("Row")
def message_kayak(message, say):
    """congratulate or commiserate re: kayaking"""
    say(
        blocks=[
            {"type": "section", "text": {"type": "mrkdwn", "text": f"<@{message['user']}>, are you going :kayaking:?"},
            "accessory": {"type": "button", "text": {"type": "plain_text", "text": ":sob_yes_nod: :sob_yes_nod:"},
            "action_id": "button_click_kayaking"}},

            {"type": "section", "text": {"type": "mrkdwn", "text": " "},
            "accessory": {"type": "button", "text": {"type": "plain_text", "text": ":cowboy_rock_back_and_forth::cowboy_rock_back_and_forth:"},
            "action_id": "button_click_not_kayaking"}}
        ],
        text=f"<@{message['user']}>, are you going :kayaking?"
        )


@app.action("button_click_kayaking")
def action_button_click_kayaking(body, ack, say):
    """send congratulations"""
    ack()
    body = "kayaking congratulations"
    [say(item) for item in kayaking_list[:]]
    say("wow!!!!!!!!!!!!!")
    say("congratulations!")
    [say(item) for item in kayaking_list[::-1]]


@app.action("button_click_not_kayaking")
def action_button_click_not_kayaking(body, ack, say):
    """send commiseration"""
    ack()
    body = "kayaking commiseration"
    [say(item) for item in not_kayaking_list[:]]


@app.message("sausage")
@app.message("Sausage")
@app.message("SAUSAGE")
@app.message("hot dog")
@app.message("Hot dog")
@app.message("Hotdog")
@app.message("extra meat")
@app.message("Extra meat")
@app.message("meat")
@app.message("Meat")
def message_hotdog(message, say):
    """find out what kind o' hot dog is desired"""
    say(
        blocks=[
            {"type": "section",
            "text": {"type": "mrkdwn", "text": f"<@{message['user']}>, how would you like that?"},
            "accessory": {"type": "button", "text": {"type": "plain_text", "text": "regular"}, "action_id": "button_click_regular"}},
            
            {"type": "section","text": {"type": "mrkdwn", "text": " "}, "accessory": {"type": "button",
            "text": {"type": "plain_text", "text": "double wide"},
            "action_id": "button_click_double_wide"}},
            
            {"type": "section", "text": {"type": "mrkdwn", "text": " "}, "accessory": {"type": "button",
            "text": {"type": "plain_text", "text": "double long"}, "action_id": "button_click_double_long"}}
        ],
        text=f"<@{message['user']}>, how would you like that?",
    )

@app.action("button_click_double_wide")
def action_button_click_double_wide(body, ack, say, logger):
    """send double wide hot dog message"""
    ack()
    try:
        [say(item * 2) for item in hotdog_list[:]]
        say(":hotdog_wave:" * 2)
        [say(item * 2) for item in hotdog_list[::-1]]
        david_wants_condiments(say, logger)
    except Exception as e:
        logger.error(f"Error doing double long: {e}")


@app.action("button_click_double_long")
def action_button_click_double_long(body, ack, say, logger):
    """send double long hot dog message"""
    ack()
    try:
        [say(item) for item in hotdog_list[:]]
        say(":hotdog_wave:")
        [say(item) for item in hotdog_list[::-1]]
        [say(item) for item in hotdog_list[1::]]
        say(":hotdog_wave:")
        [say(item) for item in hotdog_list[::-1]]
        david_wants_condiments(say, logger)
    except Exception as e:
        logger.error(f"Error doing double long: {e}")


@app.action("button_click_regular")
def action_button_click_regular(body, ack, say, logger):
    """send regular hot dog message"""
    ack()
    try:
        [say (item) for item in hotdog_list[:]]
        say(":hotdog_wave:")
        [say (item) for item in hotdog_list[::-1]]
        david_wants_condiments(say, logger)
    except Exception as e:
        logger.error(f"Error doing regular hot dog: {e}")


def david_wants_condiments(say, logger):
    """whatever david"""
    say(
        blocks=[
            {"type": "section",
            "text": {"type": "mrkdwn", "text": f"Do you want any condiments?"},
            "accessory": {"type": "button", "text": {"type": "plain_text", "text": ":onion_angel:" * 3}, "action_id": "button_click_david"}},
            
            {"type": "section","text": {"type": "mrkdwn", "text": " "}, "accessory": {"type": "button",
            "text": {"type": "plain_text", "text": ":tomato_smack:" * 3}, "action_id": "button_click_david"}},
            
            {"type": "section", "text": {"type": "mrkdwn", "text": " "}, "accessory": {"type": "button",
            "text": {"type": "plain_text", "text": ":swaddled_pickle_rocking:" * 3}, "action_id": "button_click_david"}},

            {"type": "section","text": {"type": "mrkdwn", "text": " "}, "accessory": {"type": "button",
            "text": {"type": "plain_text", "text": ":weary_hotdog_mustard:" * 3}, "action_id": "button_click_david"}},

            {"type": "section","text": {"type": "mrkdwn", "text": " "}, "accessory": {"type": "button",
            "text": {"type": "plain_text", "text": "no thank you, this isn't real"}, "action_id": "button_click_not_david"}}
        ],
        text=f"Do you want any condiments?",
    )


@app.action("button_click_david")
def action_button_click_david(body, ack, say, logger):
    """scold david"""
    ack()
    try:
        say("_MAYBE_ you should go eat a _LOBSTER ROLL_ while you _LIVE_ in _MAINE_")
    except Exception as e:
        logger.error(f"Error scolding David: {e}")


@app.action("button_click_not_david")
def action_button_click_david(body, ack, say, logger):
    """wave to non-david user"""
    ack()
    try:
        say(":hotdog_wave:")
    except Exception as e:
        logger.error(f"Error waving to not David: {e}")


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    """create home tab"""
    try:
        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
        # the user that opened your app's app home
        user_id=event["user"],
        # the view object that appears in the app home
        view={
        "type": "home",
        "callback_id": "home_view",
        # body of the view
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Welcome to _Beautiful_'s Home* :flushed_pants: :horse_cargo_shorts: :virus_yellow:"}},
            {"type": "divider"},
            {"type": "section", "text": {"type": "mrkdwn","text": f"Hi <@{event['user']}>!"}},
            {"type": "section", "text": {"type": "mrkdwn","text": ":yelp_logo_small: To *search Yelp*, type `please yelp [your search term] in [your search location]`. The first eight results will be displayed."}},
            {"type": "section", "text": {"type": "mrkdwn","text": ":alien_bong: To get the current *air quality*, type `aqi`."}},
            {"type": "section", "text": {"type": "mrkdwn","text": ":sunglasses_spin: To determine whether the *weather* is currently warmer for Hannah or Bianca, type `weather`."}},
            {"type": "section", "text": {"type": "mrkdwn","text": ":honk_nod: To see *emoji* as they are added in real time, please visit #emoji_town."}},
            {"type": "section", "text": {"type": "mrkdwn","text": ":jacked: To experience other Easter eggs, just mention `kayaking` or `hot dogs`."}},
            {"type": "image", "image_url": "https://tenor.com/view/kermit-dancing-happy-smiling-gif-14490278", "alt_text": "kermit dancing"},
            {"type": "section", "text": {"type": "mrkdwn","text": f"_All emoji here are borrowed -- many from Diana :admire:_"}}
            ]
        })
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.message("weather")
@app.message("Weather")
def message_weather(message, say, client):
    """find out where bianca is in order to call openweather api"""
    say({"blocks": [{
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Where _is_ Bianca?"},
            "accessory": {
                "type": "static_select",
                "placeholder": {"type": "plain_text", "text": "Bianca's location"},
                "options": [
                    {"text": {"type": "plain_text", "text": "Brooklyn"}, "value": "Brooklyn"},
                    {"text": {"type": "plain_text", "text": "Hancock"}, "value": "Hancock"},
                    {"text": {"type": "plain_text", "text": "Hollis"}, "value": "Hollis"},
                    {"text": {"type": "plain_text", "text": "Rangeley"}, "value": "Rangeley"},
                    {"text": {"type": "plain_text", "text": "Stratton"}, "value": "Stratton"}],
                "action_id": "static_select-action_weather"}
            }]
        })
    

@app.action("static_select-action_weather")
def weather(ack, body, logger, say):
    """use bianca's location provided by dropdown to prepare response, send"""
    ack()
    try:
        # parse hideous response from dropdown
        bianca_location = body['actions'][0]['selected_option']['value']

        # hannah weather
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q=Seattle&appid={open_weather}&units=imperial")
        seattle_weather = response.json()['weather'][0]['description']
        seattle_temperature = str(response.json()['main']['feels_like'])
        say(f"Hannah is probably in Seattle, where the weather is '{seattle_weather}' and it feels like about {seattle_temperature}° fahrenheit.")
        
        # bianca weather
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={bianca_location}&appid={open_weather}&units=imperial")
        bianca_weather = response.json()['weather'][0]['description']
        bianca_temperature = str(response.json()['main']['feels_like'])
        say(f"In {bianca_location}, the weather is '{bianca_weather}' and it feels like about {bianca_temperature}° fahrenheit.")

        # who's hotter?
        if seattle_temperature > bianca_temperature:
            say("Today, Hannah's hotter.")
        elif bianca_temperature > seattle_temperature:
            say("Today, Bianca's hotter.")
        else:
            say("Today, the ladies in the chat are equally sweaty.")
        say(":quite_sweaty::blob_sweat_bongo::mnm_sweat::flushed_sweat::sweating::blob_sweat_relief::blob_hypersweat:")

    except Exception as e:
            logger.error(f"Error providing weather report: {e}")


@app.message("aqi")
@app.message("Aqi")
@app.message("AQI")
@app.message("air quality")
@app.message("Air quality")
@app.message("PM")
def air_quality(message, client, event, logger, say):
    """query purpleair api for air quality data"""

    # default sensor
    sensor = "94279"

    try:
        # check whether user has provided a different sensor
        user_message = message['text'].lower()
        if "sensor" in user_message:
            message_list = user_message.split()
            location_of_word_sensor = message_list.index("sensor")
            sensor = message_list[location_of_word_sensor + 1]
        
        # query purple air
        response = requests.get(f"https://api.purpleair.com/v1/sensors/{sensor}",
            headers={"X-API-Key": purple_key})
        
        # save PM2.5 & sensor name for use in response
        pm_2_point_5 =response.json()['sensor']['stats']['pm2.5']
        sensor_name =response.json()['sensor']['name']


        # determine how their air quality measures up
        if pm_2_point_5 <= 12:
            end = f"*good* (less than 12)"
        elif pm_2_point_5 > 12 and pm_2_point_5 <= 35.5:
            end = "*moderate* (between 12 and 35.5)"
        elif pm_2_point_5 > 35.5 and pm_2_point_5 <= 55.5:
            end = "*unhealthy for sensitive groups* (between 35.5 and 55.5)"
        elif pm_2_point_5 > 55.5 and pm_2_point_5 <= 150.5:
            end = "*unhealthy* (between 55.5 and 150.5)"
        elif pm_2_point_5 > 150.5 and pm_2_point_5 <= 250.5:
            end = "*very unhealthy* (between 150.5 and 250.5)"
        elif pm_2_point_5 > 250.5 and pm_2_point_5 <= 500.5:
            end = "*hazardous* (between 250.5 and 500.5)"
        else:
            end = "*outside of the range of this program RIP*"

        # inform user
        say(f"PM2.5 at *{sensor_name}* is currently *{pm_2_point_5}*, which is {end}")

        # user education re: how to get data for another sensor
        say("_if this isn't an appropriate sensor, trying saying 'aqi sensor YourSensorID'_")
        say("_to find a sensor ID, visit purpleair.com/map, click on a dot, and view the number after 'select=' in the url_")
        
    except Exception as e:
            logger.error(f"Error providing AQI report: {e}")


@app.message("monitor air")
def air_quality_background(message, client, event, logger, prev_classification = "", count = 0):
    """query purpleair api for air quality data"""

    print("aqi being checked in background")

    if count == 0:
        prev_classification = "good"
        count = 1

    # default sensor
    sensor = "94279"

    try:
        # query purple air
        response = requests.get(f"https://api.purpleair.com/v1/sensors/{sensor}",
            headers={"X-API-Key": purple_key})
        
        # save PM2.5 & sensor name for use in response
        pm_2_point_5 =response.json()['sensor']['stats']['pm2.5']
        sensor_name =response.json()['sensor']['name']


        # determine how their air quality measures up
        if pm_2_point_5 <= 12:
            classification = "good"
        elif pm_2_point_5 > 12 and pm_2_point_5 <= 35.5:
            classification = "moderate"
        elif pm_2_point_5 > 35.5 and pm_2_point_5 <= 55.5:
            end = "unhealthy for sensitive groups"
        elif pm_2_point_5 > 55.5 and pm_2_point_5 <= 150.5:
            classification = "unhealthy"
        elif pm_2_point_5 > 150.5 and pm_2_point_5 <= 250.5:
            classification = "very unhealthy"
        elif pm_2_point_5 > 250.5 and pm_2_point_5 <= 500.5:
            classification = "hazardous"
        else:
            classification = "outside of the range of this program, RIP"

        print(classification)

        if prev_classification != classification:
            # tell me if the range changed

            # find an appropriate emoji
            if prev_classification == "good":
                emoji = ":blob_broken:"
            elif prev_classification == "moderate" and classification != "good":
                emoji = ":blob_broken:"
            elif prev_classification == "unhealthy for sensitive groups" and classification != "moderate":
                emoji = ":blob_broken:"
            elif prev_classification == "unhealthy" and classification != "unhealthy for sensitive groups":
                emoji = ":blob_broken:"
            elif prev_classification == "very unhealthy" and classification != "unhealthy":
                emoji = ":blob_broken:"
            elif prev_classification == "hazardous" and classification != "very unhealthy":
                emoji = ":blob_broken:"
            else:
                emoji = ":applause:"

            result = client.chat_postMessage(channel="C02BNH8KV1D", text=f"{emoji} <@U02FMJW3R>, air quality at *{sensor_name}* has changed to *{classification}* (PM2.5 is {pm_2_point_5})")

        # check every 15 min
        time.sleep(900)
        air_quality_background(client, event, logger, classification, count)
        
    except Exception as e:
            logger.error(f"Error providing AQI report: {e}")


@app.message("please yelp")
@app.message("Please yelp")
@app.message("Please Yelp")
@app.message("PLEASE YELP")
def message_yelp(message, client, event, logger, say):
    """send user's search query to yelp api, return results"""

    user_input = message['blocks'][0]['elements'][0]['elements'][0]['text'].split()

    try:
        # parse user input
        location_of_word_yelp = user_input.index("yelp")
        location_of_word_in = user_input.index("in")

        # search location should be anything that happens after the word in
        location = ' '.join(user_input[location_of_word_in + 1:])

        # search term should be whatever happened before "in Location", starting after "please yelp" -- made back into a sentence
        term = ' '.join(user_input[location_of_word_yelp + 1 : location_of_word_in])

        # call api
        yelp_api = YelpAPI(yelp_key)
        search_results = yelp_api.search_query(term=term,location=location)['businesses']
        
        # return results
        text = f"Here are some {term} businesses near {location}:"
        say(text)

        # limit to first 8 results
        for index, item in zip(range(8), search_results):

            text = {"blocks": [{
                    "type": "section",
                    "text": {"type": "mrkdwn","text": f"<{item['url']}|{item['name']}> has {item['rating']} stars!"},
                    }]}
            say(text)

            # give it a second to load the image
            time.sleep(2)

    except Exception as e:
        logger.error(f"Error publishing yelp data: {e}")
        say(f"Error publishing yelp data: {e}")


@app.event("emoji_changed") 
def message_emoji(message, client, event, logger, say):
    """post to emoji_town whenever a new emoji is added"""

    # excludes changes and removals
    if event["subtype"] == "add":

        try:

            # get emoji list using auth
            response = requests.get('https://slack.com/api/emoji.list',
                headers={'Authorization': f'Bearer {os.environ.get("SLACK_BOT_TOKEN")}'})

            # save to list -- not very efficient -- todo only get most recently added to json
            emoji = [name for name, url in response.json()['emoji'].items()]

            # post new emoji to emoji_town
            result = client.chat_postMessage(channel="C029T1LM06L", text=":" + emoji[-1] + ":")

        except Exception as e:
            logger.error(f"Error publishing new emoji: {e}")


# @app.message("where")
# def location_message(message, client, event, logger, say):
#     """print message details to terminal"""
#     print(message)




# from flask import Flask, request
# from slack_bolt.adapter.flask import SlackRequestHandler

# flask_app = Flask(__name__)
# handler = SlackRequestHandler(app)


# @flask_app.route("/slack/events", methods=["POST"])
# def slack_events():
#     return handler.handle(request)


# start app
# if __name__ == "__main__":
#     app.start(port=int(os.environ.get("PORT", 3000)))
