import importlib
import os

TEMPLATE_DIR = "templates"

def load_strategy_map():
    strategy_map = {}

    for file in os.listdir(TEMPLATE_DIR):
        if file.endswith(".py") and not file.startswith("__"):
            
            module_name = file[:-3]  # 去掉 .py
            
            module = importlib.import_module(f"templates.{module_name}")
            
            if hasattr(module, "generate"):
                strategy_map[module_name] = module.generate

    return strategy_map


STRATEGY_MAP = load_strategy_map()


def generate_strategy_code(params):
    strategy_type = params.get("strategy_type")

    if strategy_type not in STRATEGY_MAP:
        raise ValueError(f"未知策略类型: {strategy_type}")

    return STRATEGY_MAP[strategy_type](params)