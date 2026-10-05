# Stalker Anomaly 1.5.1 — project index

Generated 2026-10-02 by `_index/report.py`. Rebuild with `python _index/build.py`.

Everything in this project was *not* read into the model context. Instead the whole tree is walked once, parsed, and stored as a queryable graph in `_index/anomaly.db`; the assistant queries that database on demand and only ever pulls a few dozen rows.

## 1. What is in the install

| metric | value |
|---|---|
| files indexed | 48,316 |
| directories | 3,204 |
| symbols (config sections, script functions, XML nodes) | 108,491 |
| &nbsp;&nbsp;of which LTX config sections | 31,829 |
| &nbsp;&nbsp;of which script functions / methods | 11,079 |
| &nbsp;&nbsp;of which XML nodes | 64,417 |
| graph edges | 1,220,128 |
| edges resolved to another file | 271,935 |
| edges resolved to another symbol | 542,153 |
| files referenced by something else | 13,408 |
| files that reference something else | 12,560 |
| files with no semantic link in either direction | 28,052 |

### Size by area

| grp | files | mb |
|----------------------------------|-------|---------|
| db | 66 | 16395.2 |
| unpacked/textures | 17188 | 10748.1 |
| unpacked/levels | 2591 | 6828.5 |
| unpacked/meshes | 4277 | 2334.9 |
| unpacked/sounds | 18115 | 1171.3 |
| bin | 15 | 195.2 |
| unpacked/spawns | 1 | 92.9 |
| unpacked/configs | 3802 | 29.2 |
| appdata | 373 | 7.9 |
| unpacked/scripts | 414 | 6.2 |
| AnomalyLauncher.exe | 1 | 2.0 |
| unpacked/particles.xr | 1 | 2.0 |
| unpacked/anims | 477 | 1.3 |
| tools | 5 | 1.0 |
| unpacked/shaders | 946 | 0.9 |
| unpacked/textures.ltx | 1 | 0.7 |
| unpacked/gamemtl.xr | 1 | 0.3 |
| unpacked/shaders.xr | 1 | 0.2 |
| _index | 3 | 0.2 |
| default-44100.mhr | 1 | 0.1 |
| default-48000.mhr | 1 | 0.1 |
| gamedata | 3 | 0.1 |
| unpacked/lanims.xr | 1 | 0.0 |
| unpacked/ai | 24 | 0.0 |
| unpacked/valid_item_sections.ltx | 1 | 0.0 |
| unpacked/shaders_xrlc.xr | 1 | 0.0 |
| fsgame.ltx | 1 | 0.0 |
| unpacked/senvironment.xr | 1 | 0.0 |
| DO_NOT_INSTALL_OLD_ADDONS | 1 | 0.0 |
| AnomalyLauncher.cfg | 1 | 0.0 |
| .vscode | 1 | 0.0 |
| commandline.txt | 1 | 0.0 |

### Size by file type

| ext | files | mb |
|---------|-------|---------|
| ogg | 18114 | 1171.3 |
| dds | 10959 | 12384.2 |
| thm | 7132 | 1.5 |
| ogf | 4863 | 2144.0 |
| ltx | 3245 | 15.9 |
| xml | 668 | 13.4 |
| ps | 448 | 0.3 |
| script | 413 | 6.2 |
| (none) | 396 | 146.3 |
| omf | 386 | 176.4 |
| anm | 346 | 1.2 |
| vs | 248 | 0.2 |
| s | 165 | 0.1 |
| ppe | 115 | 0.1 |
| ini | 103 | 0.7 |
| h | 73 | 0.3 |
| db0 | 57 | 13098.4 |
| spawn | 35 | 96.8 |
| ai | 34 | 258.0 |
| cform | 34 | 1459.3 |
| env_mod | 34 | 0.0 |
| fog_vol | 34 | 0.0 |
| game | 34 | 1.8 |
| geom | 34 | 2333.7 |
| geomx | 34 | 672.3 |


## 2. How the game is laid out

