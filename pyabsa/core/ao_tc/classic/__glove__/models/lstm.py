# -*- coding: utf-8 -*-
# file: lstm.py
# author: songyouwei <youwei0314@gmail.com>
# Copyright (C) 2018. All Rights Reserved.

import torch
import torch.nn as nn

from ..layers.dynamic_rnn import DynamicLSTM


class LSTM(nn.Module):
    inputs = ['text_indices']

    def __init__(self, embedding_matrix, opt):
        super(LSTM, self).__init__()
        self.embed = nn.Embedding.from_pretrained(torch.tensor(embedding_matrix, dtype=torch.float))
        self.lstm = DynamicLSTM(opt.embed_dim, opt.hidden_dim, num_layers=1, batch_first=True)
        self.dense1 = nn.Linear(opt.hidden_dim, opt.polarities_dim1)
        self.dense2 = nn.Linear(opt.hidden_dim, opt.polarities_dim2)

    def forward(self, inputs):
        text_raw_indices = inputs[0]
        x = self.embed(text_raw_indices)
        x_len = torch.sum(text_raw_indices != 0, dim=-1)
        _, (h_n, _) = self.lstm(x, x_len)
        out1 = self.dense1(h_n[0])
        out2 = self.dense2(h_n[0])
        return out1, out2
