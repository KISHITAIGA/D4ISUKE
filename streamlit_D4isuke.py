import streamlit as st
import time
from PIL import Image
import pandas as pd
import numpy as np
import math
import random

def calculate_damage_range(attack_power, skill_power, defense_power, type_multiplier, attack_rank, defense_rank, item_multiplier):
    # 攻撃ランクに応じたダメージ倍率を計算
    if attack_rank == 0:
        damage_multiplier = 1.0
    elif attack_rank < 0:
        damage_multiplier = 2 / (2 - attack_rank)
    else:
        damage_multiplier = 1.5 + (attack_rank - 1) * 0.5

    # 防御ランクに応じたダメージ倍率を計算
    if defense_rank == 0:
        defense_multiplier = 1.0
    elif defense_rank < 0:
        defense_multiplier = 2 / (2 - defense_rank)
    else:
        defense_multiplier = 1.5 + (defense_rank - 1) * 0.5

    # アイテムによるダメージ倍率を計算
    item_multiplier = 1.0 if item_multiplier == "なし" else 1.5 if item_multiplier == "こだわり" else 1.3 if item_multiplier == "いのちのたま" else 1.2

    # ダメージ計算式に基づいて計算
    damage = (
        22 * skill_power * attack_power / defense_power // 50 + 2
    )

    # タイプ相性に基づいてダメージを補正
    damage *= type_multiplier

    # 攻撃ランクに応じてダメージを補正
    damage *= damage_multiplier

    # 防御ランクに応じてダメージを補正
    damage /= defense_multiplier

    # アイテムによるダメージを補正
    damage *= item_multiplier

    # 計算されたダメージの範囲を取得（0.85 ～ 1.00）
    min_damage = int(math.floor(damage * 0.85))
    max_damage = int(math.floor(damage * 1.00))

    return min_damage, max_damage

def calculate_kill_probability(attack_power, skill_power, defense_power, defense_hp, type_multiplier, attack_rank):
    # ダメージの範囲を計算
    min_damage, max_damage = calculate_damage_range(attack_power, skill_power, defense_power, type_multiplier, attack_rank)

    # 一撃で倒せる確率を計算
    if max_damage < defense_hp:
        probability = 0.0
    else:
        probability = (max_damage - defense_hp + 1) / (max_damage - min_damage + 1)

    return probability

def calculate_required_attacks(attack_power, skill_power, defense_power, defense_hp, type_multiplier, attack_rank):
    # ダメージの範囲を計算
    min_damage, max_damage = calculate_damage_range(attack_power, skill_power, defense_power, type_multiplier, attack_rank)

    # 一撃で倒せる確率が0%の場合、必要な攻撃回数を計算
    if max_damage < defense_hp:
        required_attacks = math.ceil(defense_hp / max_damage)
    else:
        required_attacks = 0  # 一撃で倒せる場合

    return required_attacks

def main():
    st.title("ダメージ計算ツール")

    # 攻撃力の実数値を入力
    attack_power = st.number_input("攻撃力の実数値を入力してください", min_value=0)

    # 技の威力を入力
    skill_power = st.number_input("技の威力を入力してください", min_value=0)

    # 攻撃ランクを選択
    attack_rank = st.slider("攻撃ランク", min_value=-6, max_value=6, step=1, value=0)

    # 防御側の防御実数値を入力
    defense_power = st.number_input("防御側の防御実数値を入力してください", min_value=0)

    # 防御ランクを選択
    defense_rank = st.slider("防御ランク", min_value=-6, max_value=6, step=1, value=0)

    # 攻撃側の持ち物を選択
    item_multiplier = st.selectbox("攻撃側の持ち物", ["なし", "こだわり", "いのちのたま", "タイプ強化系"])

    # 防御側のHPを入力
    defense_hp = st.number_input("防御側のHPを入力してください", min_value=0)

    # タイプ相性を選択
    type_effectiveness = st.selectbox("タイプ相性", ["こうかはばつぐんだ！", "こうかはふつうだ", "こうかはいまひとつのようだ…"])

    # タイプ相性に基づいた補正値を設定
    if type_effectiveness == "こうかはばつぐんだ！":
        type_multiplier = 2.0
    elif type_effectiveness == "こうかはふつうだ":
        type_multiplier = 1.0
    else:
        type_multiplier = 0.5

    # ダメージ計算のボタン
    if st.button("ダメージ計算"):
        min_damage, max_damage = calculate_damage_range(attack_power, skill_power, defense_power, type_multiplier, attack_rank, defense_rank, item_multiplier)

        # 一撃で倒せる確率を計算
        probability = calculate_kill_probability(attack_power, skill_power, defense_power, defense_hp, type_multiplier, attack_rank)

        # 必要な攻撃回数を計算
        required_attacks = calculate_required_attacks(attack_power, skill_power, defense_power, defense_hp, type_multiplier, attack_rank)

        # 結果を表示
        if probability == 0.0:
            st.success(f"計算されたダメージの範囲: {min_damage} ～ {max_damage}\n一撃で倒せる確率: 0%\n必要な攻撃回数: {required_attacks}回")
        else:
            st.success(f"計算されたダメージの範囲: {min_damage} ～ {max_damage}\n一撃で倒せる確率: {probability * 100}%\n必要な攻撃回数: {required_attacks}回")

# アプリの実行
if __name__ == "__main__":
    main()
