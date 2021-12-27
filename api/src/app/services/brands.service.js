const {NonExistentBrandException} = require("../exceptions/brands");

const BrandsModel = require("../models/brands.model");

/**
 * Gets a single brand.
 * Throws an exception if the brand doesn't exist
 * @param brandId BrandId to get.
 * @returns {Promise<void>}
 */
const checkExistsAndGet = async function (brandId) {
    const brand = await get(brandId);
    if (brand == null) {
        throw new NonExistentBrandException(`Brand with ID ${brandId} does not exist`)
    }
};
exports.checkExistsAndGet = checkExistsAndGet;

/**
 * Gets a brand by ID.
 * @param brandId
 * @returns {Promise<null|*|undefined>}
 */
const get = async function (brandId) {
    return await BrandsModel.getById(brandId);
}
exports.get = get;
