import os
import requests
from slack_bolt import App
from yelpapi import YelpAPI

# initializes app with bot token and signing secret
app = App(token=os.environ.get('SLACK_BOT_TOKEN'),
          signing_secret=os.environ.get('SLACK_SIGNING_SECRET'))

# include open weather key
open_weather = os.environ.get('OPEN_WEATHER')

# include yelp key
yelp_key = os.environ.get('YELP')


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
def message_kayak(message, say):
    """ congratulate or commiserate re: kayaking"""
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
    """ send congratulations """
    ack()
    body = "kayaking congratulations"
    [say(item) for item in kayaking_list[::]]
    say("wow!!!!!!!!!!!!!")
    say("congratulations!")
    [say(item) for item in kayaking_list[::-1]]


@app.action("button_click_not_kayaking")
def action_button_click_not_kayaking(body, ack, say):
    """send commiseration"""
    ack()
    body = "kayaking commiseration"
    [say(item) for item in not_kayaking_list[::]]


@app.message("sausage")
@app.message("Sausage")
@app.message("SAUSAGE")
@app.message("hot dog")
@app.message("Hot dog")
@app.message("Hotdog")
@app.message("extra meat")
@app.message("Extra meat")
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
        [say(item * 2) for item in hotdog_list[::]]
        say(":hotdog_wave:" * 2)
        [say(item * 2) for item in hotdog_list[::-1]]
    except Exception as e:
        logger.error(f"Error doing double long: {e}")


@app.action("button_click_double_long")
def action_button_click_double_long(body, ack, say, logger):
    """send double long hot dog message"""
    ack()
    try:
        [say(item) for item in hotdog_list[::]]
        say(":hotdog_wave:")
        [say(item) for item in hotdog_list[::-1]]
        [say(item) for item in hotdog_list[1::]]
        say(":hotdog_wave:")
        [say(item) for item in hotdog_list[::-1]]
    except Exception as e:
        logger.error(f"Error doing double long: {e}")


@app.action("button_click_regular")
def action_button_click_regular(body, ack, say, logger):
    """send regular hot dog message"""
    ack()
    try:
        [say (item) for item in hotdog_list[::]]
        say(":hotdog_wave:")
        [say (item) for item in hotdog_list[::-1]]
    except Exception as e:
        logger.error(f"Error doing regular hot dog: {e}")


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
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Welcome to _Beautiful's Home_* :tada:"}},
            {"type": "divider"},
            {"type": "section", "text": {"type": "mrkdwn","text": f"Hi <@{event['user']}>! So far, Beautiful has functions defined for messages containing the words kayak and sausage, weather analysis, a hot dog locator, and emoji additions."}},
            {"type": "image", "image_url": "https://tenor.com/view/kermit-dancing-happy-smiling-gif-14490278", "alt_text": "kermit dancing"}
            ]
        })
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


# listens to incoming messages that contain "weather"
@app.message("weather?")
@app.message("Weather?")
def message_weather(message, say, client):
    """ find out where bianca is in order to call openweather api """
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
                    {"text": {"type": "plain_text", "text": "Rangeley"}, "value": "Rangeley"}],
                "action_id": "static_select-action_weather"}
            }]
        })
    

# use bianca's location provided by dropdown to prepare response, send
@app.action("static_select-action_weather")
def weather(ack, body, logger, say):
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


@app.message("meat")
def message_meat(message, client, event, logger, say):

    """find out where we're lookin to call the yelp api"""
    say({"blocks": [{
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Where are we seeking hot dogs?"},
            "accessory": {
                "type": "static_select",
                "placeholder": {"type": "plain_text", "text": "Hot dog location"},
                "options": [
                    {"text": {"type": "plain_text", "text": "Brooklyn"}, "value": "Brooklyn, NY"},
                    {"text": {"type": "plain_text", "text": "Hancock"}, "value": "Hancock, Mass"},
                    {"text": {"type": "plain_text", "text": "Hollis"}, "value": "Hollis, Maine"},
                    {"text": {"type": "plain_text", "text": "Rangeley"}, "value": "Rangeley, Maine"},
                    {"text": {"type": "plain_text", "text": "Seattle"}, "value": "Capitol Hill, Seattle"}],
                "action_id": "static_select-action_hot_dog"}
            }]
        })

# use location provided by dropdown to prepare response, send
@app.action("static_select-action_hot_dog")
def hot_dog(ack, body, logger, say):
    ack()
    try:
        # parse hideous response from dropdown
        location = body['actions'][0]['selected_option']['value']
    
        yelp_api = YelpAPI(yelp_key)
        search_results = yelp_api.search_query(term="hotdog",location=location)['businesses']
        
        say("Here are some hot dog retailers near your requested location:")
        for index, item in zip(range(8), search_results):
            say({"blocks": [{
                    "type": "section",
                    "text": {"type": "mrkdwn","text": f"{item['name']} has {item['rating']} stars!"},
                    "accessory": {
                        "type": "image",
                        "image_url": item['image_url'],
                        "alt_text": "yelp pic"}
                    }]})

    except Exception as e:
        logger.error(f"Error publishing hot dog data: {e}")


@app.event("emoji_changed") 
def message_emoji(message, client, event, logger):
    """posts to emoji_town whenever a new emoji is added"""

    # excludes changes and removals
    if event["subtype"] == "add":

        try:

            # get emoji list using auth
            response = requests.get('https://slack.com/api/emoji.list',
                headers={'Authorization': f'Bearer {os.environ.get("SLACK_BOT_TOKEN")}'})

            # save to list -- not very efficient -- todo only get most recently added to json
            emoji = [ name for name, url in response.json()['emoji'].items()]

            # post new emoji to emoji_town
            result = client.chat_postMessage(channel="C029T1LM06L", text=":" + emoji[-1] + ":")

        except Exception as e:
            logger.error(f"Error publishing new emoji: {e}")

# start app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))