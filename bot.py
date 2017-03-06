from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

from strings import *
from initialize import initialize, keyboard_generate
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GET_NAME, GET_AGE, GET_LOCATION, GET_GENDER, GET_MAJOR, GET_LIS, \
GET_FAV, GET_FIELD, GET_UNI, GET_YEARS, GET_CREDS = range(11)

post = initialize()
keys = list(post.keys())

gender_keyboard = [['مذکر', 'مونث']]
gender_markup = ReplyKeyboardMarkup(gender_keyboard, one_time_keyboard=True)

major_keyboard = keyboard_generate(keys, 10)
major_markup = ReplyKeyboardMarkup(major_keyboard, one_time_keyboard=True)

lis_keyboard = [['دیپلم', 'فوق دیپلم'],
                ['لیسانس', 'فوق لیسانس'],
                ['دکتری', 'سایر']]
lis_markup = ReplyKeyboardMarkup(lis_keyboard, one_time_keyboard=True)

pass_keyboard = [['مایل نیستم']]
pass_markup = ReplyKeyboardMarkup(pass_keyboard, one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('%s - %s' % (key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):
    update.message.reply_text(startS)

    return GET_NAME


def get_name(bot, update, user_data):
    text = update.message.text
    user_data['name'] = text
    update.message.reply_text('خوش اومدین %s' % text)
    update.message.reply_text(getAgeS, reply_markup=pass_markup)

    return GET_AGE


def get_age(bot, update, user_data):
    text = update.message.text
    user_data['age'] = text
    update.message.reply_text(getLocationS)

    return GET_LOCATION


def no_age(bot, update, user_data):
    update.message.reply_text(getLocationS)

    return GET_LOCATION


def get_location(bot, update, user_data):
    text = update.message.text
    user_data['location'] = text
    update.message.reply_text(getGenderS, reply_markup=gender_markup)

    return GET_GENDER


def get_gender(bot, update, user_data):
    text = update.message.text
    user_data['gender'] = text
    update.message.reply_text(getMajorS, reply_markup=major_markup)

    return GET_MAJOR


def pass_major(bot, update, user_data):
    update.message.reply_text('گزینه خود را وارد کنید')
    return GET_MAJOR


def get_major(bot, update, user_data):
    text = update.message.text
    user_data['major'] = text
    update.message.reply_text(getLisS, reply_markup=lis_markup)

    return GET_LIS


def pass_lis(bot, update, user_data):
    update.message.reply_text('گزینه خود را وارد کنید')
    return GET_LIS


def get_lis(bot, update, user_data):
    text = update.message.text
    user_data['lis'] = text
    favs = post[user_data['major']]
    fav_keyboard = keyboard_generate(favs, int(len(favs) / 2))
    fav_keyboard.append(['سایر'])
    fav_markup = ReplyKeyboardMarkup(fav_keyboard, one_time_keyboard=True)
    update.message.reply_text(getFavS, reply_markup=fav_markup)

    return GET_FAV


def pass_fav(bot, update, user_data):
    update.message.reply_text('گزینه خود را وارد کنید')
    return GET_FAV


def get_fav(bot, update, user_data):
    text = update.message.text
    user_data['fav'] = text
    fields = post[user_data['major']]
    field_keyboard = keyboard_generate(fields, int(len(fields) / 2))
    field_keyboard.append(['سایر'])
    field_markup = ReplyKeyboardMarkup(field_keyboard, one_time_keyboard=True)

    update.message.reply_text(getFieldS, reply_markup=field_markup)

    return GET_FIELD


def pass_field(bot, update, user_data):
    update.message.reply_text('گزینه خود را وارد کنید')
    return GET_FIELD


def get_field(bot, update, user_data):
    text = update.message.text
    user_data['field'] = text
    update.message.reply_text(getUniS)

    return GET_UNI


def get_uni(bot, update, user_data):
    text = update.message.text
    user_data['uni'] = text
    update.message.reply_text(getYearsS, reply_markup=pass_markup)

    return GET_YEARS


def no_years(bot, update, user_data):
    update.message.reply_text(getCredsS)

    return GET_CREDS


def get_years(bot, update, user_data):
    text = update.message.text
    user_data['years'] = text
    update.message.reply_text(getCredsS)

    return GET_CREDS


def get_creds(bot, update, user_data):
    text = update.message.text
    user_data['creds'] = text
    update.message.reply_text(finishS)

    update.message.reply_text("این اطلاعات را در اختیار ما قرار دادید"
                              "%s"
                              "ممنون از توجهتان" % facts_to_str(user_data))

    user_data.clear()

    return ConversationHandler.END


def done(bot, update, user_data):
    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            GET_NAME: [MessageHandler(Filters.text,
                                      get_name,
                                      pass_user_data=True)
                       ],

            GET_AGE: [RegexHandler('^مایل نیستم$',
                                   no_age,
                                   pass_user_data=True),
                      MessageHandler(Filters.text,
                                     get_age,
                                     pass_user_data=True),
                      ],

            GET_LOCATION: [MessageHandler(Filters.text,
                                          get_location,
                                          pass_user_data=True),
                           ],
            GET_GENDER: [MessageHandler(Filters.text,
                                        get_gender,
                                        pass_user_data=True),
                         ],
            GET_MAJOR: [MessageHandler(Filters.text,
                                       get_major,
                                       pass_user_data=True),
                        ],
            GET_LIS: [RegexHandler('^سایر$',
                                   pass_lis,
                                   pass_user_data=True),
                      MessageHandler(Filters.text,
                                     get_lis,
                                     pass_user_data=True),
                      ],
            GET_FAV: [RegexHandler('^سایر$',
                                   pass_fav,
                                   pass_user_data=True),
                      MessageHandler(Filters.text,
                                     get_fav,
                                     pass_user_data=True),
                      ],
            GET_FIELD: [RegexHandler('^سایر$',
                                     pass_field,
                                     pass_user_data=True),
                        MessageHandler(Filters.text,
                                       get_field,
                                       pass_user_data=True),
                        ],
            GET_UNI: [MessageHandler(Filters.text,
                                     get_uni,
                                     pass_user_data=True),
                      ],
            GET_YEARS: [RegexHandler('^مایل نیستم$',
                                     no_years,
                                     pass_user_data=True),
                        MessageHandler(Filters.text,
                                       get_years,
                                       pass_user_data=True),
                        ],
            GET_CREDS: [MessageHandler(Filters.text,
                                       get_creds,
                                       pass_user_data=True),
                        ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