The shipped build is packed: `db/*.db*` are X-Ray archives. `tools/converter.exe -unpack` has already expanded them into `tools/_unpacked/`, which is where the real content lives.

| area     | files | mb      |
|----------|-------|---------|
| textures | 17188 | 10748.1 |
| levels   | 2591  | 6828.5  |
| meshes   | 4277  | 2334.9  |
| sounds   | 18115 | 1171.3  |
| spawns   | 1     | 92.9    |
| configs  | 3802  | 29.2    |
| scripts  | 414   | 6.2     |
| anims    | 477   | 1.3     |
| shaders  | 946   | 0.9     |
| ai       | 24    | 0.0     |

The semantic core — the part a modder actually edits — is much smaller than the install:

| ext | files | kb |
|---------|-------|---------|
| ltx | 3129 | 15349.5 |
| xml | 668 | 13758.1 |
| script | 413 | 6349.9 |
| dds | 3 | 683.1 |
| dic | 1 | 2.4 |
| mdl | 1 | 63.9 |
| scriptx | 1 | 45.6 |

Breakdown of `tools/_unpacked/configs`, the tree a mod actually edits:

| subtree     | files | kb     |
|-------------|-------|--------|
| text        | 276   | 9420.2 |
| items       | 404   | 7248.2 |
| gameplay    | 229   | 2538.9 |
| scripts     | 2016  | 2329.2 |
| ui          | 215   | 1818.7 |
| misc        | 131   | 1454.7 |
| environment | 108   | 1188.0 |
| models      | 213   | 1111.4 |
| creatures   | 67    | 1035.8 |
| plugins     | 27    | 430.1  |
| prefetch    | 4     | 394.9  |
| mp          | 26    | 305.1  |
| presets     | 10    | 159.6  |
| zones       | 22    | 77.8   |
| ai_tweaks   | 17    | 23.8   |


## 3. Levels

Each level folder becomes a graph node, so a level can be traced to its spawn data, AI, lightmaps, meshes and every config that mentions it.

| level | files | mb | cfg_mentions |
|-----------------------|-------|-------|--------------|
| pripyat | 135 | 485.4 | 10 |
| jupiter | 163 | 407.6 | 19 |
| zaton | 80 | 396.1 | 23 |
| k02_trucks_cemetery | 57 | 359.0 | 3 |
| l12_stancia_2 | 137 | 347.4 | 2 |
| l13_generators | 133 | 329.0 | 2 |
| l04_darkvalley | 61 | 319.8 | 2 |
| k00_marsh | 102 | 316.7 | 5 |
| l11_pripyat | 154 | 291.4 | 2 |
| l01_escape | 89 | 282.0 | 4 |
| l07_military | 68 | 275.2 | 3 |
| l03_agroprom | 34 | 238.3 | 3 |
| l12_stancia | 99 | 226.3 | 2 |
| l10_limansk | 92 | 219.1 | 2 |
| l10_radar | 51 | 218.6 | 2 |
| l09_deadcity | 77 | 214.0 | 2 |
| l02_garbage | 55 | 210.2 | 3 |
| l05_bar | 50 | 205.1 | 2 |
| l08_yantar | 44 | 181.2 | 2 |
| l06_rostok | 172 | 172.2 | 3 |
| k01_darkscape | 26 | 164.0 | 2 |
| l10_red_forest | 122 | 161.5 | 2 |
| y04_pole | 47 | 134.8 | 3 |
| l12u_sarcofag | 38 | 112.6 | 2 |
| l03u_agr_underground | 22 | 105.6 | 2 |
| l13u_warlab | 209 | 89.8 | 2 |
| l10u_bunker | 15 | 77.7 | 2 |
| jupiter_underground | 38 | 62.0 | 2 |
| l04u_labx18 | 126 | 58.3 | 2 |
| l11_hospital | 24 | 49.8 | 2 |
| l08u_brainlab | 22 | 49.0 | 2 |
| l12u_control_monolith | 16 | 41.4 | 2 |
| labx8 | 21 | 25.3 | 2 |
| fake_start | 12 | 2.0 | 2 |


