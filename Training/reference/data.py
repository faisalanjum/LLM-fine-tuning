# Dataset classes, collate_fn, and the create_dataloader / loader builders.

import json
import requests
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
import torch
from torch.utils.data import Dataset


def load_instruction_data():
    path = Path(__file__).resolve().parent.parent / "data/downloads/instruction-data.json"

    # Download and save only if the file is missing.
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        url = "https://raw.githubusercontent.com/rasbt/LLMs-from-scratch/main/ch07/01_main-chapter-code/instruction-data.json"
        response = requests.get(url)
        response.raise_for_status()
        path.write_text(response.text, encoding="utf-8")

    return json.loads(path.read_text(encoding="utf-8"))


def load_dpo_data():
    path = Path(__file__).resolve().parent.parent / "data/downloads/instruction-data-with-preference.json"

    # Download and save only if the file is missing.
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        url = "https://raw.githubusercontent.com/rasbt/LLMs-from-scratch/main/ch07/04_preference-tuning-with-dpo/instruction-data-with-preference.json"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        path.write_text(response.text, encoding="utf-8")

    return json.loads(path.read_text(encoding="utf-8"))



def load_pretraining_data(
    file_name="the-verdict.txt",
    url="https://raw.githubusercontent.com/rasbt/LLMs-from-scratch/main/ch02/01_main-chapter-code/the-verdict.txt",
):
    path = Path(__file__).resolve().parent.parent / "data/downloads" / file_name

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        path.write_bytes(response.content)

    return path.read_text(encoding="utf-8")



def load_spam_data():
    import pandas as pd

    path = Path(__file__).resolve().parent.parent / "data/downloads/SMSSpamCollection.tsv"

    # Download and save only if the file is missing.
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        url = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with ZipFile(BytesIO(response.content)) as archive:
            path.write_bytes(archive.read("SMSSpamCollection"))

    return pd.read_csv(path, sep="\t", header=None, names=["Label", "Text"])


def create_balanced_dataset(df):
    num_spam       = len(df[df['Label'] == 'spam'])
    ham_sample     = df[df['Label'] == 'ham'].sample(num_spam, random_state=123)
    balanced_df    = pd.concat([ham_sample, df[df['Label'] == 'spam']])
    return balanced_df


def random_split(df, train_frac, val_frac):
    df        = df.sample(frac=1, random_state=123).reset_index(drop=True)
    train_end = int(len(df) * train_frac)
    val_end   = train_end + int(len(df) * val_frac)

    train_df  = df.iloc[:train_end]
    val_df    = df.iloc[train_end:val_end]
    test_df   = df.iloc[val_end:]

    return train_df, val_df, test_df


class SpamDataset(Dataset):

    def __init__(self, data, tokenizer, max_length = None):
        
        self.data = data
        self.pad_token_id = [tokenizer.eot_token]
        self.encoded_texts =[tokenizer.encode(text) for text in self.data['Text']]

        if max_length is None:
            self.max_length = self._longest_encoded_length()

        else:
            self.max_length = max_length
            self.encoded_texts = [encoded_text[:self.max_length] for encoded_text in self.encoded_texts]


        self.encoded_texts = [encoded_text + self.pad_token_id * 
                             (self.max_length - len(encoded_text)) 
                             for encoded_text in self.encoded_texts]


    def __getitem__(self,index):
        input_tokens  = torch.tensor(self.encoded_texts[index], dtype=torch.long)
        target_tokens = torch.tensor(self.data.iloc[index]['Label'], dtype=torch.long)
        
        return input_tokens, target_tokens

    
    def __len__(self):
        return len(self.data)

    def _longest_encoded_length(self):
        max_length = 0
        for encoded_text in self.encoded_texts:
            encoded_length = len(encoded_text)
            if encoded_length > max_length:
                max_length = encoded_length
        return max_length

