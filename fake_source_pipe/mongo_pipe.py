import logging
import time
from random import choice, choices, randint

import pymongo


MONGO_URI = 'mongodb://mongodb-headless.mongodb.svc.cluster.local:27017/'
MONGO_DB = 'database'
MONGO_COLLECTION = 'users'

SERVICES = ['mamba', 'tinder', 'vk', 'facebook', 'drugvokrug', 'odnoklassniki']
NAMES = [
    'Alice', 'Bob', 'Charlie', 'Boris', 'Abby',
    'Piter', 'Chip', 'Dale', 'Hank', 'Masha'
]
SURNAMES = [
    'Petrova', 'Marley', 'Lee', 'Star',
    'Brown', 'Ivanov', 'Shilova', 'Popov', 'Lollypopova'
]
AGES = {'min': 0, 'max': 999}
POSSIBLE_OPERATIONS = ['insert', 'update', 'delete']
OPERATIONS_WEIGHTS = [100, 100, 15]


def run_part(mongo_collection):
    total_manapulations = randint(1, 10_000)
    logging.info(f" >>> Manipulations part : {total_manapulations}")
    for _ in range(0, total_manapulations):
        chosen_operation = choices(
            POSSIBLE_OPERATIONS,
            weights=OPERATIONS_WEIGHTS
        )[0]

        if chosen_operation == 'insert':
            _age = randint(AGES['min'], AGES['max'])
            mongo_collection.insert_one(
                {
                    'service': choice(SERVICES),
                    'name': f"{choice(NAMES)}_{_age}",
                    'surname': choice(SURNAMES),
                    'age': _age
                }
            )

        elif chosen_operation == 'delete':
            ids = mongo_collection.find({}, {'_id': 1})
            id_list = [doc['_id'] for doc in ids]
            if len(id_list):
                mongo_collection.delete_one({'_id': choice(id_list)})

        else:
            mongo_collection.update_one(
                    {
                        'name': f"{choice(NAMES)}_{_age}"
                    },
                    {
                        '$set': {
                            'age': randint(AGES['min'], AGES['max'])
                        }
                    }
            )


if __name__ == '__main__':
    mongo_client = pymongo.MongoClient(MONGO_URI)
    mongo_collection = mongo_client[MONGO_DB][MONGO_COLLECTION]

    while True:
        run_part(mongo_collection)
        time.sleep(randint(3, 30))
