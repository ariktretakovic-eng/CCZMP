[Русский](../../../../snapshot-2026-10-28/07_%D0%A1%D1%82%D0%B0%D0%B1%D0%B8%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B8/verification__results.md) · **English** · [Documentation index](../../INDEX.md) · [Translation notes](../../../TRANSLATION.md)

# CCZMP checks, 10/10/2026

205 automated tests pass. 1075 installed working files verified against SHA-256: no discrepancies. 930 OGG buffers have exactly 44100 PCM frames at 44100 Hz. The geometry, skeleton, animations and physics of the Mercedes IC are the same as the existing improved W140; 30 materials use separate DDS.

The game tested the common fragment and second limit of two receivers, auto-on, display of two trunk inventories, release of input after closing, radio/player control and spatial sound of the car with the volume reduced outside. Mercedes IC is built with GPS, alarm and suspension. The horn is playing, Win32 reading of H via LuaJIT FFI is available.

loading saving in the new process confirmed the exact initial value of the broadcast clock of 21134 ms, the state of the receivers being turned on, 17 units of fuel and the original item in the trunk with a state of 0.63 and a charge of 37. User autosaves are not changed, the settings are restored; temporary test scripts have been removed.

Limitations: The full native entry/exit cycle and the separate H press from the driver's seat are not supported by the new stand. The indoor/outdoor volume logic is covered in tests. Synchronization by second buffers, without measuring the coincidence of audio samples; joining takes up to a second. There is no network protocol between clients. Voice inserts are temporarily synthetic. The IC base is waiting for coordinates, the vehicle pack has been cancelled, air transport has not been introduced.

car_radio_native.png shows the broadcast and the horn button, not the trunk. Full logs and reconciliation results are attached.
