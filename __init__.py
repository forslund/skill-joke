# Copyright 2017, Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pyjokes

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from random import choice


class JokingSkill(MycroftSkill):
    def __init__(self):
        super(JokingSkill, self).__init__(name="JokingSkill")

    def initialize(self):
        """Register Chuck Norris jokes if supported by language."""
        lang = self.lang[:2]
        if 'chuck' in pyjokes.all_jokes[lang]:
            intent = (IntentBuilder("ChuckJokeIntent").require("Joke")
                      .require("Chuck"))
            self.register_intent_handler(intent, self.handle_chuck_joke)

    def speak_joke(self, lang, category):
        """Speak a joke from the specified category."""
        self.speak(pyjokes.get_joke(language=lang, category=category))

    @intent_handler(IntentBuilder("JokingIntent").require("Joke"))
    def handle_general_joke(self, message):
        """Select a category at random and speak a joke from it."""
        lang = self.lang[:2]
        selected = choice(pyjokes.all_jokes[lang])
        self.speak_joke(lang, selected)

    # Will only be registered if language supports chuck norris jokes
    def handle_chuck_joke(self, message):
        self.speak_joke(self.lang[:-3], 'chuck')

    @intent_handler(IntentBuilder("NeutralJokeIntent").require("Joke")
                    .require("Neutral"))
    def handle_neutral_joke(self, message):
        self.speak_joke(self.lang[:-3], 'neutral')

    def stop(self):
        pass


def create_skill():
    return JokingSkill()