## 4. Relation types

| type | edges | from_files | to_files | to_symbols | resolved_pct |
|----------------|--------|------------|----------|------------|--------------|
| call | 398429 | 403 | 0 | 4670 | 100.0 |
| binref | 258335 | 8625 | 6808 | 311 | 15.8 |
| param | 244406 | 3089 | 4019 | 17692 | 23.0 |
| same_stem | 172938 | 27711 | 27711 | 0 | 100.0 |
| call_dyn | 78905 | 392 | 0 | 4277 | 100.0 |
| contain | 48316 | 1 | 48316 | 0 | 100.0 |
| inherit | 10178 | 578 | 0 | 1248 | 98.4 |
| xml_parent | 4902 | 58 | 0 | 208 | 100.0 |
| level_contains | 2591 | 34 | 2591 | 0 | 100.0 |
| include | 1003 | 520 | 431 | 0 | 99.7 |
| strref | 96 | 68 | 0 | 0 | 0.0 |
| script_ref | 19 | 6 | 0 | 0 | 0.0 |
| xml_ref | 10 | 8 | 2 | 0 | 60.0 |

| type | meaning |
|---|---|
| `include` | `#include` directive in a config |
| `inherit` | LTX `[section]:parent` inheritance |
| `param` | a single `key = value` in a config; resolved to a file or a section when it points at one |
| `call` | script function call resolved to its definition |
| `call_dyn` | method call `:name()` resolved through the global symbol table |
| `binref` | readable string recovered from a binary container (`.spawn`, `.ai`, `.ogf`, ...) |
| `xml_parent` | XML element nested in another |
| `level_contains` | file belongs to a level |
| `contain` | file belongs to a folder |
| `same_stem` | files sharing a base name, e.g. `w_ak74.ltx` / `w_ak74.ogf` / icon atlas |

## 5. What the index resolves

| type | total | to_file | to_symbol | kept_as_text |
|----------------|--------|---------|-----------|--------------|
| call | 398429 | 0 | 398429 | 0 |
| binref | 258335 | 39805 | 899 | 40709 |
| param | 244406 | 7279 | 49006 | 39099 |
| call_dyn | 78905 | 0 | 78905 | 0 |
| inherit | 10178 | 0 | 10012 | 10178 |
| xml_parent | 4902 | 0 | 4902 | 0 |
| level_contains | 2591 | 2591 | 0 | 0 |
| include | 1003 | 1000 | 0 | 384 |
| strref | 96 | 0 | 0 | 96 |
| script_ref | 19 | 0 | 0 | 19 |
| xml_ref | 10 | 6 | 0 | 10 |

The largest LTX keys by how many of their values resolved to a real file or section (this is the item/weapon/creature -> asset wiring):

| key | occurrences | to_file | to_section |
|-------------------|-------------|---------|------------|
| description | 3555 | 0 | 3390 |
| icon | 2789 | 0 | 2752 |
| active | 2508 | 0 | 2259 |
| visual | 2178 | 2160 | 0 |
| name | 2294 | 0 | 2118 |
| section | 2019 | 0 | 2019 |
| property | 1997 | 0 | 1997 |
| $spawn | 2566 | 13 | 1931 |
| elements | 1541 | 0 | 1541 |
| inv_name_short | 1660 | 0 | 1530 |
| inv_name | 1590 | 0 | 1466 |
| effects | 2181 | 0 | 1314 |
| story_id | 1024 | 0 | 959 |
| community | 873 | 0 | 856 |
| faction | 833 | 0 | 833 |
| character_profile | 815 | 0 | 804 |
| npc_community | 854 | 0 | 767 |
| sky_texture | 706 | 706 | 0 |
| ambient | 706 | 0 | 706 |
| title | 632 | 0 | 612 |

Text that could not be resolved is still stored, so `q.py grep` can find it:

