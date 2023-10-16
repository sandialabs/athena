"""
MIT License

Copyright (c) 2023 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

""" Used to gather the timeloop-mapper stats into a single
    csv file. Borrows some functionality from the
    `parse_timeloop_output.py` script that works on only one
    output file at a time.
"""

# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of NVIDIA CORPORATION nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


## Dependencies
import os, re
import pprint
import pickle
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path
from natsort import index_natsorted


### Helper Functions
def get_stat(stats, stat, cast):
    """Helper function used in main parser;
    taken from `parse_timeloop_output.py`
    """
    items = stats.findall(stat)[0].findall("PerDataSpace")[0].findall("item")
    count = len(items)
    out = np.array([0] * count, dtype=cast)
    for j in range(count):
        if stat == "ingresses":
            value = sum([cast(i.text) for i in items[j].findall("item")])
        else:
            value = cast(items[j].text)
        out[j] = value

    return out


def parse_timeloop_stats(filepath):
    """Main parse of timeloop xml stats. See
    `parse_timeloop_output.py` for more details.
    """
    tree = ET.parse(filepath)
    root = tree.getroot()

    # parse the problem shape
    prob_dims = (
        root.findall("a")[0]
        .findall("workload_")[0]
        .findall("bounds_")[0]
        .findall("item")
    )
    prob = [int(pd.findall("second")[0].text) for pd in prob_dims]
    macs = np.prod(prob)
    topology = root.findall("engine")[0].findall("topology_")[0]

    # get storage and arithmetic levels
    levels = topology.findall("levels_")[0]
    num_levels = int(levels.findall("count")[0].text)
    level_ptrs = levels.findall("item")

    # list of networks
    networks = topology.findall("networks_")[0]
    num_networks = int(networks.findall("count")[0].text)
    network_ptrs = networks.findall("item")

    # dict for storing energy stats and flag for arithmetic level
    energy_summary_pJ = {}
    arithmetic_level_found = False

    # go through each level of the xml file and grab that level's stats
    for level_ptr in level_ptrs:
        # set level based on pointer
        level = level_ptr.findall("px")[0]

        # check for only one arithmetic level
        if (
            "class_id" in level.attrib
            and level.attrib["class_name"] == "model::ArithmeticUnits"
        ):
            assert arithmetic_level_found == False
            arithmetic_level_found = True
            cycles = int(level.findall("cycles_")[0].text)
            utilized_instances = float(level.findall("utilized_instances_")[0].text)
            total_instances_list = (
                level.findall("specs_")[0].findall("instances")[0].findall("t_")
            )

            # check if no mapping was returned
            if not total_instances_list:
                # set dummy values
                total_instances = 1
            else:
                # get total instances to find utilization numbers
                total_instances = float(
                    level.findall("specs_")[0]
                    .findall("instances")[0]
                    .findall("t_")[0]
                    .text
                )

            # find utilization numbers
            arithmetic_utilization = utilized_instances / total_instances

            # add to summary
            energy_summary_pJ["MAC"] = {
                "energy": float(level.findall("energy_")[0].text),
                "utilization": arithmetic_utilization,
            }
            continue

        # other level specifications and stats
        specs = level.findall("specs_")[0]
        stats = level.findall("stats_")[0]
        generic_level_specs = specs.findall("LevelSpecs")[0]
        level_name = generic_level_specs.findall("level_name")[0].text

        # memory accesses
        reads_per_instance = get_stat(stats, "reads", int)
        updates_per_instance = get_stat(stats, "updates", int)
        fills_per_instance = get_stat(stats, "fills", int)
        accesses_per_instance = (
            reads_per_instance + updates_per_instance + fills_per_instance
        )

        # utilization numbers
        capacity = get_stat(stats, "utilized_capacity", int)
        instances = get_stat(stats, "utilized_instances", int)
        clusters = get_stat(stats, "utilized_clusters", int)

        total_instances_obj = specs.findall("instances")[0].findall("t_")
        if not len(total_instances_obj):
            total_instances = sum(instances)
        else:
            total_instances = int(total_instances_obj[0].text)

        total_capacity_obj = specs.findall("size")[0].findall("t_")
        if not len(total_capacity_obj):
            total_capacity = sum(capacity)
        else:
            total_capacity = int(total_capacity_obj[0].text)

        # energy for memory accesses
        energy_per_access_per_instance = get_stat(stats, "energy_per_access", float)
        storage_access_energy_in_pJ = (
            energy_per_access_per_instance * accesses_per_instance * instances
        )
        read_energy = energy_per_access_per_instance * reads_per_instance * instances

        # find read-network connected to the current storage level based on network name
        for n in network_ptrs:
            network_name = n.findall("first")[0].text
            network_src = network_name.split(None, 1)[0]
            if network_src == level_name:
                network = n.findall("second")[0].findall("px")[0]
                break

        # get the network stats
        network_stats = network.findall("stats_")[0]

        # router energy
        num_hops = get_stat(network_stats, "num_hops", float)
        energy_per_hop_per_instance = get_stat(network_stats, "energy_per_hop", float)
        ingresses = get_stat(network_stats, "ingresses", int)
        network_energy_per_instance_pJ = get_stat(network_stats, "energy", float)
        network_energy_in_pJ = network_energy_per_instance_pJ * instances

        # multicast factors
        multicast = get_stat(network_stats, "multicast_factor", int)
        dist_multicast = get_stat(network_stats, "distributed_multicast", int)

        # energy for "add" operations
        spatial_add_energy_per_instance = get_stat(
            network_stats, "spatial_reduction_energy", float
        )
        spatial_add_energy = np.nansum(spatial_add_energy_per_instance * instances)

        temporal_add_energy_per_instance = get_stat(
            stats, "temporal_reduction_energy", float
        )
        temporal_add_energy = np.nansum(temporal_add_energy_per_instance * instances)

        # energy for address generation
        addr_generation_energy_per_cluster = get_stat(stats, "addr_gen_energy", float)
        addr_generation_energy = np.nansum(
            addr_generation_energy_per_cluster * clusters
        )

        # handle dummy level cases where capacity is forced to zero
        if not total_capacity:
            utilization = 0
        else:
            utilization = sum(
                (capacity * instances) / (total_capacity * total_instances)
            )

        # add energy summary for this level to the summary dictionary
        energy_summary_pJ[level_name] = {
            "energy": (
                np.nansum(storage_access_energy_in_pJ)
                + np.nansum(network_energy_in_pJ)
                + spatial_add_energy
                + temporal_add_energy
                + addr_generation_energy
            ),
            "storage_access_energy": np.nansum(storage_access_energy_in_pJ),
            "read_energy": np.nansum(read_energy),
            "spatial_add_energy": spatial_add_energy,
            "temporal_add_energy": temporal_add_energy,
            "addr_generation_energy": addr_generation_energy,
            "network_energy": np.nansum(network_energy_in_pJ),
            "energy_per_access_per_instance": energy_per_access_per_instance,
            "reads_per_instances": reads_per_instance,
            "updates_per_instances": updates_per_instance,
            "fills_per_instances": fills_per_instance,
            "accesses_per_instances": accesses_per_instance,
            "instances": instances,
            "utilization": utilization,
            "multicast": multicast,
            "dist_multicast": dist_multicast,
            "num_hops": num_hops,
            "ingresses": ingresses,
            "energy_per_hop_per_instance": energy_per_hop_per_instance,
        }

    # total energy for all levels
    energy_pJ = sum([value["energy"] for key, value in energy_summary_pJ.items()])

    # check to see if timeloop produced an output, aka did it have an arithmetic level
    if arithmetic_level_found:
        output = {
            "problem": prob,
            "utilization": arithmetic_utilization,
            "cycles": cycles,
            "energy_pJ": energy_pJ,
            "energy_per_mac": energy_pJ / macs,
            "macs": macs,
            "energy_summary_pJ": energy_summary_pJ,
        }
    else:
        output = {}

    return output


def gather_outputs(path_to_output_folder, verbose=False):
    """Gathers the xml stats in the output folder and generates summary files
    for all of the given input problems. Verbose toggles how detailed the
    summaries are (currently not implemented, and all summaries are saved.
    """
    # list of paths to all the output stats generated
    stats_paths = [f for f in path_to_output_folder.rglob("*.map+stats.xml")]

    # save energy summaries (short summary and verbose summaries) of all problem files ran
    short_summary_keys = ["filename", "utilization", "energy_pJ"]
    short_summary_dict = {key: [] for key in short_summary_keys}
    detailed_summary = {}
    verbose_summary_keys = [
        "filename",
        "problem",
        "utilization",
        "cycles",
        "energy_pJ",
        "energy_per_mac",
        "macs",
    ]
    verbose_summary_dict = {key: [] for key in verbose_summary_keys}

    for path in stats_paths:
        # organize by filename
        stats_filename = Path(path.stem).stem
        short_summary_dict["filename"].append(str(stats_filename))
        verbose_summary_dict["filename"].append(str(stats_filename))

        # get actual stats using helper function
        stats = parse_timeloop_stats(path)

        # save stats
        short_summary_dict["utilization"].append(stats["utilization"])
        short_summary_dict["energy_pJ"].append(stats["energy_pJ"])
        for key in stats.keys():
            if key != "energy_summary_pJ":
                # save more detailed stats
                verbose_summary_dict[key].append(stats[key])
            elif key == "energy_summary_pJ":
                # save very detailed summary from parser
                detailed_summary[stats_filename] = stats[key]

        # remove the stats xml after getting its data
        os.remove(path)

    # convert dicts to dataframes for output message and easy storage
    short_summary_df = pd.DataFrame(short_summary_dict)
    short_summary = short_summary_df.sort_values(
        by="filename",
        key=lambda x: np.argsort(index_natsorted(short_summary_df["filename"])),
    ).reset_index(drop=True)
    verbose_summary_df = pd.DataFrame(verbose_summary_dict)
    verbose_summary = verbose_summary_df.sort_values(
        by="filename",
        key=lambda x: np.argsort(index_natsorted(verbose_summary_df["filename"])),
    ).reset_index(drop=True)

    # output summary and save it to a csv file
    print("Summary:")
    if verbose:
        pprint.pprint(verbose_summary)
        verbose_summary_file = "verbose_summary.csv"
        vsum_path = path_to_output_folder / verbose_summary_file
        verbose_summary.to_csv(vsum_path)
        print("")
        print("Verbose summary stored in {}".format(vsum_path))
    else:
        pprint.pprint(short_summary)
        short_summary_file = "short_summary.csv"
        ssum_path = path_to_output_folder / short_summary_file
        short_summary.to_csv(ssum_path)
        print("")
        print("Short summary stored in {}".format(ssum_path))

    # save detailed summary to pkl for more in-depth analysis and plotting
    detailed_summary_file = "detailed_summary.pkl"
    dsum_path = path_to_output_folder / detailed_summary_file
    with open(dsum_path, "wb") as dsum_file:
        pickle.dump(detailed_summary, dsum_file, pickle.HIGHEST_PROTOCOL)
    print("Detailed summaries of each problem stored in {}".format(dsum_path))
    print("")

    # move all the logs in a log folder
    log_paths = [f for f in path_to_output_folder.rglob("*.log")]
    log_dest = path_to_output_folder / "logs"
    log_dest.mkdir(exist_ok=True)
    for file in log_paths:
        file.rename(log_dest / file.name)
