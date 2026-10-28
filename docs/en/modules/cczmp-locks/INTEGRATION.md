[Русский](../../../../modules/cczmp-locks/INTEGRATION.md) · **English** · [Documentation index](../../docs/INDEX.md) · [Translation notes](../../TRANSLATION.md)

# Integration of CCZMP Locks and API boundaries

Module dependencies are visible directly from [`cczmp_locks.script`](../../../../modules/cczmp-locks/gamedata/scripts/cczmp_locks.script). This is not an external X-Ray binary plugin: it uses the Anomaly Lua API and the CCZMP framework.

## Input points

| Function | Destination |
|---|---|
| `configure(id, pin)` | Sets a PIN to an existing open case |
| `unlock(id, pin)` | Checks PIN and sets temporary access |
| `close(id)` | Revokes current access |
| `info(id)` / `access(id)` | Return the condition and the right to open the case |
| `contents(id)` | Gets a list of objects actually located inside |
| `store(id, item_id)` | Starts or ends the transfer of the **original** game object to a hidden container |
| `take(id, item_id)` | Starts or ends a reverse transfer |
| `target(id)`, `check_job(token)`, `hack_result(token, success)` | Connection with hacking gameplay |
| `on_game_start()` | Signs loading and periodic update |

The case status is stored in `cczmp_items.item_state(item).vault`. Real items are held in the game `hidden_box`, and the record contains identifiers, sections and pending changes. Current access grants are **not serialized**, the PIN/container state is serialized through the CCZMP infrastructure.

## Dependencies

Required: `cczmp_items`, `cczmp_ops`, `cczmp_hacking`, `cczmp_items_ui`, `cczmp_ui` and gaming `alife()`, `db.actor`, `level`, `RegisterScriptCallback`, `alife_create`. Other Lua files in this directory exist for the playable test harness and are not separate releases.

## Invariants

- Do not create a copy of the content during normal transfer.
- Do not accept a repeat request for an item while the operation is awaiting completion.
- Check the identifiers of game objects and the owner, do not trust one numeric ID.
- Do not replace missing objects with a new “recovery” item.
- Do not consider isolated unit tests as proof of all native scripts.

## Installation package restrictions

This publication is a verified **source snapshot**: it does not contain game assets, texture atlases or a full set of item registrations for pure Anomaly. There is no automatic installation or guarantee of compatibility with other modpacks. The historical complete package included other subsystems and has been deliberately not copied in its entirety into this public catalog.
