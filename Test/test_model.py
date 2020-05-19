import torch,nltk
nn=torch.nn
optim=torch.optim
F=nn.functional
#use fot changing inputs to the trained vectors
sent_data=[]
label_data=[]
# word list creation
with open(r'data\sents.txt') as f:
    for sentence in f.read().splitlines():
        sent_data.append(sentence.split())

# sent_data=sent_data.split()
word_list=[]
[[word_list.append(words) for words in i] for i in sent_data]
words=list(set(word_list))
words.sort()
#labels list creation
with open("data\labels.txt") as f:
    for label  in  f.read().splitlines():
        label_data.append(label.split())


label_list=[]
[[label_list.append(words) for words in i] for i in label_data]
labels=list(set(label_list))
labels.sort()

# Declaring dict for vocab and tags
tag={}
vocab={}
indx2word={}
indx2tag={}

for i, word in enumerate(words):
    vocab[word] = i
    indx2word[i]=word
for i, tags in enumerate(labels):
    tag[tags] = i
    indx2tag[i]=tags

vocab['PAD']=len(vocab.keys())
tag['PAD']=len(tag.keys())
indx2word[len(indx2word.keys())]='PAD'
indx2tag[len(indx2tag.keys())]='PAD'




class LSTMTagger(nn.Module):

    def __init__(self, embedding_dim, hidden_dim, vocab_size, tagset_size):
        super(LSTMTagger, self).__init__()
        self.hidden_dim = hidden_dim

        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)

        # The LSTM takes word embeddings as inputs, and outputs hidden states
        # with dimensionality hidden_dim.
        self.lstm = nn.LSTM(embedding_dim, hidden_dim)

        # The linear layer that maps from hidden state space to tag space
        self.hidden2tag = nn.Linear(hidden_dim, tagset_size)

    def forward(self, sentence):
        embeds = self.word_embeddings(sentence)
        lstm_out, _ = self.lstm(embeds.view(len(sentence), 1, -1))
        tag_space = self.hidden2tag(lstm_out.view(len(sentence), -1))
        tag_scores = F.log_softmax(tag_space, dim=1)
        return tag_scores

EMBEDDING_DIM = 64
HIDDEN_DIM = 64
# model = LSTMTagger(EMBEDDING_DIM, HIDDEN_DIM, len(vocab.keys()), len(tag.keys()))
# loss_function = nn.NLLLoss()
# optimizer = optim.SGD(model.parameters(), lr=0.1)

# Model Loading
model=LSTMTagger(EMBEDDING_DIM,HIDDEN_DIM,len(vocab.keys()), len(tag.keys()))
model.load_state_dict(torch.load('model_file.pth'))
model.eval()


# #Testing
# tests=['which is the max spend  in  may  for  2017  for  alaska','which is the highest spending site','which is the max spend  in  may  for  2017  for  sitegroup alaska']
#
# testing_statement=tests[2]
# l=testing_statement.split()
# model_test_statement=[]
#
# for i in l:
#     stemed_word = nltk.PorterStemmer().stem(i)
#     lemmetized_word = nltk.WordNetLemmatizer().lemmatize(i)
#     if i in vocab.keys():
#         model_test_statement.append(vocab[i])
#     elif stemed_word in vocab.keys():
#         model_test_statement.append(vocab[stemed_word])
#     elif lemmetized_word in vocab.keys():
#         model_test_statement.append(vocab[lemmetized_word])
#     else:
#         model_test_statement.append(208)
#
# if len(model_test_statement)<25:
#     for i in range(len(model_test_statement),25):
#         model_test_statement.append(208)
#
# st=torch.tensor(model_test_statement,dtype=torch.long)
# f= model(st)
#
# [print(list(tag.keys())[i],end=" ") for i in f.max(dim=1).indices]
