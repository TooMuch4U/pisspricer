const tools = require( "../services/tools");
const Items = require( "../models/items.model");
const Images = require( "../models/images.model");
const ItemsModel = require( '../models/items.model');
const Prices = require( "../models/itemPrices.model");
const {ItemDoesntExistException} = require( "../exceptions/items");

/**
 * Gets the item with matching internalSku
 * @param internalSku
 * @param brandId
 * @returns {Promise<null|*|undefined>}
 */
async function getItemByInternalSku(internalSku, brandId) {
    return await ItemsModel.getByInternalSku(internalSku, brandId)
}
exports.getItemByInternalSku = getItemByInternalSku;

async function create(newItem) {
    let barcode = newItem.barcode;
    let barcodeData = { "ean": barcode };
    delete newItem.barcode;
    let slugName = newItem.name + (typeof newItem.volumeEach == 'undefined' ? '' : newItem.volumeEach);
    // let data = tools.onlyInclude(req.body, Object.keys(rules));
    return await Items.insert(tools.toUnderscoreCase(data), barcodeData, slugName);
}
exports.create = create;

async function setImage(sku, image) {
    // get item form sku
    const item = await ItemsModel.getBySku(sku);

    // save image
    const path = `items/`;
    const blob = {"originalname": sku, "buffer": image};
    await Images.uploadImage(blob, path);

    // set image flag
    if (item.hasImage !== 1) {
        await Items.setImage(sku, 1);
    }
}
exports.setImage = setImage;

/**
 * Gets the item by sku.
 * Returns null if it doesn't exist
 * @param sku Sku of item to get
 * @returns {Promise<null|*|undefined>} The item, if it exists.
 */
async function getBySku(sku) {
    return await ItemsModel.getBySku(sku);
}
exports.getBySku = getBySku;

/**
 * Checks the item exists and returns if the price was new or not.
 * @param sku
 * @param storeId
 * @param newItemPrice
 * @returns {Promise<boolean|undefined>}
 */
async function setOrUpdatePrice(sku, storeId, newItemPrice) {
    // Check if sku exists
    const item = await getBySku(sku);
    if (!item) {
        throw new ItemDoesntExistException(`Item with SKU '${sku}' doesn't exist`);
    }

    // Insert price
    return await Prices.insertOrSetPrice(sku, storeId, newItemPrice);
}
exports.setOrUpdatePrice = setOrUpdatePrice;
