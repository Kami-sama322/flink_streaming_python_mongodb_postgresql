// Set values
const dbName = 'database'
const collectionName = 'users'

// Create or switch to the database
db = db.getSiblingDB(dbName);

// Create collection
db.createCollection(collectionName);

// Insert documents into the collection
db[collectionName].insertMany([
    { service: 'tinder', name: 'Boris', surname: 'The blade' , age: 45 },
    { service: 'vk', name: 'Pavel', surname: 'Losev', age: 14 },
    { service: 'facebook', name: 'Mark', surname: 'Mask', age: 32 },
    { service: 'mamba', name: 'Elena', surname: 'Vorobey', age: 18 },
    { service: 'drugvokrug', name: 'Anna', surname: 'Kurnikuva', age: 22 }
]);

