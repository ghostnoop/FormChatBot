import json
import os


async def load_fixtures():
    from db.models import Fixture, _models

    path = 'fixtures'
    files = []
    for (dir_path, dir_names, file_names) in os.walk(path):
        files.extend(file_names)
        break

    fixtures = list(await Fixture.all().values_list('name', flat=True))

    for file in files:
        if file in fixtures:
            continue

        with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
            data: dict = json.loads(f.read())

        lst = []
        for model, items in data.items():
            MODEL = _models[model]
            for item in items:
                lst.append(MODEL(**item))

            await MODEL.bulk_create(lst)

        await Fixture.create(name=file)
