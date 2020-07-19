#!/usr/bin/env python3

from aws_cdk import core

from automatic_translation_diary.automatic_translation_diary_stack import AutomaticTranslationDiaryStack


app = core.App()
AutomaticTranslationDiaryStack(app, "automatic-translation-diary")

app.synth()
