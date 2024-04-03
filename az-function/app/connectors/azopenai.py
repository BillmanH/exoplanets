import requests
import yaml
import openai
import os

class OpenAiCon():
    def __init__(self):
        self.params = {"api_key":os.getenv('OPENAI_KEY','API_key_not_set'),
          "api_base":"https://exodestiny-ai.openai.azure.com/",
          "api_type":"azure",
          "api_version":"2024-02-15-preview"}

        self.openai = openai
        self.max_tokens = 1000
        self.openai.api_key = self.params['api_key']
        self.openai.api_base =  self.params['api_base']
        self.openai.api_type = self.params['api_type']
        self.openai.api_version = self.params['api_version']
        self.deployment_name = 'exodestiny'
        self.temperature = 0.7
        self.max_tokens = 256
        # self.top_p = 1
        self.frequency_penalty = 0
        self.presence_penalty = 0

    def request(self, prompt):
      self.response = self.openai.Completion.create(engine=self.deployment_name, 
                                    prompt=prompt, 
                                    temperature=self.temperature,
                                    max_tokens=self.max_tokens,
                                    frequency_penalty=self.frequency_penalty,
                                    presence_penalty=self.presence_penalty)

      textResponse = self.response.choices[0].text
      textResponse = textResponse.replace(". ",". \n")
      return textResponse
      
