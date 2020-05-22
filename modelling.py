import torch
import nltk, os

# train_data = [
#     ("Uber blew through $1 million a week", [(0, 4, 'ORG')]),
#     ("Android Pay expands to Canada", [(0, 11, 'PRODUCT'), (23, 30, 'GPE')]),
#     ("Spotify steps up Asia expansion", [(0, 8, "ORG"), (17, 21, "LOC")]),
#     ("Google Maps launches location sharing", [(0, 11, "PRODUCT")]),
#     ("Google rebrands its business apps", [(0, 6, "ORG")]),
#     ("look what i found on google! 😂", [(21, 27, "PRODUCT")])

model_file = "model_file.pth"
sent_data = []
label_data = []
# word list creation
with open(r'data\sents.txt') as f:
    for sentence in f.read().splitlines():
        sent_data.append(sentence.split())

# sent_data=sent_data.split()
word_list = []
[[word_list.append(words) for words in i] for i in sent_data]
words = list(set(word_list))
words.sort()


# labels list creation
with open("data\labels.txt") as f:
    for label in f.read().splitlines():
        label_data.append(label.split())

label_list = []
[[label_list.append(words) for words in i] for i in label_data]
labels = list(set(label_list))
labels.sort()


# Declaring dict for vocab and tags
tags = {}
vocab = {}
indx2word = {}
indx2tag = {}

for i, word in enumerate(words):
    vocab[word] = i
    indx2word[i] = word
for i, tag in enumerate(labels):
    tags[tag] = i
    indx2tag[i] = tag

vocab['PAD'] = len(vocab.keys())
tags['PAD'] = len(tags.keys())
indx2word[len(indx2word.keys())]='PAD'
indx2tag[len(indx2tag.keys())]='PAD'


batch_max_len = max([len(i) for i in sent_data])

train_sent = vocab['PAD'] * torch.ones(len(label_data), batch_max_len, dtype=torch.long)
train_label = tags['PAD'] * torch.ones(len(label_data), batch_max_len, dtype=torch.long)

for j in range(len(label_data)):
    cur_len = len(label_data[j])
    for k in range(cur_len):
        train_sent[j][k] = vocab[sent_data[j][k]]
        train_label[j][k] = tag[label_data[j][k]]

batch_data, batch_labels = train_sent, train_label
batch_data, batch_labels = torch.autograd.Variable(batch_data), torch.autograd.Variable(batch_labels)
F = torch.nn.functional
nn = torch.nn
optim = torch.optim


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
model = LSTMTagger(EMBEDDING_DIM, HIDDEN_DIM, len(vocab.keys()), len(tags.keys()))
loss_function = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

for epoch in range(2):
    for i in range(len(batch_data)):  # len(batch_data)):
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
    print(loss, epoch)

torch.save(model.state_dict(), model_file)
