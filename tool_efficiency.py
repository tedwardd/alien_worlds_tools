#!/usr/bin/env python3

import json
from pathlib import Path
import click
import itertools
import sys


def remove_n_smallest(lst, n):
    if len(lst) == 3:
        if lst[0] == lst[1] and lst[1] == lst[2]:
            del lst[0]
            return lst
        for _ in range(n):
            m = min(lst)
            lst[:] = (x for x in lst if x != m)
        return lst
    return lst


@click.command()
@click.option(
    "-r",
    "--rarity",
    "rarities",
    multiple=True,
    required=False,
    type=str,
    default=None,
    show_default="all",
)
@click.option(
    "-m",
    "--multiplier",
    required=False,
    type=float,
    default=1,
    show_default="1",
)
@click.option(
    "-p",
    "--power-multiplier",
    required=False,
    type=float,
    default=1,
    show_default="1",
)
@click.option(
    "-l",
    "--luck-multiplier",
    required=False,
    type=float,
    default=1,
    show_default="1",
)
@click.option(
    "--allow-duplicate",
    is_flag=True,
)
@click.option(
    "--summary",
    is_flag=True,
)
@click.option(
    "--tool",
    "-t",
    "tools",
    required=False,
    type=str,
    default=None,
    multiple=True,
)
@click.option(
    "--supply",
    "-s",
    required=False,
    default=20,
)
def main(
    rarities,
    multiplier,
    allow_duplicate,
    summary,
    tools,
    supply,
    power_multiplier,
    luck_multiplier,
):

    if rarities and tools:
        click.secho(
            "Can not specify rarities and tools at the same time.", fg="red", bold=True
        )
        sys.exit(1)

    tools_filename = "tools.json"

    useable = []
    tools_obj = json.loads(Path(tools_filename).read_bytes())
    if rarities is None and tools is None:
        useable = list(tools_obj.keys())
    if tools is not None:
        for tool in tools:
            if tool not in list(tools_obj):
                click.secho(
                    f"{tool} is not a valid tool. Choose from list below:",
                    bold=True,
                    fg="red",
                )
                print("\n".join(list(tools_obj)))
                sys.exit(1)
            useable.append(tool)
    if rarities is not None:
        for tool in tools_obj:
            if tools_obj.get(tool).get("rarity") in rarities:
                useable.append(tool)

    if allow_duplicate:
        three_tools = list(itertools.combinations_with_replacement(useable, 3))
        two_tools = list(itertools.combinations_with_replacement(useable, 2))

    else:
        three_tools = list(itertools.combinations(useable, 3))
        two_tools = list(itertools.combinations(useable, 2))
    all_bags = three_tools + two_tools

    tlm_scores = {}
    luck_scores = {}
    for bag in all_bags:
        charge_times = []
        tlm = []
        luck = []
        for tool in bag:
            charge_times.append(tools_obj.get(tool).get("charge_time"))
            tlm.append(tools_obj.get(tool).get("tlm"))
            luck.append(tools_obj.get(tool).get("luck"))
        charge_times = remove_n_smallest(charge_times, 1)
        tlm_total = sum(tlm) * power_multiplier
        charge_total = sum(charge_times) * multiplier
        luck_total = sum(luck) * luck_multiplier
        tlm_per_min = ((tlm_total / 100) * supply) / charge_total * 60
        luck_per_min = luck_total
        if not summary:
            click.secho(f"{bag}", bold=True)
            click.echo(
                f"TLM/min: {round(tlm_per_min, 3)} // {round((tlm_total/100) * supply, 3)}/attempt"
            )
            click.echo(f"luck: {luck_total}")
            click.secho(f"------------------------", bold=True)
        tlm_scores.update({round(tlm_per_min, 3): bag})
        luck_scores.update({luck_per_min: bag})
    top_tlm = max(list(tlm_scores))
    top_luck = max(list(luck_scores))
    click.secho("Best overall combo for average TLM/min", bold=True, fg="green")
    click.secho(f"{tlm_scores.get(top_tlm)}: {top_tlm} TLM/min", fg="green")
    click.secho(f"{luck_scores.get(top_luck)}: {top_luck} Luck", fg="green")


if __name__ == "__main__":
    main()
