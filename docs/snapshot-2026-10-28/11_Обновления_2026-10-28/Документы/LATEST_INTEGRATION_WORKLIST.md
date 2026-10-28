**Русский** · [English](../../../en/docs/snapshot-2026-10-28/11_Updates_2026-10-28/Documents/LATEST_INTEGRATION_WORKLIST.md)

# CCZMP — очередь интеграции свежих моделей

Дата: 23.10.2026. Наличие архива означает только доступность исходника. Статусы ниже не являются подтверждением конвертации.

| Донор | Требуемый контроллер | Функции | Статус |
|---|---|---|---|
| 2011_volvo_c30_wtcc.zip | car_controller | drive, fuel, damage, trunk, seats | исходник, проверка интеграции не выполнена |
| bmw_x6m_competition_assetto__www.vecarz.com.zip | car_controller | drive, fuel, damage, trunk, seats | исходник, проверка интеграции не выполнена |
| ford_crown_victoria_lx_2011.zip | car_controller | drive, fuel, damage, trunk, seats | исходник, проверка интеграции не выполнена |
| subaru_wrx_wagon_gg.zip | car_controller | drive, fuel, damage, trunk, seats | исходник, проверка интеграции не выполнена |
| 2014_volvo_7900a_hybrid.zip | bus_controller | drive, passenger doors, articulated sections | исходник, проверка интеграции не выполнена |
| 1997_mercedes_clk_gtr_gt1.zip | car_controller | drive, fuel, damage, trunk, seats | исходник, проверка интеграции не выполнена |
| 2002_mercedes-benz_clk_dtm.zip | car_controller | drive, fuel, damage, trunk, seats | исходник, проверка интеграции не выполнена |
| 2005_mercedes-benz_amg_c-class_w203_dtm.zip | car_controller | drive, fuel, damage, trunk, seats | исходник, проверка интеграции не выполнена |
| lowpoly_sedan__wagon.zip | car_controller | separate meshes, drive | исходник, проверка интеграции не выполнена |
| peugeot_expert.zip | car_controller | drive, fuel, damage, trunk, seats | исходник, проверка интеграции не выполнена |
| suzuki_carry_blind_van.zip | car_controller | drive, fuel, damage, trunk, seats | исходник, проверка интеграции не выполнена |
| tata_signa_cargo_truck__low_poly_game_ready_pbr.zip | heavy_truck_controller | drive, cargo, towing | исходник, проверка интеграции не выполнена |
| 1992_jaguar_xj220.zip | car_controller | drive, fuel, damage, trunk, seats | исходник, проверка интеграции не выполнена |
| bugatti_bolide_2024__www.vecarz.com.zip | car_controller | drive, fuel, damage, trunk, seats | исходник, проверка интеграции не выполнена |
| mercedes-benz_g-class_2021.zip | car_controller | drive, fuel, damage, trunk, seats | исходник, проверка интеграции не выполнена |
| ebrc_jaguar_infantry_fighting_vehicle.zip | wheeled_armored_controller | drive, turret, crew, damage | исходник, проверка интеграции не выполнена |
| russian_ka-52_alligator.zip | rotorcraft_controller | pilot, lift, yaw, pitch, land, rotor | исходник, проверка интеграции не выполнена |
| su-30mkk_with_kh-59m.zip | fixed_wing_controller | thrust, pitch, roll, yaw, takeoff, landing | исходник, проверка интеграции не выполнена |
| vietnam_people_air_forces_-_su-27sk.zip | fixed_wing_controller | thrust, pitch, roll, yaw, takeoff, landing | исходник, проверка интеграции не выполнена |
| crane_machine_tower_liebherr_lowpoly.zip | static_world_mechanism | placement, collision, optional lifting mechanism | исходник, проверка интеграции не выполнена |
| murphy_97_sp_cruiser_-_low_poly_model.zip | car_controller | drive, lights, siren, agency access | исходник, проверка интеграции не выполнена |
| negotiator_80_cop_cruiser_-_low_poly_model.zip | car_controller | drive, lights, siren, agency access | исходник, проверка интеграции не выполнена |
| car_tahoe_police.zip | car_controller | drive, lights, siren, agency access | исходник, проверка интеграции не выполнена |
| goldeneye_007_-_dam_level_baked.zip | level_editor | placement, collision, optimization | исходник, проверка интеграции не выполнена |

## Критерии приёмки
1. Для каждой отдельной модели — собственная секция и ссылка на OGF, текстуры, материалы, коллизии.
2. Наличие в F7/соответствующем каталоге, спавн без ошибок движка.
3. Категорийная механика в реальной игровой сессии; поведение именно данной модели, не фиктивный общий класс.
4. Сохранение/загрузка в течение нескольких циклов, корректное состояние после смерти/уничтожения.
5. Проверка лицензии до распространения сборки.

Не изменять gamedata до проверки соответствия фактических ресурсов/скриптов и создания rollback.
