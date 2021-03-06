const Locations = require("../models/locations.model");
const Regions = require("../models/regions.model");

/**
 * Creates a location
 * @param location Location object with fields
 * @param storeId
 * @returns {Promise<void>}
 */
const create = async function (location, storeId) {
    // create or get region
    const regionId = (await createOrGetRegion(location.region)).regionId;
    await Locations.insert({regionId, ...location}, storeId);
}
exports.create = create;

/**
 * Given a region name, gets an existing one or creates if not.
 * @param newRegion Name of new region.
 * @returns {Promise<*>} Region object.
 */
const createOrGetRegion = async function (newRegion) {
    let region = await Regions.getByName(newRegion);
    if (!region) {
        await Regions.insert({name: newRegion});
        region = await Regions.getByName(newRegion);
    }
    return region
};
exports.createOrGetRegion = createOrGetRegion;