| unresolved_value | n |
|---------------------------------------------|-------|
|  | 10083 |
| 1 | 9265 |
| 0 | 8517 |
| true | 5812 |
| false | 5504 |
| 1, 1 | 2749 |
| 2 | 2496 |
| inventory_upgrades.prereq_tooltip_functor_a | 2018 |
| inventory_upgrades.prereq_functor_a | 2018 |
| inventory_upgrades.precondition_functor_a | 2018 |
| inventory_upgrades.effect_functor_a | 2018 |
| 0.01 | 1998 |
| 1.0 | 1881 |
| 0.0 | 1825 |
| something_here | 1694 |


## 6. Files with no named reference

These are real, not a parse failure. The X-Ray sound engine loads whole banks by directory scan rather than by name — `sounds/ambient/**` is mixed at random by the ambience engine, and `sounds/characters_voice/scenario/<level>/**` is sampled per level — so no config line ever mentions an individual file in there. The same holds for LOD chains packed inside a single `.dds`, and for the vanilla content this heavily modded install no longer ships. Each such file is still attached to its folder through a `contain` edge, and its folder is the semantic unit the engine actually loads.

| ext | files | mb |
|-----|-------|---------|
| ogg | 16718 | 1086.3 |
| dds | 5100 | 3947.1 |
| thm | 4010 | 0.5 |
| xml | 601 | 12.7 |
| ps | 443 | 0.3 |
|  | 361 | 0.7 |
| anm | 212 | 0.8 |
| s | 163 | 0.1 |
| ppe | 110 | 0.1 |
| ini | 103 | 0.7 |
| db0 | 55 | 12997.5 |
| ltx | 43 | 0.5 |

Largest unreferenced areas, which is where engine-side directory scanning takes over:

| area | files | mb |
|---------------------------------------|-------|-------|
| tures/act | 834 | 289.6 |
| tures/prop | 761 | 137.4 |
| tures/mtl | 585 | 316.2 |
| tures/crete | 488 | 339.7 |
| tures/wpn | 416 | 108.6 |
| tures/ui | 392 | 69.4 |
| tures/ston | 391 | 382.5 |
| ders/r3 | 320 | 0.3 |
| tures/intro | 294 | 102.0 |
| nds/characters_voice/scenario/pripyat | 293 | 13.2 |
| nds/ambient/rnd_outdoor | 288 | 15.4 |
| nds/characters_voice/scenario/jupiter | 266 | 11.6 |


## 7. Querying the index

```
cd _index
python q.py stats              # headline numbers
python q.py stats table        # edges per relation type
python q.py tree tools/_unpacked/configs   # directory rollup
python q.py ls    <file>       # sections / functions defined in a file
python q.py show  <section|id> # full picture: body, parents, params, users
python q.py refs  <file>       # what this file points at
python q.py uses  <file>       # what points at this file
python q.py chain <file> -d 3  # transitive dependencies
python q.py rchain <section>   # transitive reverse dependencies
python q.py grep  <text>       # search params, binary refs, symbols, paths
python q.py levels             # per-level rollup
python q.py orphans            # files nothing links to
```
Rebuild a single stage without redoing the whole run:

```
python build.py ltx resolve params stats   # e.g. after editing the LTX parser
python build.py scan ltx script xml misc bin name atlas levels resolve params links stats
```
Stages: `scan ltx script xml misc bin name atlas levels resolve params prune links vacuum stats`.

## 8. Schema

```sql
files(id, path UNIQUE, dir, name, stem, ext, size, grp, lang, bin, parsed)
dirs(path, parent, depth, files, bytes)
symbols(id, file_id, kind, name, qname, parent, line)
edges(id, src_file, src_sym, type, key, raw, dst_file, dst_sym, dst_name, line)
nameidx(key, file_id)        -- every path/alias a config may refer to an asset by
blobs(id, file_id, key, val) -- raw key/value with no index (UI atlas rectangles, ...)
meta(k, v)                   -- build statistics
```
`kind` prefixes: `ltx_*` (actor/item/env/sound/ui/phys/logic/other), `script_fn`, `script_method`, `xml_*`, `c_symbol`, `level`.
