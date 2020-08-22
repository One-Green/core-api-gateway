import rom
from datetime import datetime


class Config(rom.Model):
    tag = rom.Text(required=True, unique=True)
    soil_moisture_min_level = rom.Float(required=True, default=30)
    soil_moisture_max_level = rom.Float(required=True, default=60)


class Controller(rom.Model):
    tag = rom.Text(required=True, unique=True)
    water_valve_signal = rom.Boolean(default=False)


class Registry(rom.Model):
    tag = rom.Text(required=True, unique=True)


class UpdatedAt(rom.Model):
    tag = rom.Text(required=True, unique=True)
    dt = rom.DateTime(required=True, unique=True)


class Sprinklers:

    def __init__(self):

        self.registry = Registry

        self.config = Config
        self.soil_moisture_min_level: float = 0.0
        self.soil_moisture_max_level: float = 0.0

        self.controller = Controller
        self.water_valve_signal: bool = False

    @staticmethod
    def set_updated_datetime(tag: str) -> bool:
        UpdatedAt(tag=tag, dt=datetime.utcnow()).save()
        return True

    @staticmethod
    def get_updated_datetime(tag: str) -> datetime:
        return UpdatedAt.get_by(tag=tag).dt

    def is_tag_in_registry(self, tag: str) -> bool:
        for _ in self.registry.query.all():
            if _.tag == tag:
                return True
        return False

    def add_tag_in_registry(self, tag) -> bool:
        try:
            self.registry(tag=tag).save()
            return True
        except rom.UniqueKeyViolation:
            return False

    def update_config(
            self,
            tag: str,
            soil_moisture_min_level: float,
            soil_moisture_max_level: float,
    ):
        try:
            self.config \
                .get_by(tag=tag) \
                .update(soil_moisture_min_level=soil_moisture_min_level,
                        soil_moisture_max_level=soil_moisture_max_level) \
                .save()
        except AttributeError:
            self.config(
                tag=tag,
                soil_moisture_min_level=soil_moisture_min_level,
                soil_moisture_max_level=soil_moisture_max_level
            ).save()

    def get_config(self, tag: str):
        c = self.config.get_by(tag=tag)
        self.soil_moisture_min_level = c.soil_moisture_min_level
        self.soil_moisture_max_level = c.soil_moisture_max_level

    def update_controller(
            self,
            tag: str,
            water_valve_signal: bool):
        try:
            self.controller \
                .get_by(tag=tag) \
                .update(water_valve_signal=water_valve_signal) \
                .save()
        except AttributeError:
            self.controller(
                tag=tag,
                water_valve_signal=water_valve_signal
            ).save()

    def is_any_require_water(self) -> bool:
        """
        Check if any of sprinkler required water
        :return:
        """
        for _ in self.controller.query.all():
            if _.water_valve_signal:
                return True
        return False
