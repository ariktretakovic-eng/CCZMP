[Русский](../../../../../snapshot-2026-10-28/11_%D0%9E%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F_2026-10-28/%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B/LATEST_INTEGRATION_WORKLIST.md) · **English** · [Documentation index](../../../INDEX.md) · [Translation notes](../../../../TRANSLATION.md)

# CCZMP - integration queue for new models

Date: 10/23/2026. The presence of an archive only means the availability of the source. The statuses below are not confirmation of conversion.

| Donor | Required controller | Functions | Status |
|---|---|---|---|
| 2011_volvo_c30_wtcc.zip | car_controller | drive, fuel, damage, trunk, seats | source code, integration check failed |
| bmw_x6m_competition_assetto__www.vecarz.com.zip | car_controller | drive, fuel, damage, trunk, seats | source code, integration check failed |
| ford_crown_victoria_lx_2011.zip | car_controller | drive, fuel, damage, trunk, seats | source code, integration check failed |
| subaru_wrx_wagon_gg.zip | car_controller | drive, fuel, damage, trunk, seats | source code, integration check failed |
| 2014_volvo_7900a_hybrid.zip | bus_controller | drive, passenger doors, articulated sections | source code, integration check failed |
| 1997_mercedes_clk_gtr_gt1.zip | car_controller | drive, fuel, damage, trunk, seats | source code, integration check failed |
| 2002_mercedes-benz_clk_dtm.zip | car_controller | drive, fuel, damage, trunk, seats | source code, integration check failed |
| 2005_mercedes-benz_amg_c-class_w203_dtm.zip | car_controller | drive, fuel, damage, trunk, seats | source code, integration check failed |
| lowpoly_sedan__wagon.zip | car_controller | separate meshes, drive | source code, integration check failed |
| peugeot_expert.zip | car_controller | drive, fuel, damage, trunk, seats | source code, integration check failed |
| suzuki_carry_blind_van.zip | car_controller | drive, fuel, damage, trunk, seats | source code, integration check failed |
| tata_signa_cargo_truck__low_poly_game_ready_pbr.zip | heavy_truck_controller | drive, cargo, towing | source code, integration check failed |
| 1992_jaguar_xj220.zip | car_controller | drive, fuel, damage, trunk, seats | source code, integration check failed |
| bugatti_bolide_2024__www.vecarz.com.zip | car_controller | drive, fuel, damage, trunk, seats | source code, integration check failed |
| mercedes-benz_g-class_2021.zip | car_controller | drive, fuel, damage, trunk, seats | source code, integration check failed |
| ebrc_jaguar_infantry_fighting_vehicle.zip | wheeled_armored_controller | drive, turret, crew, damage | source code, integration check failed |
| russian_ka-52_alligator.zip | rotorcraft_controller | pilot, lift, yaw, pitch, land, rotor | source code, integration check failed |
| su-30mkk_with_kh-59m.zip | fixed_wing_controller | thrust, pitch, roll, yaw, takeoff, landing | source code, integration check failed |
| vietnam_people_air_forces_-_su-27sk.zip | fixed_wing_controller | thrust, pitch, roll, yaw, takeoff, landing | source code, integration check failed |
| crane_machine_tower_liebherr_lowpoly.zip | static_world_mechanism | placement, collision, optional lifting mechanism | source code, integration check failed |
| murphy_97_sp_cruiser_-_low_poly_model.zip | car_controller | drive, lights, siren, agency access | source code, integration check failed |
| negotiator_80_cop_cruiser_-_low_poly_model.zip | car_controller | drive, lights, siren, agency access | source code, integration check failed |
| car_tahoe_police.zip | car_controller | drive, lights, siren, agency access | source code, integration check failed |
| goldeneye_007_-_dam_level_baked.zip | level_editor | placement, collision, optimization | source code, integration check failed |

## Criteria acceptance testing
1. For each individual model - its own section and a link to OGF, textures, materials, collisions.
2. Availability in F7/corresponding directory, spawn without engine errors.
3. Category mechanics in a real game session; the behavior of this particular model, not a fictitious general class.
4. Preservation/loading for several cycles, correct state after death/destruction.
5. Verify the license before distributing the assembly.

Do not change gamedata until the actual resources/scripts are matched and a rollback is created.
