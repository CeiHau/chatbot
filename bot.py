from transformers import BertForQuestionAnswering
model = BertForQuestionAnswering.from_pretrained('resource/', local_files_only = True)

from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained('resource/', local_files_only = True)

import torch
class Bot:
    def __init__(self, context):
        self.context = context
    def ask(self, question):

        # Tokenize
        indexedTokens = tokenizer.encode(question, self.context)
        tokensTensor = torch.tensor([indexedTokens])

        # Search the index of '[SEP]' token
        sepIndex = indexedTokens.index(tokenizer.sep_token_id)
        segmentsIds = [0] * (sepIndex + 1) + [1] * (len(indexedTokens) - (sepIndex + 1))
        segmentsTensors = torch.tensor([segmentsIds])

        # Predict the start and end positions logits
        outputs = model(tokensTensor, token_type_ids=segmentsTensors, return_dict=True)

        # Get the index of start and end logits
        startIndex = torch.argmax(outputs.start_logits)
        endIndex = torch.argmax(outputs.end_logits)

        tokens = tokenizer.convert_ids_to_tokens(indexedTokens)
        answer = ""
        for i in range(startIndex, endIndex + 1):
            if tokens[i][0:2] == '##':
                answer += tokens[i][2:]
            else:
                answer += " " + tokens[i]
        return answer

    def changeContext(self, newContext):
        self.context = newContext



# q11 = "who is kanye's wife?"
# q12 = "what albums does kanye have"
# a1 = "Kanye West initially made his mark on the music industry as a producer for leading artists. He showcased his own abilities as a rapper with his 2004 debut, College Dropout, and cemented his place atop the hip hop world via such chart-topping albums as Late Registration (2005), My Beautiful Dark Twisted Fantasy (2010), Yeezus (2013) and Ye (2018). The winner of nearly two dozen Grammy Awards, West is also known for his awards-show theatrics, forays into fashion and marriage to Kim Kardashian."
#
#
# bot = Bot(a1)
# print(bot.ask(q11))
# print(bot.ask( q12))