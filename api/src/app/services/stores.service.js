const {NoneUniqueInternalStoreIdException} = require("../exceptions/stores");
const Regions = require("../models/regions.model");
const Stores = require("../models/stores.model");
const LocationsService = require("../services/locations.service");
const {NonExistentRegionException} = require("../exceptions/regions");
const BrandsService = require("../services/brands.service")

/**
 * Expects a brandId in the body.
 * @param newStore Object for the stores parameters.
 * @returns {Promise<void>} Store ID
 */
const create = async function (newStore) {
    const region = await Regions.getById(newStore.regionId);

    // if a region is provided but doesn't exist
    if (newStore.regionId != null && region == null) {
        throw new NonExistentRegionException("Field regionId doesn't reference a region");
    }

    // check if brand exists
    await BrandsService.checkExistsAndGet(newStore.brandId);

    // check the store doesn't already exist
    await checkStoreDoesntExistByInternalId(newStore.internalId, newStore.brandId);

    // create the store
    const storeId = await Stores.insert(newStore);

    // create the stores location
    await LocationsService.create(newStore.location, storeId);

    return storeId;
};

/**
 * Checks that a store with internalId doesn't already exist.
 * Throws a NoneUniqueInternalStoreIdException exception if not unique.
 * @param internalId InternalId of the store
 * @param brandId BrandId of the store
 * @returns {Promise<void>} None
 */
const checkStoreDoesntExistByInternalId = async function (internalId, brandId) {
    if (!(await getStoreByInternalId(internalId, brandId))) {
        throw new NoneUniqueInternalStoreIdException(
            `Store with internalId '${internalId}' and brandId ${brandId} already exists`)
    }
}

const getStoreByInternalId = async function (internalId, brandId) {
    return await Stores.getByInternalId(internalId, brandId);
}

exports.create = create;
exports.checkStoreDoesntExistByInternalId = checkStoreDoesntExistByInternalId;
exports.getStoreByInternalId = getStoreByInternalId;
