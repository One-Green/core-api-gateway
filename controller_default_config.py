SPRINKLER: dict = {
    "soil_humidity_min": 40,
    "soil_humidity_max": 80
}

WATER_CONTROLLER: dict = {
    "water":
        {
            "tank":
                {
                    "unit": "percent",
                    "min_level": 20,
                    "max_level": 80,
                }
        },
    "pH":
        {
            "min_level": 7.5,
            "max_level": 7.8
        },
    "ec":
        {
            "unit": "mV",
            "min_level": 100,
            "max_level": 200
        }
}
