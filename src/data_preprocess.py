import json


def main():
    with open("data/raw_data.json") as in_data:
        data_list = json.load(in_data)

    data_dic = dict()
    for d in data_list:
        data_dic[d["id"]] = d

    all_bonuses = set()

    for value in data_dic.values():
        del value["id"]
        del value["rarity"]
        del value["baseDamage"]
        del value["location"]
        del value["captureChance"]
        del value["pity"]
        del value["expeditionBonuses"]

        bonus_list = []
        for bonus in value["bonuses"]:
            bonus_list.append(bonus["name"])

        value["bonuses"] = bonus_list
        all_bonuses.update(bonus_list)

    with open("data/processed_data.json", "w") as output_data:
        json.dump(data_dic, output_data, indent=2, sort_keys=True)

    all_bonuses = list(all_bonuses)
    all_bonuses.sort()

    with open("data/all_bonuses.json", "w") as output_data:
        json.dump(all_bonuses, output_data, indent=2)


if __name__ == "__main__":
    main()
