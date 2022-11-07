from torch.utils.data import Dataset
import torch
import random
import numpy as np
from collections import defaultdict

class LogDataset(Dataset):
    def __init__(self, log_corpus, time_corpus, vocab, seq_len, corpus_lines=None, encoding="utf-8", on_memory=True, predict_mode=False, mask_ratio=0.15):
        """

        :param corpus: log sessions/line
        :param vocab: log events collection including pad, ukn ...
        :param seq_len: max sequence length
        :param corpus_lines: number of log sessions
        :param encoding:
        :param on_memory:
        :param predict_mode: if predict
        """
        self.vocab = vocab
        self.seq_len = seq_len

        self.on_memory = on_memory
        self.encoding = encoding

        self.predict_mode = predict_mode
        self.log_corpus = log_corpus
        self.time_corpus = time_corpus
        self.corpus_lines = len(log_corpus)

        self.mask_ratio = mask_ratio
        self.add_special_tokens = True

        self.scalar_i = set()

        for token in self.vocab.stoi:
            if token.isdigit() and int(token) >= 90:
                self.scalar_i.add(self.vocab.stoi[token])

    def __len__(self):
        return self.corpus_lines

    def __getitem__(self, idx):
        k, t = self.log_corpus[idx], self.time_corpus[idx]

        k_masked, k_label, t_masked, t_label = self.random_item(k, t)

        # [CLS] tag = SOS tag, [SEP] tag = EOS tag
        
        # k_label = [self.vocab.sos_index] + k_label
        if self.add_special_tokens:
            new_k_masked = []
            new_k_label = []
            new_t_masked = []
            new_t_label = []

            for idx, i in enumerate(k):
                if i in self.scalar_i:
                    new_k_masked.append(self.vocab.scalar_index)
                else:
                    if (i == 0) or (i >= 1 and k[idx - 1] in self.scalar_i):
                        new_k_masked.append(self.vocab.log_index)
                
                new_k_label.append(0)
                new_k_masked.append(k_masked[idx])
                new_k_label.append(k_label[idx])

                new_t_masked.append(0)
                new_t_label.append(0)
                new_t_masked.append(t_masked[idx])
                new_t_label.append(t_label[idx])
            
            new_k_masked = [self.vocab.sos_index] + new_k_masked
            new_k_label = [self.vocab.pad_index] + new_k_label

            new_t_masked = [0] + new_t_masked
            new_t_label = [self.vocab.pad_index] + new_t_label

            return new_k_masked, new_k_label, new_t_masked, new_t_label
        
        k = [self.vocab.sos_index] + k_masked
        k_label = [self.vocab.pad_index] + k_label

        t = [0] + t_masked
        t_label = [self.vocab.pad_index] + t_label

        return k, k_label, t, t_label

    def random_item(self, k, t):
        tokens = list(k)
        new_tokens = []
        output_label = []
        new_output_label = []

        time_intervals = list(t)
        time_label = []

        # print(time_intervals)

        for i, token in enumerate(tokens):
            time_int = time_intervals[i]

            # add scalars special keys
            # if self.add_special_tokens:
            #     if int(token) < 90:
            #         new_tokens.append(self.vocab.log_index)
            #     else:
            #         new_tokens.append(self.vocab.scalar_index)
                
            #     new_output_label.append(0)
                
            #     time_intervals.append(0)
            #     time_label.append(0)

            
            prob = random.random()
            # replace 15% of tokens in a sequence to a masked token
            if prob < self.mask_ratio:
                # raise AttributeError("no mask in visualization")

                if self.predict_mode:
                    tokens[i] = self.vocab.mask_index
                    output_label.append(self.vocab.stoi.get(token, self.vocab.unk_index))

                    time_label.append(time_int)
                    time_intervals[i] = 0

                    # if self.add_special_tokens:
                    #     new_tokens.append(self.vocab.mask_index)
                    #     new_output_label.append(self.vocab.stoi.get(token, self.vocab.unk_index))

                    continue

                prob /= self.mask_ratio

                # 80% randomly change token to mask token
                if prob < 0.8:
                    tokens[i] = self.vocab.mask_index

                    # if self.add_special_tokens:
                    #     new_tokens.append(self.vocab.mask_index)

                # 10% randomly change token to random token
                elif prob < 0.9:
                    tokens[i] = random.randrange(len(self.vocab))

                    # if self.add_special_tokens:
                    #     new_tokens.append(random.randrange(len(self.vocab)))

                # 10% randomly change token to current token
                else:
                    tokens[i] = self.vocab.stoi.get(token, self.vocab.unk_index)

                    # if self.add_special_tokens:
                    #     new_tokens.append(self.vocab.stoi.get(token, self.vocab.unk_index))

                output_label.append(self.vocab.stoi.get(token, self.vocab.unk_index))

                time_intervals[i] = 0  # time mask value = 0
                time_label.append(time_int)

            else:
                tokens[i] = self.vocab.stoi.get(token, self.vocab.unk_index)
                
                # if self.add_special_tokens:
                #     new_tokens.append(self.vocab.stoi.get(token, self.vocab.unk_index))

                output_label.append(0)
                new_output_label.append(0)
                time_label.append(0)
        
        # if self.add_special_tokens:
        #     return new_tokens, new_output_label, time_intervals, time_label

        return tokens, output_label, time_intervals, time_label

    def collate_fn(self, batch, percentile=100, dynamical_pad=True):
        lens = [len(seq[0]) for seq in batch]

        # find the max len in each batch
        if dynamical_pad:
            # dynamical padding
            seq_len = int(np.percentile(lens, percentile))
            if self.seq_len is not None:
                seq_len = min(seq_len, self.seq_len)
        else:
            # fixed length padding
            seq_len = self.seq_len

        output = defaultdict(list)
        for seq in batch:
            bert_input = seq[0][:seq_len]
            bert_label = seq[1][:seq_len]
            time_input = seq[2][:seq_len]
            time_label = seq[3][:seq_len]

            padding = [self.vocab.pad_index for _ in range(seq_len - len(bert_input))]
            bert_input.extend(padding), bert_label.extend(padding), time_input.extend(padding), time_label.extend(
                padding)

            time_input = np.array(time_input)[:, np.newaxis]
            output["bert_input"].append(bert_input)
            output["bert_label"].append(bert_label)
            output["time_input"].append(time_input)
            output["time_label"].append(time_label)

        output["bert_input"] = torch.tensor(output["bert_input"], dtype=torch.long)
        output["bert_label"] = torch.tensor(output["bert_label"], dtype=torch.long)
        output["time_input"] = torch.tensor(output["time_input"], dtype=torch.float)
        output["time_label"] = torch.tensor(output["time_label"], dtype=torch.float)

        return output

