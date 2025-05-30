import os
from dataclasses import dataclass, field
from typing import Optional, List

from transformers import TrainingArguments


def default_list() -> List[str]:
    return ["q_proj", "k_proj", "v_proj", "o_proj", "down_proj", "up_proj", "gate_proj"]


@dataclass
class ModelArguments:
    """
    Arguments pertaining to which model/config/tokenizer we are going to fine-tune from.
    """

    model_name_or_path: str = field(
        metadata={"help": "Path to pretrained model or model identifier from huggingface.co/models"}
    )

    peft_model_path: str = field(
        default=''
    )
    config_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained config name or path if not the same as model_name"}
    )
    tokenizer_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained tokenizer name or path if not the same as model_name"}
    )
    use_lora: bool = field(
        default=True,
        metadata={"help": "If passed, will use LORA (low-rank parameter-efficient training) to train the model."}
    )
    lora_rank: int = field(
        default=64,
        metadata={"help": "The rank of lora."}
    )
    lora_alpha: float = field(
        default=16,
        metadata={"help": "The alpha parameter of lora."}
    )
    lora_dropout: float = field(
        default=0.1,
        metadata={"help": "The dropout rate of lora modules."}
    )
    target_modules: List[str] = field(
        default_factory=default_list
    )
    save_merged_lora_model: bool = field(
        default=False,
        metadata={"help": "If passed, will merge the lora modules and save the entire model."}
    )
    use_flash_attn: bool = field(
        default=True,
        metadata={"help": "If passed, will use flash attention to train the model."}
    )
    use_slow_tokenizer: bool = field(
        default=False,
        metadata={"help": "If passed, will use a slow tokenizer (not backed by the 🤗 Tokenizers library)."}
    )
    low_cpu_mem_usage: bool = field(
        default=False,
        metadata={"help": "It is an option to create the model as an empty shell,"
                          "then only materialize its parameters when the pretrained weights are loaded."
                          "If passed, LLM loading time and RAM consumption will be benefited."}
    )
    cache_dir: str = field(
        default="tmp", metadata={"help": "the cache of the model"}
    )
    token: str = field(
        default=None, metadata={"help": "the token to access the huggingface model"}
    )
    from_peft: str = field(
        default=None
    )
    lora_extra_parameters: str = field(
        default=None
    )
    compress_method: str = field(
        default='mean'
    )
    padding_side: str = field(
        default='left'
    )
    compress_layers: List[int] = field(
        default=None
    )
    compress_ratios: List[int] = field(
        default=None
    )
    start_layer: int = field(
        default=None
    )
    layer_sep: int = field(
        default=None
    )
    layer_wise: bool = field(
        default=False
    )
    train_method: str = field(
        default='distill'
    )
    raw_peft: List[str] = field(
        default=None
    )
    finetune_type: str = field(
        default='layer'
    )

@dataclass
class DataArguments:
    train_data: List[str] = field(
        default=None, metadata={"help": "Path to train data"}
    )

    train_group_size: int = field(default=8)

    query_max_len: int = field(
        default=32,
        metadata={
            "help": "The maximum total input sequence length after tokenization for passage. Sequences longer "
                    "than this will be truncated, sequences shorter will be padded."
        },
    )

    passage_max_len: int = field(
        default=128,
        metadata={
            "help": "The maximum total input sequence length after tokenization for passage. Sequences longer "
                    "than this will be truncated, sequences shorter will be padded."
        },
    )

    max_example_num_per_dataset: int = field(
        default=100000000, metadata={"help": "the max number of examples for each dataset"}
    )

    query_instruction_for_retrieval: str = field(
        default="A: ", metadata={"help": "query: "}
    )
    passage_instruction_for_retrieval: str = field(
        default="B: ", metadata={"help": "passage: "}
    )

    cache_path: str = field(
        default='./data_dir'
    )

    load_from_disk: bool = field(
        default=False, metadata={"help": " whether load the data from disk"}
    )

    load_disk_path: str = field(
        default=None, metadata={"help": " the path to load the data", "nargs": "+"}
    )

    save_to_disk: bool = field(
        default=False, metadata={"help": " whether save the data to disk"}
    )

    save_disk_path: str = field(
        default=None, metadata={"help": " the path to save the data"}
    )

    num_shards: int = field(
        default=0, metadata={
            "help": "number of shards to write, prior than `save_max_shard_size`, default depends on `save_max_shard_size`"}
    )

    save_max_shard_size: str = field(
        default="50GB", metadata={"help": "the max size of the shard"}
    )

    exit_after_save: bool = field(
        default=False, metadata={"help": " whether exit after save the data"}
    )

    # def __post_init__(self):
    #     if not os.path.exists(self.train_data):
    #         raise FileNotFoundError(f"cannot find file: {self.train_data}, please set a true path")

@dataclass
class RetrieverTrainingArguments(TrainingArguments):
    loss_type: str = field(default='only logits')
    temperature: float = field(default=1.0)
