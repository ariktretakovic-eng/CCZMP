[Русский](../README.md) · [English overview](README.md) · [Complete English index](docs/INDEX.md)

# English documentation: scope and terminology

Published October 29, 2026. This edition provides English counterparts for all **87 documentation files** in source commit `3662e36433b102b2a43b870a91cbf7850e845f03` of `ariktretakovic-eng/CCZMP`.

The scope includes root documentation, current status pages, technical guides, dated reports, the complete published system/vehicle registers, module guides, the archived installation index, short `.txt` notes and historical prose concepts stored as `.ltx`. The latter are presented as Markdown for reading; they are not translated replacement game configuration files. Already-English filenames and identifiers are retained where appropriate.

## Translation method

The corpus was translated with machine assistance and a fixed technical glossary. Entry pages were edited for clarity. Coverage, relative links, Markdown structure, preserved examples and correspondence with the Russian originals were checked. The entire technical corpus has not received a line-by-line review by an independent human translator.

Historical dates, figures, incomplete features, contradictory stage-specific findings and uncertainty remain part of the documents. Translation does not constitute new game testing or acceptance of any feature. A specification describes intended behavior; a dated report describes its own stage.

Russian prose remains available at its original paths. Language links connect corresponding pages. The Russian source governs if wording is ambiguous. [The coverage manifest](translation-manifest.json) records each source, English counterpart and source revision.

## Technical material

Executable code examples, configuration keys, section IDs, commands, diagnostic strings and original paths are retained. Russian text inside literal examples may remain because it is part of the original UI, data or code. Links between documents lead to their English counterparts; links to implementation files lead to the original source files.

This is documentation localization. It does not change the game's UI language, localization tables, scripts or assets.

## Project glossary

| Russian term | English convention |
|---|---|
| НЧГ — Независимое Чернобыльское Государство | NChG — Independent Chernobyl State, the fictional state in project lore |
| СК | IC — Investigative Committee |
| МВД | MVD — Ministry of Internal Affairs |
| МЧС | MChS — Ministry of Emergency Situations |
| СЧС | SChS — the project's emergency service; distinct from MChS |
| ОМОН / СОБР | OMON / SOBR; retain the organizational acronyms |
| ФСИН | FSIN — penitentiary service |
| ОПГ | OCG — organized crime group |
| ЧВК | PMC — private military company |
| УК / АК | Criminal Code / Administrative Code |
| ТЗ | Technical specification |
| Мёртвый город | Dead City |
| ПДА / КПК | PDA; original item section IDs distinguish device types |
| Полномочия | Authority / permissions, according to context |
| Удостоверение | Service ID / identity document |
| Ордер | Warrant |
| Конвой | Custody escort; “convoy” in some historical translations |
| Секция транспорта | Vehicle configuration section; not necessarily a fully tested vehicle |
| Донор | Donor/source asset awaiting or undergoing conversion |
| Холодная / тёплая загрузка | Cold / warm loading of a saved game |
| Вылет | Crash |
| Нативная проверка | Test in the real game/engine |
| Mock-проверка | Test using simulated engine dependencies |
| Приёмка | Acceptance testing |

## Keeping both languages current

Update both current summaries when implementation changes. Keep dated reports as historical records. A new source document needs an English counterpart and an entry in the coverage manifest. Rebuild both indexes and run the [document checks](docs/INDEXING_EN.md) before publishing. Translation output should be reviewed against source limitations and evidence, not just grammar.
