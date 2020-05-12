import nltk,numpy as np,pandas as pd, re,os,random
import torch


# word list creation
with open('sents.txt') as f:
    x=f.read()

x=x.split('\n')
wl=[]
[[wl.append(words) for words in i.split()] for i in x]

words=set(wl)

#labels list creation
with open("labels.txt") as f:
    x1=f.read()

x1=x1.split('\n')

ll=[]
[[ll.append(words) for words in i.split()] for i in x1]

labels=set(ll)

# Declaring dict for vocab and tags
tag={}
vocab={}
for i, word in enumerate(words):
    vocab[word] = i

for i, tags in enumerate(labels):
    tag[tags] = i

train_sent=[[vocab[a] for a in a1.split()] for a1 in x]
train_label=[[tag[a] for a in a1.split()] for a1 in x1]


batch_data,batch_labels=torch.LongTensor(train_sent),torch.LongTensor(train_label)
batch_data,batch_labels=torch.autograd.Variable(batch_data),torch.autograd.Variable(batch_labels)
F= torch.nn.functional
nn=torch.nn


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

    for epoch in range(300):  # again, normally you would NOT do 300 epochs, it is toy data
        for i in range(8):
        # for sentence, tags in batch_data,batch_labels:
            # Step 1. Remember that Pytorch accumulates gradients.
            # We need to clear them out before each instance
            model.zero_grad()

            # Step 2. Get our inputs ready for the network, that is, turn them into
            # Tensors of word indices.
            # sentence_in = prepare_sequence(sentence, word_to_ix)
            # targets = prepare_sequence(tags, tag_to_ix)

            # Step 3. Run our forward pass.
            tag_scores = model(batch_data[i])

            # Step 4. Compute the loss, gradients, and update the parameters by
            #  calling optimizer.step()
            loss = loss_function(tag_scores, batch_labels[i])
            loss.backward()
            optimizer.step()


#Testing
f=model(batch_data[0])
[print(list(tag.keys())[i]) for i in f.max(dim=1).indices]