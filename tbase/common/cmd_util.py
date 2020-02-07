# -*- coding:utf-8 -*-

import os
import random

import numpy as np

from tgym.market import Market
from tgym.scenario import make_env as _make_env


def set_global_seeds(seed):
    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True
    except ImportError:
        pass
    np.random.seed(seed)
    random.seed(seed)


def make_env(args):
    """
    Create a wrapped, monitored gym.Env for Tgym.
    """
    ts_token = os.getenv("TUSHARE_TOKEN")
    codes = args.codes.split(",")
    indexs = args.indexs.split(",")

    m = Market(
            ts_token=ts_token,
            start=args.start,
            end=args.end,
            codes=codes,
            indexs=indexs,
            data_dir=args.data_dir)
    env = _make_env(
        scenario=args.scenario,
        market=m,
        investment=args.investment,
        look_back_days=args.look_back_days)
    return env


def common_arg_parser():
    """
    Create an argparse.ArgumentParser for run_mujoco.py.
    """
    import argparse
    parser = argparse.ArgumentParser("reinforcement learning trade agents")
    # 环境
    parser.add_argument('--scenario', help='environment scenario', type=str,
                        default='multi_vol')
    parser.add_argument("--codes", type=str, default="000001.SZ,000002.SZ",
                        help="tushare code of the experiment stocks")
    parser.add_argument("--indexs", type=str, default="000001.SH,399001.SZ",
                        help="tushare code of the indexs")
    parser.add_argument("--start", type=str, default='20190101',
                        help="when start the game")
    parser.add_argument("--end", type=str, default='20191231',
                        help="when end the game")
    parser.add_argument("--investment", type=float, default=100000,
                        help="the investment for each stock")
    parser.add_argument("--look_back_days", type=int, default=10,
                        help="how many days shoud look back")
    parser.add_argument("--data_dir", type=str, default='/tmp/tgym',
                        help="directory for tgym store trade data")
    parser.add_argument('--num_env', default=2, type=int,
                        help='Number of environment copies run in parallel.')
    # 训练参数
    parser.add_argument('--seed', help='RNG seed', type=int, default=None)
    parser.add_argument('--alg', help='Algorithm', type=str, default='ppo2')
    parser.add_argument('--max_episode', type=float, default=1000)
    # 模型参数
    parser.add_argument('--policy_net', default=None,
                        help='network type (mlp, lstm, cnn_lstm)')
    parser.add_argument('--value_net', default=None,
                        help='network type (mlp, lstm_mpl)')
    parser.add_argument('--save_path', help='Path to save trained model to',
                        default=None, type=str)
    parser.add_argument('--log_path', default=None, type=str,
                        help='Directory to save learning curve data.')
    # 运行参数
    parser.add_argument('--play', default=False, action='store_true')
    return parser.parse_args()