const Categories = require('../models/categories.model');

// returns a category
async function getByNameOrCreate(name) {
    const lowerCaseName = name.toLowerCase();
    let category = await Categories.getByName(lowerCaseName);
    if (!category) {
        category = await Categories.insert({'name': lowerCaseName})
    }

    return category
}
exports.getByNameOrCreate = getByNameOrCreate;